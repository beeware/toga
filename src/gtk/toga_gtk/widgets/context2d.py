import gi
try:
    gi.require_foreign("cairo")
except ImportError:
    print("Pycairo integration required for Context2D :(")

# TODO import colosseum once updated to support colors
# from colosseum import colors

from .base import Widget


class Context2D(Widget):
    def create(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 200, 200)
        self.native = cairo.Context(surface)
        # self.native.interface = self.interface

    def save(self):
        self.native.save()

    def restore(self):
        self.native.restore()

    def release(self):
        pass
        # TODO determine how flush the surface
        # surface.flush()
        # surface.finish()

    def line_width(self, width=2.0):
        self.native.set_line_width(width)

    def fill_style(self, color='None', r=0.0, b=0.0, g=0.0, a=1.0):
        if color is not 'None':
            pass
            # Support future colosseum versions
            # for named_color, rgb in colors.NAMED_COLOR.items():
            #     if named_color == color:
            #         exec('self.native.set_source_' + str(rgb))
        else:
            self.native.set_source_rgba(r, g, b, a)

    def stroke_style(self, color='None', r=0.0, b=0.0, g=0.0, a=1.0):
        self.fill_style(color)

    def begin_path(self):
        self.native.new_sub_path()

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
