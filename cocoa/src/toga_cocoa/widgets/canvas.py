from math import ceil
from warnings import warn

from rubicon.objc import CGSize, objc_method, objc_property
from travertino.size import at_least

from toga.colors import BLACK, TRANSPARENT, Color
from toga.constants import Baseline, FillRule
from toga_cocoa.colors import native_color
from toga_cocoa.libs import (
    CGAffineTransformIdentity,
    CGFloat,
    CGPathDrawingMode,
    CGRectMake,
    NSAttributedString,
    NSFontAttributeName,
    NSForegroundColorAttributeName,
    NSGraphicsContext,
    NSImage,
    NSMutableDictionary,
    NSPoint,
    NSRect,
    NSSize,
    NSStrokeColorAttributeName,
    NSStrokeWidthAttributeName,
    NSView,
    core_graphics,
    kCGPathEOFill,
    kCGPathFill,
    kCGPathStroke,
)

from .base import Widget


class TogaCanvas(NSView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def drawRect_(self, rect: NSRect) -> None:
        context = NSGraphicsContext.currentContext.CGContext

        # Store this so we can restore the original if needed.
        self.original_matrix = core_graphics.CGContextGetCTM(context)
        self.using_standard_coords = self.original_matrix == CGAffineTransformIdentity
        # If we're not in the normal coordinate space (presumably because we're
        # rendering to a cache), save the inverse as well.
        if not self.using_standard_coords:
            self.inverse_original = core_graphics.CGAffineTransformInvert(
                core_graphics.CGContextGetCTM(context)
            )

        self.interface.context._draw(self.impl, draw_context=context)

    @objc_method
    def isFlipped(self) -> bool:
        # Default Cocoa coordinate frame is around the wrong way.
        return True

    @objc_method
    def mouseDown_(self, event) -> None:
        position = self.convertPoint(event.locationInWindow, fromView=None)
        if event.clickCount == 1:
            self.interface.on_press(position.x, position.y)
        else:
            self.interface.on_activate(position.x, position.y)

    @objc_method
    def rightMouseDown_(self, event) -> None:
        position = self.convertPoint(event.locationInWindow, fromView=None)
        self.interface.on_alt_press(position.x, position.y)

    @objc_method
    def mouseUp_(self, event) -> None:
        position = self.convertPoint(event.locationInWindow, fromView=None)
        self.interface.on_release(position.x, position.y)

    @objc_method
    def rightMouseUp_(self, event) -> None:
        position = self.convertPoint(event.locationInWindow, fromView=None)
        self.interface.on_alt_release(position.x, position.y)

    @objc_method
    def mouseDragged_(self, event) -> None:
        position = self.convertPoint(event.locationInWindow, fromView=None)
        self.interface.on_drag(position.x, position.y)

    @objc_method
    def rightMouseDragged_(self, event) -> None:
        position = self.convertPoint(event.locationInWindow, fromView=None)
        self.interface.on_alt_drag(position.x, position.y)


class Canvas(Widget):
    def create(self):
        self.native = TogaCanvas.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        # Add the layout constraints
        self.add_constraints()

    def redraw(self):
        self.native.needsDisplay = True

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self.interface.on_resize(width=width, height=height)

    def set_background_color(self, color):
        if color is TRANSPARENT or color is None:
            self.native.backgroundColor = None
        else:
            self.native.backgroundColor = native_color(color)

    # Context management
    def push_context(self, draw_context, **kwargs):
        core_graphics.CGContextSaveGState(draw_context)

    def pop_context(self, draw_context, **kwargs):
        core_graphics.CGContextRestoreGState(draw_context)

    # Basic paths
    def begin_path(self, draw_context, **kwargs):
        core_graphics.CGContextBeginPath(draw_context)

    def close_path(self, draw_context, **kwargs):
        core_graphics.CGContextClosePath(draw_context)

    def move_to(self, x, y, draw_context, **kwargs):
        core_graphics.CGContextMoveToPoint(draw_context, x, y)

    def line_to(self, x, y, draw_context, **kwargs):
        self._ensure_subpath(x, y, draw_context)
        core_graphics.CGContextAddLineToPoint(draw_context, x, y)

    def _ensure_subpath(self, x, y, draw_context):
        if core_graphics.CGContextIsPathEmpty(draw_context):
            self.move_to(x, y, draw_context)

    # Basic shapes

    def bezier_curve_to(
        self,
        cp1x,
        cp1y,
        cp2x,
        cp2y,
        x,
        y,
        draw_context,
        **kwargs,
    ):
        self._ensure_subpath(cp1x, cp1y, draw_context)
        core_graphics.CGContextAddCurveToPoint(
            draw_context, cp1x, cp1y, cp2x, cp2y, x, y
        )

    def quadratic_curve_to(self, cpx, cpy, x, y, draw_context, **kwargs):
        self._ensure_subpath(cpx, cpy, draw_context)
        core_graphics.CGContextAddQuadCurveToPoint(draw_context, cpx, cpy, x, y)

    def arc(
        self,
        x,
        y,
        radius,
        startangle,
        endangle,
        counterclockwise,
        draw_context,
        **kwargs,
    ):
        # Cocoa Box Widget is using a flipped coordinate system, so clockwise
        # is actually counterclockwise
        if counterclockwise:
            clockwise = 1
        else:
            clockwise = 0
        core_graphics.CGContextAddArc(
            draw_context, x, y, radius, startangle, endangle, clockwise
        )

    def ellipse(
        self,
        x,
        y,
        radiusx,
        radiusy,
        rotation,
        startangle,
        endangle,
        counterclockwise,
        draw_context,
        **kwargs,
    ):
        core_graphics.CGContextSaveGState(draw_context)
        self.translate(x, y, draw_context)
        self.rotate(rotation, draw_context)
        if radiusx >= radiusy:
            self.scale(1, radiusy / radiusx, draw_context)
            self.arc(
                0, 0, radiusx, startangle, endangle, counterclockwise, draw_context
            )
        else:
            self.scale(radiusx / radiusy, 1, draw_context)
            self.arc(
                0, 0, radiusy, startangle, endangle, counterclockwise, draw_context
            )
        core_graphics.CGContextRestoreGState(draw_context)

    def rect(self, x, y, width, height, draw_context, **kwargs):
        rectangle = CGRectMake(x, y, width, height)
        core_graphics.CGContextAddRect(draw_context, rectangle)

    # Drawing Paths

    def fill(self, color, fill_rule, draw_context, **kwargs):
        if fill_rule == FillRule.EVENODD:
            mode = CGPathDrawingMode(kCGPathEOFill)
        else:
            mode = CGPathDrawingMode(kCGPathFill)
        core_graphics.CGContextSetRGBFillColor(
            draw_context, color.r / 255, color.g / 255, color.b / 255, color.a
        )
        if not core_graphics.CGContextIsPathEmpty(draw_context):
            path = core_graphics.CGContextCopyPath(draw_context)
            core_graphics.CGContextDrawPath(draw_context, mode)
            core_graphics.CGContextAddPath(draw_context, path)

    def stroke(self, color, line_width, line_dash, draw_context, **kwargs):
        core_graphics.CGContextSetLineWidth(draw_context, line_width)
        mode = CGPathDrawingMode(kCGPathStroke)
        core_graphics.CGContextSetRGBStrokeColor(
            draw_context, color.r / 255, color.g / 255, color.b / 255, color.a
        )
        if line_dash is not None:
            core_graphics.CGContextSetLineDash(
                draw_context, 0, (CGFloat * len(line_dash))(*line_dash), len(line_dash)
            )
        else:
            core_graphics.CGContextSetLineDash(draw_context, 0, None, 0)
        if not core_graphics.CGContextIsPathEmpty(draw_context):
            path = core_graphics.CGContextCopyPath(draw_context)
            core_graphics.CGContextDrawPath(draw_context, mode)
            core_graphics.CGContextAddPath(draw_context, path)

    # Transformations
    def rotate(self, radians, draw_context, **kwargs):
        core_graphics.CGContextRotateCTM(draw_context, radians)

    def scale(self, sx, sy, draw_context, **kwargs):
        core_graphics.CGContextScaleCTM(draw_context, sx, sy)

    def translate(self, tx, ty, draw_context, **kwargs):
        core_graphics.CGContextTranslateCTM(draw_context, tx, ty)

    def reset_transform(self, draw_context, **kwargs):
        # Core Graphics has no built-in ability to assign to or reset the transformation
        # matrix.
        current = core_graphics.CGContextGetCTM(draw_context)

        if current == self.native.original_matrix:
            # No resetting necessary.
            return

        if self.native.using_standard_coords:
            transform = current
        else:
            # The *original* transform matrix isn't the standard identity; this is
            # probably because we're rendering to a cache. So we need to know the
            # transform from what we started with.
            transform = core_graphics.CGAffineTransformConcat(
                current,
                self.native.inverse_original,
            )

        inverse_transform = core_graphics.CGAffineTransformInvert(transform)
        if inverse_transform == transform:
            # When a matrix has no inverse, TransformInvert returns it unchanged.
            warn(
                (
                    "No way to reset transform on macOS if current transform has no "
                    "inverse. Did you scale to 0, perhaps?"
                ),
                RuntimeWarning,
                stacklevel=2,
            )
            return

        core_graphics.CGContextConcatCTM(draw_context, inverse_transform)

    # Text
    def _render_string(self, text, font, **kwargs):
        textAttributes = NSMutableDictionary.alloc().init()
        textAttributes[NSFontAttributeName] = font.native

        if "stroke_color" in kwargs:
            textAttributes[NSStrokeColorAttributeName] = native_color(
                kwargs["stroke_color"]
            )

            # Stroke width is expressed as a percentage of the font size, or a negative
            # percentage to get both stroke and fill.
            stroke_width = kwargs["line_width"] / font.native.pointSize * 100
            if "fill_color" in kwargs:
                stroke_width *= -1
            textAttributes[NSStrokeWidthAttributeName] = stroke_width
        if "fill_color" in kwargs:
            textAttributes[NSForegroundColorAttributeName] = native_color(
                kwargs["fill_color"]
            )

        text_string = NSAttributedString.alloc().initWithString(
            text, attributes=textAttributes
        )
        return text_string

    # Although the native API can measure and draw multi-line strings, this makes the
    # line spacing depend on the scale factor, which messes up the tests.
    def _line_height(self, font, line_height):
        if line_height is None:
            # descender is a negative number.
            return ceil(font.native.ascender - font.native.descender)
        else:
            return font.native.pointSize * line_height

    def measure_text(self, text, font, line_height):
        # We need at least a fill color to render, but that won't change the size.
        sizes = [
            self._render_string(line, font, fill_color=Color.parse(BLACK)).size()
            for line in text.splitlines()
        ]
        return (
            ceil(max(size.width for size in sizes)),
            self._line_height(font, line_height) * len(sizes),
        )

    def write_text(self, text, x, y, font, baseline, line_height, **kwargs):
        lines = text.splitlines()
        scaled_line_height = self._line_height(font, line_height)
        total_height = scaled_line_height * len(lines)

        if baseline == Baseline.TOP:
            top = y + font.native.ascender
        elif baseline == Baseline.MIDDLE:
            top = y + font.native.ascender - (total_height / 2)
        elif baseline == Baseline.BOTTOM:
            top = y + font.native.ascender - total_height
        else:
            # Default to Baseline.ALPHABETIC
            top = y

        for line_num, line in enumerate(lines):
            # Rounding minimizes differences between scale factors.
            origin = NSPoint(round(x), round(top) + (scaled_line_height * line_num))
            rs = self._render_string(line, font, **kwargs)

            # "This method uses the baseline origin by default. If
            # NSStringDrawingUsesLineFragmentOrigin is not specified, the
            # rectangle’s height will be ignored"
            #
            # Previously we used drawAtPoint, which takes a TOP-relative origin. But
            # this often gave off-by-one errors in ALPHABETIC mode, even when we
            # attempted to put the baseline on a logical pixel edge. This may be
            # because drawAtPoint calculates the line height in its own way and then
            # sets the baseline relative to its bottom
            # (https://www.sketch.com/blog/typesetting-in-sketch/), but it would be
            # unwise to rely on that.
            rs.drawWithRect(
                NSRect(origin, NSSize(2**31 - 1, 0)), options=0, context=None
            )

    # Images
    def draw_image(self, image, x, y, width, height, draw_context, **kwargs):
        ns_image = image._impl.native

        # Have an NSImage, need a CGImage
        ns_rectangle = NSRect(NSPoint(0, 0), NSSize(width, height))
        cg_image = ns_image.CGImageForProposedRect(
            ns_rectangle, context=NSGraphicsContext.currentContext, hints=None
        )

        # Quartz is flipped relative to data, so we:
        # - store the current state
        # - translate to bottom of the image
        # - flip vertical axis
        # - draw image at the new y-origin, with normal height
        # - restore state
        core_graphics.CGContextSaveGState(draw_context)
        core_graphics.CGContextTranslateCTM(draw_context, 0, y + height)
        core_graphics.CGContextScaleCTM(draw_context, 1.0, -1.0)
        rectangle = CGRectMake(x, 0, width, height)
        core_graphics.CGContextDrawImage(draw_context, rectangle, cg_image)
        core_graphics.CGContextRestoreGState(draw_context)

    def get_image_data(self):
        bitmap = self.native.bitmapImageRepForCachingDisplayInRect(self.native.bounds)
        self.native.cacheDisplayInRect(self.native.bounds, toBitmapImageRep=bitmap)

        # Get a reference to the CGImage from the bitmap
        cg_image = bitmap.CGImage

        target_size = CGSize(
            core_graphics.CGImageGetWidth(cg_image),
            core_graphics.CGImageGetHeight(cg_image),
        )
        ns_image = NSImage.alloc().initWithCGImage(cg_image, size=target_size)
        return ns_image

    # Rehint
    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.intrinsic.height = at_least(fitting_size.height)
        self.interface.intrinsic.width = at_least(fitting_size.width)
