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
        self.context_dict = defaultdict(list)
        self.set_context('default')
        self.native_context, self.draw_stack = self.context_dict['default']
        self.native.connect('draw', self.draw_all_contexts)
        self.native.font = None

    def set_on_draw(self, handler):
        self.native.connect('draw', handler)

    def create_context_values(self):
        self.native_context = cairo.Context(self.surface)
        draw_stack = []
        return [self.native_context, draw_stack]

    def draw_all_contexts(self):
        for context, context_values in self.context_dict.items():
            self.native_context, draw_stack = context_values
            for draw_operation in draw_stack:
                draw_operation()

    def set_context(self, context):
        if context:
            for context in self.context_dict:
                self.draw_stack = self.context_dict[context]
            else:
                self.context_dict[context] = self.create_context_values()
                self.native_context, self.draw_stack = self.context_dict[context]
        else:
            print("No context provided")

    def line_width(self, width=2.0, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.set_line_width(width))
        else:
            self.draw_stack.append(self.native_context.set_line_width(width))

    def fill_style(self, color=None, remove=False):
        if color is not None:
            num = re.search('^rgba\((\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*)\)$', color)
            if num is not None:
                #  Convert RGB values to be a float between 0 and 1
                r = float(num.group(1)) / 255
                g = float(num.group(2)) / 255
                b = float(num.group(3)) / 255
                a = float(num.group(4))
                if remove:
                    self.draw_stack.remove(self.native_context.set_source_rga(r, g, b, a))
                else:
                    self.draw_stack.append(self.native_context.set_source_rgba(r, g, b, a))
            else:
                pass
                # Support future colosseum versions
                # for named_color, rgb in colors.NAMED_COLOR.items():
                #     if named_color == color:
                #         exec('self.native.set_source_' + str(rgb))
        else:
            # Default to black
            if remove:
                self.draw_stack.remove(self.native_context.set_source_rga(0, 0, 0, 1))
            else:
                self.draw_stack.append(self.native_context.set_source_rgba(0, 0, 0, 1))

    def stroke_style(self, color=None, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.fill_style(color))
        else:
            self.draw_stack.append(self.native_context.fill_style(color))

    def new_path(self, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.new_path())
        else:
            self.draw_stack.append(self.native_context.new_path())

    def close_path(self, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.close_path())
        else:
            self.draw_stack.append(self.native_context.close_path())

    def move_to(self, x, y, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.move_to(x, y))
        else:
            self.draw_stack.append(self.native_context.move_to(x, y))

    def line_to(self, x, y, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.line_to(x, y))
        else:
            self.draw_stack.append(self.native_context.line_to(x, y))

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.curve_to(cp1x, cp1y, cp2x, cp2y, x, y))
        else:
            self.draw_stack.append(self.native_context.curve_to(cp1x, cp1y, cp2x, cp2y, x, y))

    def quadratic_curve_to(self, cpx, cpy, x, y, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.curve_to(cpx, cpy, cpx, cpy, x, y))
        else:
            self.draw_stack.append(self.native_context.curve_to(cpx, cpy, cpx, cpy, x, y))

    def arc(self, x, y, radius, startangle, endangle, anticlockwise, remove=False):
        if anticlockwise and remove:
            self.draw_stack.remove(self.native_context.arc_negative(x, y, radius, startangle, endangle))
        elif anticlockwise:
            self.draw_stack.append(self.native_context.arc_negative(x, y, radius, startangle, endangle))
        elif remove:
            self.draw_stack.remove(self.native_context.arc(x, y, radius, startangle, endangle))
        else:
            self.draw_stack.append(self.native_context.arc(x, y, radius, startangle, endangle))

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.save())
            self.translate(x, y, remove=True)
            if radiusx >= radiusy:
                self.scale(1, radiusy / radiusx, remove=True)
                self.arc(0, 0, radiusx, startangle, endangle, anticlockwise, remove=True)
            elif radiusy > radiusx:
                self.scale(radiusx / radiusy, 1, remove=True)
                self.arc(0, 0, radiusy, startangle, endangle, anticlockwise, remove=True)
            self.rotate(rotation, remove=True)
            self.reset_transform(remove=True)
            self.draw_stack.remove(self.native_context.restore())
        else:
            self.draw_stack.remove(self.native_context.save())
            self.translate(x, y)
            if radiusx >= radiusy:
                self.scale(1, radiusy / radiusx)
                self.arc(0, 0, radiusx, startangle, endangle, anticlockwise)
            elif radiusy > radiusx:
                self.scale(radiusx / radiusy, 1)
                self.arc(0, 0, radiusy, startangle, endangle, anticlockwise)
            self.rotate(rotation)
            self.reset_transform()
            self.draw_stack.restore()

    def rect(self, x, y, width, height, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.rectangle(x, y, width, height))
        else:
            self.draw_stack.append(self.native_context.rectangle(x, y, width, height))

    # Drawing Paths

    def fill(self, fill_rule, preserve, remove=False):
        if fill_rule is 'evenodd' and remove:
            self.draw_stack.remove(self.native_context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD))
        elif fill_rule is 'evenodd':
            self.draw_stack.append(self.native_context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD))
        elif remove:
            self.draw_stack.remove(self.native_context.set_fill_rule(cairo.FILL_RULE_WINDING))
        else:
            self.draw_stack.append(self.native_context.set_fill_rule(cairo.FILL_RULE_WINDING))
        if preserve and remove:
            self.draw_stack.remove(self.native_context.fill_preserve())
        elif preserve:
            self.draw_stack.append(self.native_context.fill_preserve())
        elif remove:
            self.draw_stack.remove(self.native_context.fill())
        else:
            self.draw_stack.append(self.native_context.fill())

    def stroke(self, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.stroke())
        else:
            self.draw_stack.append(self.native_context.stroke())

    # Transformations

    def rotate(self, radians, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.rotate(radians))
        else:
            self.draw_stack.append(self.native_context.rotate(radians))

    def scale(self, sx, sy, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.scale(sx, sy))
        else:
            self.draw_stack.append(self.native_context.scale(sx, sy))

    def translate(self, tx, ty, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.translate(tx, ty))
        else:
            self.draw_stack.append(self.native_context.translate(tx, ty))

    def reset_transform(self, remove=False):
        if remove:
            self.draw_stack.remove(self.native_context.identity_matrix())
        else:
            self.draw_stack.append(self.native_context.identity_matrix())

    def write_text(self, text, x, y, font, remove=False):
        # Set font family and size
        if font:
            write_font = font
        elif self.native.font:
            write_font = self.native.font
            write_font.family = self.native.font.get_family()
            write_font.size = self.native.font.get_size() / SCALE
        else:
            return
        if remove:
            self.draw_stack.remove(self.native_context.select_font_face(write_font.family))
            self.draw_stack.remove(self.native_context.set_font_size(write_font.size))
        else:
            self.draw_stack.append(self.native_context.select_font_face(write_font.family))
            self.draw_stack.append(self.native_context.set_font_size(write_font.size))

        # Support writing multiline text
        for line in text.splitlines():
            width, height = write_font.measure(line)
            if remove:
                self.draw_stack.remove(self.native_context.move_to(x, y))
                self.draw_stack.remove(self.native_context.text_path(line))
            else:
                self.draw_stack.append(self.native_context.move_to(x, y))
                self.draw_stack.append(self.native_context.text_path(line))
            y += height

    def measure_text(self, text, font):
        # Set font family and size
        if font:
            self.native_context.select_font_face(font.family)
            self.native_context.set_font_size(font.size)
        elif self.native.font:
            self.native_context.select_font_face(self.native.font.get_family())
            self.native_context.set_font_size(self.native.font.get_size() / SCALE)

        x_bearing, y_bearing, width, height, x_advance, y_advance = self.draw_stack.text_extents(text)
        return width, height

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()
