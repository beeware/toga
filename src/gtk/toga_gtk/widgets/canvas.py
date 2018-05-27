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

from .base import Widget
from ..color import native_color


class Canvas(Widget):
    def create(self):
        if cairo is None:
            raise RuntimeError("'import cairo' failed; may need to install python-gi-cairo.")

        self.native = Gtk.DrawingArea()
        self.native.interface = self.interface

    def set_root_context(self, root_context):
        """Sets the root context from the interface so that it can be traversed.

        Gtk+ uses a drawing callback to draw on a DrawingArea. Assignment of the
        callback function creates a Gtk+ canvas and Gtk+ context automatically
        using the canvas and native_context function arguments. This method
        traverses through the full tree of drawing objects and uses the
        callback to call each one.

        """
        def draw_callback(canvas, context):
            for drawing_object in traverse(root_context.drawing_objects):
                drawing_object(self, native_context=context)
        self.native.connect('draw', draw_callback)

    def redraw(self):
        pass

    # Basic paths

    def new_path(self, native_context):
        native_context.new_path()

    def closed_path(self, x, y, native_context):
        native_context.close_path()

    def move_to(self, x, y, native_context):
        native_context.move_to(x, y)

    def line_to(self, x, y, native_context):
        native_context.line_to(x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, native_context):
        native_context.curve_to(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y, native_context):
        native_context.curve_to(cpx, cpy, cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise, native_context):
        if anticlockwise:
            native_context.arc_negative(x, y, radius, startangle, endangle)
        else:
            native_context.arc(x, y, radius, startangle, endangle)

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise, native_context):
        native_context.save()
        native_context.translate(x, y)
        if radiusx >= radiusy:
            native_context.scale(1, radiusy / radiusx)
            self.arc(0, 0, radiusx, startangle, endangle, anticlockwise, native_context)
        elif radiusy > radiusx:
            native_context.scale(radiusx / radiusy, 1)
            self.arc(0, 0, radiusy, startangle, endangle, anticlockwise, native_context)
        native_context.rotate(rotation)
        native_context.identity_matrix()
        native_context.restore()

    def rect(self, x, y, width, height, native_context):
        native_context.rectangle(x, y, width, height)

    # Drawing Paths

    def apply_color(self, color, native_context):
        if color is not None:
            native_context.set_source_rgba(*native_color(color))
        else:
            # set color to black
            native_context.set_source_rgba(0, 0, 0, 1.0)

    def fill(self, color, fill_rule, preserve, native_context):
        self.apply_color(color, native_context)
        if fill_rule is 'evenodd':
            native_context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        else:
            native_context.set_fill_rule(cairo.FILL_RULE_WINDING)
        if preserve:
            native_context.fill_preserve()
        else:
            native_context.fill()

    def stroke(self, color, line_width, native_context):
        self.apply_color(color, native_context)
        native_context.set_line_width(line_width)
        native_context.stroke()

    def write_text(self, text, x, y, font, native_context):
        # Set font family and size
        if font:
            write_font = font
        elif self.native.font:
            write_font = self.native.font
            write_font.family = self.native.font.get_family()
            write_font.size = self.native.font.get_size() / scale
        native_context.select_font_face(write_font.family)
        native_context.set_font_size(write_font.size)

        # Support writing multiline text
        for line in text.splitlines():
            width, height = write_font.measure(line)
            native_context.move_to(x, y)
            native_context.text_path(line)
            y += height

    def measure_text(self, text, font, native_context):
        # Set font family and size
        if font:
            native_context.select_font_face(font.family)
            native_context.set_font_size(font.size)
        elif self.native.font:
            native_context.select_font_face(self.native.font.get_family())
            native_context.set_font_size(self.native.font.get_size() / scale)

        x_bearing, y_bearing, width, height, x_advance, y_advance = native_context.text_extents(text)
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
