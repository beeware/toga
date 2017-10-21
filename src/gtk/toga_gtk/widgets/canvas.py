from gi.repository import Gtk
import cairo
from .base import Widget


class Canvas(Widget):
    def create(self):
        self.native = Gtk.DrawingArea()
        self.native.interface = self.interface


class Context2D(Widget):
    def create(self):
        self.native = cairo.Context()
        self.native.interface = self.interface

    def save(self):
        self.native.save()

    def restore(self):
        self.native.restore()

    def line_width(self, width=2.0):
        self.native.set_line_width(width)

    def fill_style(self, color='black'):
        self.native.set_source_rgba(color)

    def stroke_style(self, color='black'):
        self.native.set_source_rgba(color)

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


class Matrix(Widget):
    def create(self):
        self.native = cairo.Matrix()
        self.native.interface = self.interface

    def transform_point(self, x, y):
        return self.native.transform_point(x, y)
