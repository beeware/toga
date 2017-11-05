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
        self.native.interface = self.interface
        self.native.connect('show', lambda event: self.rehint())

    def draw(self, draw_func):
        self.native.connect('draw', draw_func)
        yield

    def save(self):
        self.native.save()

    def restore(self):
        self.native.restore()

    def line_width(self, width=2.0):
        self.native.set_line_width(width)

    def fill_style(self, color=None):
        if color is not None:
            num = re.search('^rgba\((\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*)\)$', color)
            if num is not None:
                r = num.group(1)
                g = num.group(2)
                b = num.group(3)
                a = num.group(4)
                self.native.set_source_rgba(r, b, g, a)
            else:
                pass
                # Support future colosseum versions
                # for named_color, rgb in colors.NAMED_COLOR.items():
                #     if named_color == color:
                #         exec('self.native.set_source_' + str(rgb))
        else:
            # set color to black
            self.native.set_source_rgba(0, 0, 0, 1)

    def stroke_style(self, color=None):
        self.fill_style(color)

    def close_path(self):
        self.native.close_path()

    def move_to(self, x, y):
        self.native.move_to(x, y)

    def line_to(self, x, y):
        self.native.line_to(x, y)

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self.native.curve_to(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        # Not supported by cairo.Context
        pass

    def arc(self, x, y, radius, startangle, endangle, anticlockwise):
        if anticlockwise:
            self.native.arc_negative(x, y, radius, startangle, endangle)
        else:
            self.native.arc(x, y, radius, startangle, endangle)

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise):
        width = 2 * radiusx
        height = 2 * radiusy
        self.save()
        self.translate(x + width / 2, y + height / 2)
        self.scale(width / 2, height / 2)
        self.rotate(rotation)
        self.arc(x, y, 1, startangle, endangle, anticlockwise)
        self.restore()

    def rect(self, x, y, width, height):
        self.native.rectangle(x, y, width, height)

    # Drawing Paths

    def fill(self, fill_rule, preserve):
        if fill_rule is 'evenodd':
            cairo.Context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        else:
            cairo.Context.set_fill_rule(cairo.FILL_RULE_WINDING)
        if preserve:
            self.native.fill_preserve()
        else:
            self.native.fill()

    def stroke(self):
        self.native.stroke()

    # Transformations

    def rotate(self, radians):
        self.native.rotate(radians)

    def scale(self, sx, sy):
        self.native.scale(sx, sy)

    def translate(self, tx, ty):
        self.native.translate(tx, ty)

    def reset_transform(self):
        self.native.identity_matrix()

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
