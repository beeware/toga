from gi.repository import Gtk
import re

try:
    import cairo
except ImportError:
    print("Import 'import cairo' failed; may need to install cairo.")

# TODO import colosseum once updated to support colors
# from colosseum import colors

from .base import Widget


class Canvas(Widget):
    def create(self):
        self.native = Gtk.DrawingArea()
        self.native.set_size_request(640, 480)
        self.native.interface = self.interface
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.native.get_allocated_width(),
                                          self.native.get_allocated_height())
        self.native.context = cairo.Context(surface)

    def set_on_draw(self, handler):
        self.native.connect('draw', handler)

    def set_context(self, context):
        self.native.context = context

    def line_width(self, width=2.0):
        self.native.context.set_line_width(width)

    def fill_style(self, color=None):
        if color is not None:
            num = re.search('^rgba\((\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*)\)$', color)
            if num is not None:
                #  Convert RGB values to be a float between 0 and 1
                r = float(num.group(1)) / 255
                g = float(num.group(2)) / 255
                b = float(num.group(3)) / 255
                a = float(num.group(4))
                self.native.context.set_source_rgba(r, g, b, a)
            else:
                pass
                # Support future colosseum versions
                # for named_color, rgb in colors.NAMED_COLOR.items():
                #     if named_color == color:
                #         exec('self.native.set_source_' + str(rgb))
        else:
            # set color to black
            self.native.context.set_source_rgba(0, 0, 0, 1)

    def stroke_style(self, color=None):
        self.fill_style(color)

    def new_path(self):
        self.native.context.new_path()

    def close_path(self):
        self.native.context.close_path()

    def move_to(self, x, y):
        self.native.context.move_to(x, y)

    def line_to(self, x, y):
        self.native.context.line_to(x, y)

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self.native.context.curve_to(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        # Not supported by cairo.Context
        pass

    def arc(self, x, y, radius, startangle, endangle, anticlockwise):
        if anticlockwise:
            self.native.context.arc_negative(x, y, radius, startangle, endangle)
        else:
            self.native.context.arc(x, y, radius, startangle, endangle)

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise):
        self.native.context.save()
        self.translate(x, y)
        if radiusx >= radiusy:
            self.scale(1, radiusy / radiusx)
            self.arc(0, 0, radiusx, startangle, endangle, anticlockwise)
        elif radiusy > radiusx:
            self.scale(radiusx / radiusy, 1)
            self.arc(0, 0, radiusy, startangle, endangle, anticlockwise)
        self.rotate(rotation)
        self.reset_transform()
        self.native.context.restore()

    def rect(self, x, y, width, height):
        self.native.context.rectangle(x, y, width, height)

    # Drawing Paths

    def fill(self, fill_rule, preserve):
        if fill_rule is 'evenodd':
            self.native.context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        else:
            self.native.context.set_fill_rule(cairo.FILL_RULE_WINDING)
        if preserve:
            self.native.context.fill_preserve()
        else:
            self.native.context.fill()

    def stroke(self):
        self.native.context.stroke()

    # Transformations

    def rotate(self, radians):
        self.native.context.rotate(radians)

    def scale(self, sx, sy):
        self.native.context.scale(sx, sy)

    def translate(self, tx, ty):
        self.native.context.translate(tx, ty)

    def reset_transform(self):
        self.native.context.identity_matrix()

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height(), getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False))
        hints = {}
        width = self.native.get_preferred_width()
        minimum_width = width[0]
        natural_width = width[1]

        height = self.native.get_preferred_height()
        minimum_height = height[0]
        natural_height = height[1]

        if minimum_width > 0:
            hints['min_width'] = minimum_width
        if minimum_height > 0:
            hints['min_height'] = minimum_height
        if natural_height > 0:
            hints['height'] = natural_height

        if hints:
            self.interface.style.hint(**hints)
