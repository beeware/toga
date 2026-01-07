from math import ceil

from rubicon.objc import CGSize, objc_method, objc_property
from travertino.size import at_least

from toga.colors import BLACK, TRANSPARENT, Color
from toga.constants import Baseline, FillRule
from toga_cocoa.colors import native_color
from toga_cocoa.libs import (
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


class Context:
    def __init__(self):
        self.cg_context = NSGraphicsContext.currentContext.CGContext
        self.set_line_width(2.0)

    # Context management
    def save(self):
        core_graphics.CGContextSaveGState(self.cg_context)

    def restore(self):
        core_graphics.CGContextRestoreGState(self.cg_context)

    # Setting attributes
    def set_fill_style(self, color):
        core_graphics.CGContextSetRGBFillColor(
            self.cg_context, color.r / 255, color.g / 255, color.b / 255, color.a
        )

    def set_line_dash(self, line_dash):
        core_graphics.CGContextSetLineDash(
            self.cg_context,
            0,
            (CGFloat * len(line_dash))(*line_dash),
            len(line_dash),
        )

    def set_line_width(self, line_width):
        core_graphics.CGContextSetLineWidth(self.cg_context, line_width)

    def set_stroke_style(self, color):
        core_graphics.CGContextSetRGBStrokeColor(
            self.cg_context, color.r / 255, color.g / 255, color.b / 255, color.a
        )

    # Basic paths
    def begin_path(self):
        core_graphics.CGContextBeginPath(self.cg_context)

    def close_path(self):
        core_graphics.CGContextClosePath(self.cg_context)

    def move_to(self, x, y):
        core_graphics.CGContextMoveToPoint(self.cg_context, x, y)

    def line_to(self, x, y):
        self._ensure_subpath(x, y)
        core_graphics.CGContextAddLineToPoint(self.cg_context, x, y)

    def _ensure_subpath(self, x, y):
        if core_graphics.CGContextIsPathEmpty(self.cg_context):
            self.move_to(x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self._ensure_subpath(cp1x, cp1y)
        core_graphics.CGContextAddCurveToPoint(
            self.cg_context, cp1x, cp1y, cp2x, cp2y, x, y
        )

    def quadratic_curve_to(self, cpx, cpy, x, y):
        self._ensure_subpath(cpx, cpy)
        core_graphics.CGContextAddQuadCurveToPoint(self.cg_context, cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle, endangle, counterclockwise):
        # Cocoa Box Widget is using a flipped coordinate system, so clockwise
        # is actually counterclockwise
        if counterclockwise:
            clockwise = 1
        else:
            clockwise = 0
        core_graphics.CGContextAddArc(
            self.cg_context, x, y, radius, startangle, endangle, clockwise
        )

    def ellipse(
        self, x, y, radiusx, radiusy, rotation, startangle, endangle, counterclockwise
    ):
        self.save()
        self.translate(x, y)
        self.rotate(rotation)
        if radiusx >= radiusy:
            self.scale(1, radiusy / radiusx)
            self.arc(0, 0, radiusx, startangle, endangle, counterclockwise)
        else:
            self.scale(radiusx / radiusy, 1)
            self.arc(0, 0, radiusy, startangle, endangle, counterclockwise)
        self.restore()

    def rect(self, x, y, width, height):
        rectangle = CGRectMake(x, y, width, height)
        core_graphics.CGContextAddRect(self.cg_context, rectangle)

    # Drawing Paths

    def fill(self, fill_rule):
        if fill_rule == FillRule.EVENODD:
            mode = CGPathDrawingMode(kCGPathEOFill)
        else:
            mode = CGPathDrawingMode(kCGPathFill)
        if not core_graphics.CGContextIsPathEmpty(self.cg_context):
            path = core_graphics.CGContextCopyPath(self.cg_context)
            core_graphics.CGContextDrawPath(self.cg_context, mode)
            core_graphics.CGContextAddPath(self.cg_context, path)

    def stroke(self):
        mode = CGPathDrawingMode(kCGPathStroke)
        if not core_graphics.CGContextIsPathEmpty(self.cg_context):
            path = core_graphics.CGContextCopyPath(self.cg_context)
            core_graphics.CGContextDrawPath(self.cg_context, mode)
            core_graphics.CGContextAddPath(self.cg_context, path)

    # Transformations
    def rotate(self, radians):
        core_graphics.CGContextRotateCTM(self.cg_context, radians)

    def scale(self, sx, sy):
        core_graphics.CGContextScaleCTM(self.cg_context, sx, sy)

    def translate(self, tx, ty):
        core_graphics.CGContextTranslateCTM(self.cg_context, tx, ty)

    def reset_transform(self):
        # Restore the "clean" state of the graphics context.
        core_graphics.CGContextRestoreGState(self.cg_context)
        # CoreGraphics has a stack-based state representation,
        # so ensure that there is a new, clean version of the "clean"
        # state on the stack.
        core_graphics.CGContextSaveGState(self.cg_context)

    # Text
    def write_text(self, text, x, y, font, baseline, line_height):
        lines = text.splitlines()
        scaled_line_height = _line_height(font, line_height)
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
            rs = _render_string(line, font)

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


class TogaCanvas(NSView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def drawRect_(self, rect: NSRect) -> None:
        self.interface.context._draw(Context())

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

    def measure_text(self, text, font, line_height):
        # We need at least a fill color to render, but that won't change the size.
        sizes = [
            _render_string(line, font, fill_color=Color.parse(BLACK)).size()
            for line in text.splitlines()
        ]
        return (
            ceil(max(size.width for size in sizes)),
            _line_height(font, line_height) * len(sizes),
        )

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
