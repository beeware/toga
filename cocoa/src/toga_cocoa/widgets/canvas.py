from ctypes import POINTER, c_char, cast

from rubicon.objc import objc_method, objc_property
from travertino.size import at_least

from toga.colors import BLACK, color
from toga.widgets.canvas import FillRule
from toga_cocoa.colors import native_color
from toga_cocoa.libs import (
    CGFloat,
    CGPathDrawingMode,
    CGRectMake,
    NSAttributedString,
    NSBitmapImageFileType,
    NSFontAttributeName,
    NSForegroundColorAttributeName,
    NSGraphicsContext,
    NSMutableDictionary,
    NSPoint,
    NSRect,
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
        self.interface.context._draw(self.impl, draw_context=context)

    @objc_method
    def isFlipped(self) -> bool:
        # Default Cocoa coordinate frame is around the wrong way.
        return True

    @objc_method
    def mouseDown_(self, event) -> None:
        position = self.convertPoint(event.locationInWindow, fromView=None)
        if event.clickCount == 1:
            self.interface.on_press(None, position.x, position.y)
        else:
            self.interface.on_activate(None, position.x, position.y)

    @objc_method
    def rightMouseDown_(self, event) -> None:
        position = self.convertPoint(event.locationInWindow, fromView=None)
        self.interface.on_alt_press(None, position.x, position.y)

    @objc_method
    def mouseUp_(self, event) -> None:
        position = self.convertPoint(event.locationInWindow, fromView=None)
        self.interface.on_release(None, position.x, position.y)

    @objc_method
    def rightMouseUp_(self, event) -> None:
        position = self.convertPoint(event.locationInWindow, fromView=None)
        self.interface.on_alt_release(None, position.x, position.y)

    @objc_method
    def mouseDragged_(self, event) -> None:
        position = self.convertPoint(event.locationInWindow, fromView=None)
        self.interface.on_drag(None, position.x, position.y)

    @objc_method
    def rightMouseDragged_(self, event) -> None:
        position = self.convertPoint(event.locationInWindow, fromView=None)
        self.interface.on_alt_drag(None, position.x, position.y)


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
        if self.interface.window:
            self.interface.on_resize(None, width=width, height=height)

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
        core_graphics.CGContextAddLineToPoint(draw_context, x, y)

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
        core_graphics.CGContextAddCurveToPoint(
            draw_context, cp1x, cp1y, cp2x, cp2y, x, y
        )

    def quadratic_curve_to(self, cpx, cpy, x, y, draw_context, **kwargs):
        core_graphics.CGContextAddQuadCurveToPoint(draw_context, cpx, cpy, x, y)

    def arc(
        self,
        x,
        y,
        radius,
        startangle,
        endangle,
        anticlockwise,
        draw_context,
        **kwargs,
    ):
        # Cocoa Box Widget is using a flipped coordinate system, so clockwise
        # is actually anticlockwise
        if anticlockwise:
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
        anticlockwise,
        draw_context,
        **kwargs,
    ):
        core_graphics.CGContextSaveGState(draw_context)
        self.translate(x, y, draw_context)
        if radiusx >= radiusy:
            self.scale(1, radiusy / radiusx, draw_context)
            self.arc(0, 0, radiusx, startangle, endangle, anticlockwise, draw_context)
        elif radiusy > radiusx:
            self.scale(radiusx / radiusy, 1, draw_context)
            self.arc(0, 0, radiusy, startangle, endangle, anticlockwise, draw_context)
        self.rotate(rotation, draw_context)
        self.reset_transform(draw_context)
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
        if color is not None:
            core_graphics.CGContextSetRGBFillColor(
                draw_context, color.r / 255, color.g / 255, color.b / 255, color.a
            )
        else:
            # Set color to black
            core_graphics.CGContextSetRGBFillColor(draw_context, 0, 0, 0, 1)
        core_graphics.CGContextDrawPath(draw_context, mode)

    def stroke(self, color, line_width, line_dash, draw_context, **kwargs):
        core_graphics.CGContextSetLineWidth(draw_context, line_width)
        mode = CGPathDrawingMode(kCGPathStroke)
        if color is not None:
            core_graphics.CGContextSetRGBStrokeColor(
                draw_context, color.r / 255, color.g / 255, color.b / 255, color.a
            )
        else:
            # Set color to black
            core_graphics.CGContextSetRGBStrokeColor(draw_context, 0, 0, 0, 1)
        if line_dash is not None:
            core_graphics.CGContextSetLineDash(
                draw_context, 0, (CGFloat * len(line_dash))(*line_dash), len(line_dash)
            )
        else:
            core_graphics.CGContextSetLineDash(draw_context, 0, None, 0)
        core_graphics.CGContextDrawPath(draw_context, mode)

    # Transformations
    def rotate(self, radians, draw_context, **kwargs):
        core_graphics.CGContextRotateCTM(draw_context, radians)

    def scale(self, sx, sy, draw_context, **kwargs):
        core_graphics.CGContextScaleCTM(draw_context, sx, sy)

    def translate(self, tx, ty, draw_context, **kwargs):
        core_graphics.CGContextTranslateCTM(draw_context, tx, ty)

    def reset_transform(self, draw_context, **kwargs):
        # Restore the "clean" state of the graphics context.
        core_graphics.CGContextRestoreGState(draw_context)
        # CoreGraphics has a stack-based state representation,
        # so ensure that there is a new, clean version of the "clean"
        # state on the stack.
        core_graphics.CGContextSaveGState(draw_context)

    # Text
    def _render_string(self, text, font, **kwargs):
        textAttributes = NSMutableDictionary.alloc().init()
        textAttributes[NSFontAttributeName] = font.native

        if "stroke_color" in kwargs and "fill_color" in kwargs:
            textAttributes[NSStrokeColorAttributeName] = native_color(
                kwargs["stroke_color"]
            )
            # Apply negative NSStrokeWidthAttributeName to get stroke and fill
            textAttributes[NSStrokeWidthAttributeName] = -1 * kwargs["line_width"]
            textAttributes[NSForegroundColorAttributeName] = native_color(
                kwargs["fill_color"]
            )
        elif "stroke_color" in kwargs:
            textAttributes[NSStrokeColorAttributeName] = native_color(
                kwargs["stroke_color"]
            )
            textAttributes[NSStrokeWidthAttributeName] = kwargs["line_width"]
        elif "fill_color" in kwargs:
            textAttributes[NSForegroundColorAttributeName] = native_color(
                kwargs["fill_color"]
            )
        else:
            raise ValueError("No stroke or fill of write text")

        text_string = NSAttributedString.alloc().initWithString(
            text, attributes=textAttributes
        )
        return text_string

    def measure_text(self, text, font):
        # We need at least a fill color to render, but that won't change the size.
        rendered_string = self._render_string(text, font, fill_color=color(BLACK))
        size = rendered_string.size()
        return size.width, size.height

    def write_text(self, text, x, y, font, **kwargs):
        rendered_string = self._render_string(text, font, **kwargs)
        size = rendered_string.size()
        rendered_string.drawAtPoint(NSPoint(x, y - size.height))

    def get_image_data(self):
        bitmap = self.native.bitmapImageRepForCachingDisplayInRect(self.native.bounds)
        bitmap.setSize(self.native.bounds.size)
        self.native.cacheDisplayInRect(self.native.bounds, toBitmapImageRep=bitmap)

        data = bitmap.representationUsingType(
            NSBitmapImageFileType.PNG,
            properties=None,
        )
        # data is an NSData object that has .bytes as a c_void_p, and a .length. Cast to
        # POINTER(c_char) to get an addressable array of bytes, and slice that array to
        # the known length. We don't use c_char_p because it has handling of NUL
        # termination, and POINTER(c_char) allows array subscripting.
        return cast(data.bytes, POINTER(c_char))[: data.length]

    # Rehint
    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.intrinsic.height = at_least(fitting_size.height)
        self.interface.intrinsic.width = at_least(fitting_size.width)
