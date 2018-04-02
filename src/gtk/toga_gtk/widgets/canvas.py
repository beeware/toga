import re

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
try:
    import cairo
except ImportError:
    cairo = None
try:
    gi.require_version("Pango", "1.0")
    from gi.repository import Pango
    scale = Pango.SCALE
except ImportError:
    scale = 1024

# TODO import colosseum once updated to support colors
# from colosseum import colors

from .base import Widget


class Canvas(Widget):
    def create(self):
        if cairo is None:
            raise RuntimeError(
                "'import cairo' failed; may need to install python-gi-cairo."
            )

        self.native = Gtk.DrawingArea()
        self.native.interface = self.interface
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.native.get_allocated_width(),
                                          self.native.get_allocated_height())
        self.native_context = cairo.Context(self.surface)
        self.context_root = None
        self.native.connect('draw', self.draw_callback)
        self.native.font = None

    def context(self):
        pass

    def set_context_root(self, context_root):
        self.context_root = context_root

    def draw_callback(self, canvas, context):
        self.native_context = context
        for drawing_object in traverse(self.context_root):
            drawing_object(self)

    # Basic paths

    def new_path(self):
        self.native_context.new_path()

    def closed_path(self):
        self.native_context.close_path()

    def move_to(self, x, y):
        self.native_context.move_to(x, y)

    def line_to(self, x, y):
        self.native_context.line_to(x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self.native_context.curve_to(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y):
        self.native_context.curve_to(cpx, cpy, cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise):
        if anticlockwise:
            self.native_context.arc_negative(x, y, radius, startangle, endangle)
        else:
            self.native_context.arc(x, y, radius, startangle, endangle)

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise):
        self.native_context.save()
        self.translate(x, y)
        if radiusx >= radiusy:
            self.scale(1, radiusy / radiusx)
            self.arc(0, 0, radiusx, startangle, endangle, anticlockwise)
        elif radiusy > radiusx:
            self.scale(radiusx / radiusy, 1)
            self.arc(0, 0, radiusy, startangle, endangle, anticlockwise)
        self.rotate(rotation)
        self.reset_transform()
        self.native_context.restore()

    def rect(self, x, y, width, height):
        self.native_context.rectangle(x, y, width, height)

    # Drawing Paths

    def set_color(self, color=None):
        if color is not None:
            num = re.search('^rgba\((\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*)\)$', color)
            if num is not None:
                #  Convert RGB values to be a float between 0 and 1
                r = float(num.group(1)) / 255
                g = float(num.group(2)) / 255
                b = float(num.group(3)) / 255
                a = float(num.group(4))
                self.native_context.set_source_rgba(r, g, b, a)
            else:
                pass
                # Support future colosseum versions
                # for named_color, rgb in colors.NAMED_COLOR.items():
                #     if named_color == color:
                #         exec('self.native.set_source_' + str(rgb))
        else:
            # set color to black
            self.native_context.set_source_rgba(0, 0, 0, 1)

    def fill(self, color, fill_rule, preserve):
        self.set_color(color)
        if fill_rule is 'evenodd':
            self.native_context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        else:
            self.native_context.set_fill_rule(cairo.FILL_RULE_WINDING)
        if preserve:
            self.native_context.fill_preserve()
        else:
            self.native_context.fill()

    def stroke(self, color, line_width):
        self.set_color(color)
        self.native_context.set_line_width(line_width)
        self.native_context.stroke()

    # Transformations

    def rotate(self, radians):
        self.native_context.rotate(radians)

    def scale(self, sx, sy):
        self.native_context.scale(sx, sy)

    def translate(self, tx, ty):
        self.native_context.translate(tx, ty)

    def reset_transform(self):
        self.native_context.identity_matrix()

    # Text

    def write_text(self, text, x, y, font):
        # Set font family and size
        if font:
            write_font = font
        elif self.native.font:
            write_font = self.native.font
            write_font.family = self.native.font.get_family()
            write_font.size = self.native.font.get_size() / scale
        self.native_context.select_font_face(write_font.family)
        self.native_context.set_font_size(write_font.size)

        # Support writing multiline text
        for line in text.splitlines():
            width, height = write_font.measure(line)
            self.native_context.move_to(x, y)
            self.native_context.text_path(line)
            y += height

    def measure_text(self, text, font):
        # Set font family and size
        if font:
            self.native_context.select_font_face(font.family)
            self.native_context.set_font_size(font.size)
        elif self.native.font:
            self.native_context.select_font_face(self.native.font.get_family())
            self.native_context.set_font_size(self.native.font.get_size() / scale)

        x_bearing, y_bearing, width, height, x_advance, y_advance = self.native_context.text_extents(text)
        return width, height

    # Rehint

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()


def traverse(nested_list):
    if isinstance(nested_list, list):
        for drawing_object in nested_list:
            for subdrawing_object in traverse(drawing_object):
                yield subdrawing_object
    else:
        yield nested_list
