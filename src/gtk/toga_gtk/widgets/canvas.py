import re
from collections import defaultdict

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

    SCALE = Pango.SCALE
except ImportError:
    SCALE = 1024

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
        self.context_dict = {}
        self.set_context('default')
        self.draw_stack = self.context_dict['default']
        print(self.draw_stack)
        self.native.connect('draw', self.draw_all_contexts)
        self.native.font = None

    def draw_all_contexts(self, canvas, context):
        print("Start to draw")
        self.native.context = context
        print(self.context_dict)
        for context, draw_stack in self.context_dict.items():
            print(draw_stack)
            for draw_operation in draw_stack:
                draw_operation()
                print("draw op")

    def set_context(self, context):
        if context:
            for context in self.context_dict:
                print("Set context", context)
                self.draw_stack = self.context_dict[context]
            else:
                print("Create context", context)
                self.context_dict[context] = []
                self.draw_stack = self.context_dict[context]
                print(self.draw_stack)
        else:
            print("No context provided")

    def append_to_draw_stack(self, method):
        print("Append", method)
        self.draw_stack.append(method)

    def remove_from_draw_stack(self, method):
        self.draw_stack.remove(method)

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
        self.native.context.curve_to(cpx, cpy, cpx, cpy, x, y)

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

    def write_text(self, text, x, y, font):
        # Set font family and size
        if font:
            write_font = font
        elif self.native.font:
            write_font = self.native.font
            write_font.family = self.native.font.get_family()
            write_font.size = self.native.font.get_size() / SCALE
        self.native.context.select_font_face(write_font.family)
        self.native.context.set_font_size(write_font.size)

        # Support writing multiline text
        for line in text.splitlines():
            width, height = write_font.measure(line)
            self.native.context.move_to(x, y)
            self.native.context.text_path(line)
            y += height

    def measure_text(self, text, font):
        # Set font family and size
        if font:
            self.native.context.select_font_face(font.family)
            self.native.context.set_font_size(font.size)
        elif self.native.font:
            self.native.context.select_font_face(self.native.font.get_family())
            self.native.context.set_font_size(self.native.font.get_size() / SCALE)

        x_bearing, y_bearing, width, height, x_advance, y_advance = self.native.context.text_extents(text)
        return width, height

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()
