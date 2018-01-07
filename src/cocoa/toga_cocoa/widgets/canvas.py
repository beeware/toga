import re

from rubicon.objc import objc_method, SEL

# TODO import colosseum once updated to support colors
# from colosseum import colors

from toga_cocoa.libs import *
from .base import Widget


class TogaCanvas(NSView):
    @objc_method
    def drawRect_(self, rect: NSRect) -> None:
        if self.interface.on_draw:
            self.interface.on_draw(self.interface, NSGraphicsContext.currentContext)


class Canvas(Widget):
    def create(self):
        self.native = TogaCanvas.alloc().init()
        self.native.context = NSGraphicsContext.currentContext
        self.native.interface = self.interface

        self.native.target = self.native
        self.native.action = SEL('onDraw:')

        # Add the layout constraints
        self.add_constraints()

    def set_on_draw(self, handler):
        pass

    def set_context(self, context):
        core_graphics = context

    def line_width(self, width=1.0):
        core_graphics.CGContextSetLineWidth(self.native.context, width)

    def fill_style(self, color=None):
        if color is not None:
            num = re.search('^rgba\((\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*)\)$', color)
            if num is not None:
                #  Convert RGB values to be a float between 0 and 1
                r = float(num.group(1)) / 255
                g = float(num.group(2)) / 255
                b = float(num.group(3)) / 255
                a = float(num.group(4))
                core_graphics.CGContextSetRGBFillColor(self.native.context, r, g, b, a)
            else:
                pass
                # Support future colosseum versions
                # for named_color, rgb in colors.NAMED_COLOR.items():
                #     if named_color == color:
                #         exec('self.native.set_source_' + str(rgb))
        else:
            # set color to black
            core_graphics.CGContextSetRGBFillColor(self.native.context, 0, 0, 0, 1)

    def stroke_style(self, color=None):
        if color is not None:
            num = re.search('^rgba\((\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*)\)$', color)
            if num is not None:
                #  Convert RGB values to be a float between 0 and 1
                r = float(num.group(1)) / 255
                g = float(num.group(2)) / 255
                b = float(num.group(3)) / 255
                a = float(num.group(4))
                core_graphics.CGContextSetRGBStrokeColor(self.native.context, r, g, b, a)
            else:
                pass
                # Support future colosseum versions
                # for named_color, rgb in colors.NAMED_COLOR.items():
                #     if named_color == color:
                #         exec('self.native.set_source_' + str(rgb))
        else:
            # set color to black
            core_graphics.CGContextSetRGBStrokeColor(self.native.context, 0, 0, 0, 1)

    def new_path(self):
        core_graphics.CGContextBeginPath(self.native.context)

    def close_path(self):
        core_graphics.CGContextClosePath(self.native.context)

    def move_to(self, x, y):
        core_graphics.CGContextMoveToPoint(self.native.context, x, y)

    def line_to(self, x, y):
        core_graphics.CGContextAddLineToPoint(self.native.context, x, y)

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        core_graphics.CGContextAddCurveToPoint(self.native.context, cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        core_graphics.CGContextAddQuadCurveToPoint(self.native.context, cpx, cpy, cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise):
        if anticlockwise:
            clockwise = 0
        else:
            clockwise = 1
        core_graphics.CGContextAddArc(self.native.context, x, y, radius, startangle, endangle, clockwise)

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise):
        core_graphics.CGContextSaveGState(self.native.context)
        self.translate(x, y)
        if radiusx >= radiusy:
            self.scale(1, radiusy / radiusx)
            self.arc(0, 0, radiusx, startangle, endangle, anticlockwise)
        elif radiusy > radiusx:
            self.scale(radiusx / radiusy, 1)
            self.arc(0, 0, radiusy, startangle, endangle, anticlockwise)
        self.rotate(rotation)
        self.reset_transform()
        core_graphics.CGContextRestoreGState(self.native.context)

    def rect(self, x, y, width, height):
        rectangle = CGRectMake(x, y, width, height)
        core_graphics.CGContextAddRect(self.native.context, rectangle)

    # Drawing Paths

    def fill(self, fill_rule, preserve):
        if fill_rule is 'evenodd':
            mode = CGPathDrawingMode(kCGPathEOFill)
        else:
            mode = CGPathDrawingMode(kCGPathFill)
        core_graphics.CGContextDrawPath(self.native.context, mode)

    def stroke(self):
        mode = CGPathDrawingMode(kCGPathStroke)
        core_graphics.CGContextDrawPath(self.native.context, mode)

    # Transformations

    def rotate(self, radians):
        core_graphics.CGContextRotateCTM(self.native.context, radians)

    def scale(self, sx, sy):
        core_graphics.CGContextScaleCTM(self.native.context, sx, sy)

    def translate(self, tx, ty):
        core_graphics.CGContextTranslateCTM(self.native.context, tx, ty)

    def reset_transform(self):
        pass

    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.intrinsic.height = fitting_size.height
        self.interface.intrinsic.width = fitting_size.width
