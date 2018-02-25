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
        default_stack = []
        self.current_context = default_stack
        self.context_map = {'default': default_stack}
        self.current_context.append(cairo.Context(self.surface))
        self.native.font = None

    def set_on_draw(self, handler):
        self.native.connect('draw', handler)

    def set_context(self, context):
        if context:
            for context in self.context_map:
                self.current_context = self.context_map[context]
            else:
                self.context_map[context] = []
                self.current_context = self.context_map[context]
                self.current_context.append(cairo.Context(self.surface))
        else:
            print("No context provided")

    def line_width(self, width=2.0, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.set_line_width(width))
        else:
            self.current_context.append(context.set_line_width(width))

    def fill_style(self, color=None, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if color is not None:
            num = re.search('^rgba\((\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*), (\d*\.?\d*)\)$', color)
            if num is not None:
                #  Convert RGB values to be a float between 0 and 1
                r = float(num.group(1)) / 255
                g = float(num.group(2)) / 255
                b = float(num.group(3)) / 255
                a = float(num.group(4))
                if remove:
                    self.current_context.remove(context.set_source_rga(r, g, b, a))
                else:
                    self.current_context.append(context.set_source_rgba(r, g, b, a))
            else:
                pass
                # Support future colosseum versions
                # for named_color, rgb in colors.NAMED_COLOR.items():
                #     if named_color == color:
                #         exec('self.native.set_source_' + str(rgb))
        else:
            # Default to black
            if remove:
                self.current_context.remove(context.set_source_rga(0, 0, 0, 1))
            else:
                self.current_context.append(context.set_source_rgba(0, 0, 0, 1))

    def stroke_style(self, color=None, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.fill_style(color))
        else:
            self.current_context.append(context.fill_style(color))

    def new_path(self, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.new_path())
        else:
            self.current_context.append(context.new_path())

    def close_path(self, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.close_path())
        else:
            self.current_context.append(context.close_path())

    def move_to(self, x, y, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.move_to(x, y))
        else:
            self.current_context.append(context.move_to(x, y))

    def line_to(self, x, y, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.line_to(x, y))
        else:
            self.current_context.append(context.line_to(x, y))

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.curve_to(cp1x, cp1y, cp2x, cp2y, x, y))
        else:
            self.current_context.append(context.curve_to(cp1x, cp1y, cp2x, cp2y, x, y))

    def quadratic_curve_to(self, cpx, cpy, x, y, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.curve_to(cpx, cpy, cpx, cpy, x, y))
        else:
            self.current_context.append(context.curve_to(cpx, cpy, cpx, cpy, x, y))

    def arc(self, x, y, radius, startangle, endangle, anticlockwise, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if anticlockwise and remove:
            self.current_context.remove(context.arc_negative(x, y, radius, startangle, endangle))
        elif anticlockwise:
            self.current_context.append(context.arc_negative(x, y, radius, startangle, endangle))
        elif remove:
            self.current_context.remove(context.arc(x, y, radius, startangle, endangle))
        else:
            self.current_context.append(context.arc(x, y, radius, startangle, endangle))

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.save())
            self.translate(x, y, remove=True)
            if radiusx >= radiusy:
                self.scale(1, radiusy / radiusx, remove=True)
                self.arc(0, 0, radiusx, startangle, endangle, anticlockwise, remove=True)
            elif radiusy > radiusx:
                self.scale(radiusx / radiusy, 1, remove=True)
                self.arc(0, 0, radiusy, startangle, endangle, anticlockwise, remove=True)
            self.rotate(rotation, remove=True)
            self.reset_transform(remove=True)
            self.current_context.remove(context.restore())
        else:
            self.current_context.remove(context.save())
            self.translate(x, y)
            if radiusx >= radiusy:
                self.scale(1, radiusy / radiusx)
                self.arc(0, 0, radiusx, startangle, endangle, anticlockwise)
            elif radiusy > radiusx:
                self.scale(radiusx / radiusy, 1)
                self.arc(0, 0, radiusy, startangle, endangle, anticlockwise)
            self.rotate(rotation)
            self.reset_transform()
            self.current_context.restore()

    def rect(self, x, y, width, height, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.rectangle(x, y, width, height))
        else:
            self.current_context.append(context.rectangle(x, y, width, height))

    # Drawing Paths

    def fill(self, fill_rule, preserve, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if fill_rule is 'evenodd' and remove:
            self.current_context.remove(context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD))
        elif fill_rule is 'evenodd':
            self.current_context.append(context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD))
        elif remove:
            self.current_context.remove(context.set_fill_rule(cairo.FILL_RULE_WINDING))
        else:
            self.current_context.append(context.set_fill_rule(cairo.FILL_RULE_WINDING))
        if preserve and remove:
            self.current_context.remove(context.fill_preserve())
        elif preserve:
            self.current_context.append(context.fill_preserve())
        elif remove:
            self.current_context.remove(context.fill())
        else:
            self.current_context.append(context.fill())

    def stroke(self, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.stroke())
        else:
            self.current_context.append(context.stroke())

    # Transformations

    def rotate(self, radians, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.rotate(radians))
        else:
            self.current_context.append(context.rotate(radians))

    def scale(self, sx, sy, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.scale(sx, sy))
        else:
            self.current_context.append(context.scale(sx, sy))

    def translate(self, tx, ty, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.translate(tx, ty))
        else:
            self.current_context.append(context.translate(tx, ty))

    def reset_transform(self, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
        if remove:
            self.current_context.remove(context.identity_matrix())
        else:
            self.current_context.append(context.identity_matrix())

    def write_text(self, text, x, y, font, remove=False):
        context = self.current_context[cairo.Context(self.surface)]
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
            self.current_context.remove(context.select_font_face(write_font.family))
            self.current_context.remove(context.set_font_size(write_font.size))
        else:
            self.current_context.append(context.select_font_face(write_font.family))
            self.current_context.append(context.set_font_size(write_font.size))

        # Support writing multiline text
        for line in text.splitlines():
            width, height = write_font.measure(line)
            if remove:
                self.current_context.remove(context.move_to(x, y))
                self.current_context.remove(context.text_path(line))
            else:
                self.current_context.append(context.move_to(x, y))
                self.current_context.append(context.text_path(line))
            y += height

    def measure_text(self, text, font):
        context = self.current_context[cairo.Context(self.surface)]
        # Set font family and size
        if font:
            self.context.select_font_face(font.family)
            self.context.set_font_size(font.size)
        elif self.native.font:
            self.context.select_font_face(self.native.font.get_family())
            self.context.set_font_size(self.native.font.get_size() / SCALE)

        x_bearing, y_bearing, width, height, x_advance, y_advance = self.current_context.text_extents(text)
        return width, height

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()
