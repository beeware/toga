from rubicon.objc import objc_method, SEL, ObjCInstance
from toga_cocoa.libs import *

from .base import Widget
from ..color import native_color


class TogaCanvas(NSView):
    @objc_method
    def drawRect_(self, rect: NSRect) -> None:
        context = NSGraphicsContext.currentContext.graphicsPort()

        # Flip the coordinate system back to normal (unflipped)
        xform = NSAffineTransform.transform()
        xform.translateXBy(0.0, yBy=rect.size.height)
        xform.scaleXBy(1.0, yBy=-1.0)
        xform.concat()

        if self.interface.on_draw:
            self.interface.on_draw(self.interface, context)


class Canvas(Widget):
    def create(self):
        self.native = TogaCanvas.alloc().init()
        self.native.interface = self.interface

        self.context = NSGraphicsContext.currentContext

        self.native.target = self.native
        self.native.action = SEL("onDraw:")

        # Add the layout constraints
        self.add_constraints()

    def redraw(self):
        self.interface.draw(self)

    # Basic paths

    def new_path(self):
        core_graphics.CGContextBeginPath(self.context)

    def closed_path(self, x, y):
        core_graphics.CGContextClosePath(self.context)

    def move_to(self, x, y):
        core_graphics.CGContextMoveToPoint(self.context, x, y)

    def line_to(self, x, y):
        core_graphics.CGContextAddLineToPoint(self.context, x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        core_graphics.CGContextAddCurveToPoint(
            self.context, cp1x, cp1y, cp2x, cp2y, x, y
        )

    def quadratic_curve_to(self, cpx, cpy, x, y):
        core_graphics.CGContextAddQuadCurveToPoint(self.context, cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise):
        # Cocoa Box Widget is using a flipped coordinate system, so clockwise
        # is actually anticlockwise
        if anticlockwise:
            clockwise = 1
        else:
            clockwise = 0
        core_graphics.CGContextAddArc(
            self.context, x, y, radius, startangle, endangle, clockwise
        )

    def ellipse(
        self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise
    ):
        core_graphics.CGContextSaveGState(self.context)
        self.translate(x, y)
        if radiusx >= radiusy:
            self.scale(1, radiusy / radiusx)
            self.arc(0, 0, radiusx, startangle, endangle, anticlockwise)
        elif radiusy > radiusx:
            self.scale(radiusx / radiusy, 1)
            self.arc(0, 0, radiusy, startangle, endangle, anticlockwise)
        self.rotate(rotation)
        self.reset_transform()  # TODO Reset transform is not implemented
        core_graphics.CGContextRestoreGState(self.context)

    def rect(self, x, y, width, height):
        rectangle = CGRectMake(x, y, width, height)
        core_graphics.CGContextAddRect(self.context, rectangle)

    # Drawing Paths

    def fill(self, color, fill_rule, preserve):
        if fill_rule is "evenodd":
            mode = CGPathDrawingMode(kCGPathEOFill)
        else:
            mode = CGPathDrawingMode(kCGPathFill)
        if color is not None:
            core_graphics.CGContextSetRGBFillColor(self.context, *native_color(color))
        else:
            # Set color to black
            core_graphics.CGContextSetRGBFillColor(self.context, 0, 0, 0, 1)
        core_graphics.CGContextDrawPath(self.context, mode)

    def stroke(self, color, line_width):
        core_graphics.CGContextSetLineWidth(self.context, line_width)
        mode = CGPathDrawingMode(kCGPathStroke)
        if color is not None:
            core_graphics.CGContextSetRGBStrokeColor(self.context, *native_color(color))
        else:
            # Set color to black
            core_graphics.CGContextSetRGBStrokeColor(self.context, 0, 0, 0, 1)
        core_graphics.CGContextDrawPath(self.context, mode)

    # Transformations

    def rotate(self, radians):
        core_graphics.CGContextRotateCTM(self.context, radians)

    def scale(self, sx, sy):
        core_graphics.CGContextScaleCTM(self.context, sx, sy)

    def translate(self, tx, ty):
        core_graphics.CGContextTranslateCTM(self.context, tx, ty)

    def reset_transform(self):
        pass

    # Text

    def measure_text(self, text, font):
        # Set font family and size
        if font:
            meas_font = font
        elif self.native.font:
            meas_font = self.native.font
        else:
            raise ValueError("No font to measure with")

        font_attrs = {NSFontAttributeName: meas_font}

        # The double ObjCInstance wrapping is workaround for rubicon since it
        # doesn't yet provide an ObjCStringInstance
        text_string = ObjCInstance(
            ObjCInstance(NSString.alloc(convert_result=False)).initWithString_(
                text, convert_result=False
            )
        )

        size = text_string.sizeWithAttributes(font_attrs)
        return size.width, size.height

    def write_text(self, text, x, y, font):
        # Set font family and size
        if font:
            write_font = font
        elif self.native.font:
            write_font = self.native.font
        else:
            raise ValueError("No font to write with")

        core_graphics.CGContextSelectFont(
            self.context, write_font.family, write_font.size, kCGEncodingFontSpecific
        )
        # core_graphics.CGContextSetTextDrawingMode(self.context, kCGTextFillStroke)

        # Support writing multiline text
        for line in text.splitlines():
            width, height = write_font.measure(line)
            core_graphics.CGContextShowTextAtPoint(self.context, x, y, line, len(line))
            y += height

    # Rehint

    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.intrinsic.height = fitting_size.height
        self.interface.intrinsic.width = fitting_size.width
