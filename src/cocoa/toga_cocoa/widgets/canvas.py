from toga_cocoa.libs import (
    core_found,
    core_graphics,
    core_text,
    CGPathDrawingMode,
    CGRectMake,
    CFRange,
    kCGPathStroke,
    kCGPathEOFill,
    kCGPathFill,
    NSGraphicsContext,
    NSAffineTransform,
    NSPoint,
    NSView,
    NSRect,
    objc_method,
)

from .base import Widget


class TogaCanvas(NSView):
    @objc_method
    def drawRect_(self, rect: NSRect) -> None:
        context = NSGraphicsContext.currentContext.graphicsPort()

        # Flip the coordinate system back to normal (unflipped)
        if self.isFlipped:
            xform = NSAffineTransform.transform()
            xform.translateXBy(0.0, yBy=rect.size.height)
            xform.scaleXBy(1.0, yBy=-1.0)
            xform.concat()

        if self.interface.redraw:
            self.interface._draw(self._impl, draw_context=context)


class Canvas(Widget):
    def create(self):
        self.native = TogaCanvas.alloc().init()
        self.native.interface = self.interface
        self.native._impl = self

        # Add the layout constraints
        self.add_constraints()

    def redraw(self):
        pass

    # Basic paths

    def new_path(self, draw_context):
        core_graphics.CGContextBeginPath(draw_context)

    def closed_path(self, x, y, draw_context):
        core_graphics.CGContextClosePath(draw_context)

    def move_to(self, x, y, draw_context):
        core_graphics.CGContextMoveToPoint(draw_context, x, y)

    def line_to(self, x, y, draw_context):
        core_graphics.CGContextAddLineToPoint(draw_context, x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, draw_context):
        core_graphics.CGContextAddCurveToPoint(
            draw_context, cp1x, cp1y, cp2x, cp2y, x, y
        )

    def quadratic_curve_to(self, cpx, cpy, x, y, draw_context):
        core_graphics.CGContextAddQuadCurveToPoint(draw_context, cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise, draw_context):
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
        self.reset_transform(draw_context)  # TODO Reset transform is not implemented
        core_graphics.CGContextRestoreGState(draw_context)

    def rect(self, x, y, width, height, draw_context):
        rectangle = CGRectMake(x, y, width, height)
        core_graphics.CGContextAddRect(draw_context, rectangle)

    # Drawing Paths

    def fill(self, color, fill_rule, preserve, draw_context):
        if fill_rule is "evenodd":
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

    def stroke(self, color, line_width, draw_context):
        core_graphics.CGContextSetLineWidth(draw_context, line_width)
        mode = CGPathDrawingMode(kCGPathStroke)
        if color is not None:
            core_graphics.CGContextSetRGBStrokeColor(
                draw_context, color.r / 255, color.g / 255, color.b / 255, color.a
            )
        else:
            pass
            # Set color to black
            core_graphics.CGContextSetRGBStrokeColor(draw_context, 0, 0, 0, 1)
        core_graphics.CGContextDrawPath(draw_context, mode)

    # Transformations

    def rotate(self, radians, draw_context):
        core_graphics.CGContextRotateCTM(draw_context, radians)

    def scale(self, sx, sy, draw_context):
        core_graphics.CGContextScaleCTM(draw_context, sx, sy)

    def translate(self, tx, ty, draw_context):
        core_graphics.CGContextTranslateCTM(draw_context, tx, ty)

    def reset_transform(self, draw_context):
        pass

    # Text

    def write_text(self, text, x, y, font, draw_context):
        # Set font family and size
        if font:
            write_font = font
        elif self.native.font:
            write_font = self.native.font
        else:
            raise ValueError("No font to write with")

        # Flip the coordinate system for text drawing
        flip = core_graphics.CGAffineTransformMakeScale(1, -1)
        core_graphics.CGContextSetTextMatrix(draw_context, flip)

        text_string = write_font.create_string(text)
        frame_setter = core_text.CTFramesetterCreateWithAttributedString(text_string)
        width, height = font.measure(text)
        rect = CGRectMake(x, y, width, height)
        path = core_graphics.CGPathCreateWithRect(rect, None)
        cf_range = CFRange(0, 0)
        frame = core_text.CTFramesetterCreateFrame(
            frame_setter, cf_range, path, None
        )
        lines = core_text.CTFrameGetLines(frame)
        line_count = core_found.CFArrayGetCount(lines)
        line_origins = (NSPoint * line_count)()
        core_text.CTFrameGetLineOrigins(frame, cf_range, line_origins)
        for c in range(line_count):
            line = core_found.CFArrayGetValueAtIndex(lines, c)
            core_graphics.CGContextSetTextPosition(
                draw_context, x + line_origins[c].x, y + line_origins[c].y
            )
            core_text.CTLineDraw(line, draw_context)

        # Cleanup
        core_found.CFRelease(frame)
        core_found.CFRelease(path)
        core_found.CFRelease(frame_setter)
        core_found.CFRelease(text_string)

    # Rehint

    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.intrinsic.height = fitting_size.height
        self.interface.intrinsic.width = fitting_size.width
