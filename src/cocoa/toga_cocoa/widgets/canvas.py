import re

from rubicon.objc import objc_method, SEL

# TODO import colosseum once updated to support colors
# from colosseum import colors

from toga_cocoa.libs import *
from .base import Widget


class TogaCanvas(NSGraphicsContext):
    @objc_method
    def onDraw_(self, obj) -> None:
        if self.interface.on_draw:
            self.interface.on_draw(self.interface)


class Canvas(Widget):
    def create(self):
        self.native = TogaCanvas.alloc().init()
        self.native.interface = self.interface

        self.native.target = self.native
        self.native.action = SEL('onDraw:')

        # Add the layout constraints
        self.add_constraints()

    def set_on_draw(self, handler):
        pass

    def set_context(self, context):
        self.native = context

    def line_width(self, width=1.0):
        self.native.CGContextSetLineWidth(width)

    def fill_style(self, color=None):
        if color is not None:
            num = re.search('^rgba\((\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*)\)$', color)
            if num is not None:
                #  Convert RGB values to be a float between 0 and 1
                r = float(num.group(1)) / 255
                g = float(num.group(2)) / 255
                b = float(num.group(3)) / 255
                a = float(num.group(4))
                self.native.CGContextSetRGBFillColor(r, g, b, a)
            else:
                pass
                # Support future colosseum versions
                # for named_color, rgb in colors.NAMED_COLOR.items():
                #     if named_color == color:
                #         exec('self.native.set_source_' + str(rgb))
        else:
            # set color to black
            self.native.CGContextSetRGBFillColor(0, 0, 0, 1)

    def stroke_style(self, color=None):
        if color is not None:
            num = re.search('^rgba\((\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*)\)$', color)
            if num is not None:
                #  Convert RGB values to be a float between 0 and 1
                r = float(num.group(1)) / 255
                g = float(num.group(2)) / 255
                b = float(num.group(3)) / 255
                a = float(num.group(4))
                self.native.CGContextSetRGBStrokeColor(r, g, b, a)
            else:
                pass
                # Support future colosseum versions
                # for named_color, rgb in colors.NAMED_COLOR.items():
                #     if named_color == color:
                #         exec('self.native.set_source_' + str(rgb))
        else:
            # set color to black
            self.native.CGContextSetRGBStrokeColor(0, 0, 0, 1)

    def new_path(self):
        self.native.CGContextBeginPath()

    def close_path(self):
        self.native.CGContextClosePath()

    def move_to(self, x, y):
        self.native.CGContextMoveToPoint(x, y)

    def line_to(self, x, y):
        self.native.CGContextAddLineToPoint(x, y)

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self.native.CGContextAddCurveToPoint(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        self.native.CGContextAddQuadCurveToPoint(cpx, cpy, cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise):
        if anticlockwise:
            clockwise = 0
        else:
            clockwise = 1
        self.native.CGContextAddArc(x, y, radius, startangle, endangle, clockwise)

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise):
        self.native.CGContextSaveGState()
        self.translate(x, y)
        if radiusx >= radiusy:
            self.scale(1, radiusy / radiusx)
            self.arc(0, 0, radiusx, startangle, endangle, anticlockwise)
        elif radiusy > radiusx:
            self.scale(radiusx / radiusy, 1)
            self.arc(0, 0, radiusy, startangle, endangle, anticlockwise)
        self.rotate(rotation)
        self.reset_transform()
        self.native.CGContextRestoreGState()

    def rect(self, x, y, width, height):
        rectangle = self.native.CGMakeRect(x, y, width, height)
        self.native.CGContextAddRect(rectangle)

    # Drawing Paths

    def fill(self, fill_rule, preserve):
        if fill_rule is 'evenodd':
            mode = self.native.CGPathDrawingMode(kCGPathEOFill)
        else:
            mode = self.native.CGPathDrawingMode(kCGPathFill)
        self.native.CGContextDrawPath(mode)

    def stroke(self):
        mode = self.native.CGPathDrawingMode(kCGPathStroke)
        self.native.CGContextDrawPath(mode)

    # Transformations

    def rotate(self, radians):
        self.native.CGContextRotateCTM(radians)

    def scale(self, sx, sy):
        self.native.CGContextScaleCTM(sx, sy)

    def translate(self, tx, ty):
        self.native.CGContextTranslateCTM(tx, ty)

    def reset_transform(self):
        pass

    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
