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

from .base import Widget
from ..color import native_color


class Canvas(Widget):
    def create(self):
        if cairo is None:
            raise RuntimeError(
                "'import cairo' failed; may need to install python-gi-cairo."
            )

        self.native = Gtk.DrawingArea()
        self.native.interface = self.interface

    def create_draw_callback(self, root_context):
        """Creates a draw callback

        Gtk+ uses a drawing callback to draw on a DrawingArea. Assignment of the
        callback function creates a Gtk+ canvas and Gtk+ context automatically
        using the canvas and native_context function arguments. This method
        traverses through the full tree of drawing objects and uses the
        callback to call each one.

        """

        def draw_callback(canvas, context):
            for drawing_object in root_context.drawing_objects:
                drawing_object(self, native_context=context)

        self.native.connect("draw", draw_callback)

    def redraw(self, root_context):
        pass

    # Basic paths

    @staticmethod
    def new_path(native_context):
        native_context.new_path()

    @staticmethod
    def closed_path(native_context, x, y):
        native_context.close_path()

    @staticmethod
    def move_to(native_context, x, y):
        native_context.move_to(x, y)

    @staticmethod
    def line_to(native_context, x, y):
        native_context.line_to(x, y)

    # Basic shapes

    @staticmethod
    def bezier_curve_to(native_context, cp1x, cp1y, cp2x, cp2y, x, y):
        native_context.curve_to(cp1x, cp1y, cp2x, cp2y, x, y)

    @staticmethod
    def quadratic_curve_to(native_context, cpx, cpy, x, y):
        native_context.curve_to(cpx, cpy, cpx, cpy, x, y)

    @staticmethod
    def arc(native_context, x, y, radius, startangle, endangle, anticlockwise):
        if anticlockwise:
            native_context.arc_negative(x, y, radius, startangle, endangle)
        else:
            native_context.arc(x, y, radius, startangle, endangle)

    @staticmethod
    def ellipse(
        native_context,
        x,
        y,
        radiusx,
        radiusy,
        rotation,
        startangle,
        endangle,
        anticlockwise,
    ):
        native_context.save()
        native_context.translate(x, y)
        if radiusx >= radiusy:
            native_context.scale(1, radiusy / radiusx)
            native_context.arc(0, 0, radiusx, startangle, endangle, anticlockwise, native_context)
        else:
            native_context.scale(radiusx / radiusy, 1)
            native_context.arc(0, 0, radiusy, startangle, endangle, anticlockwise, native_context)
        native_context.rotate(rotation)
        native_context.identity_matrix()
        native_context.restore()

    @staticmethod
    def rect(native_context, x, y, width, height):
        native_context.rectangle(x, y, width, height)

    # Drawing Paths

    @staticmethod
    def apply_color(native_context, color):
        if color is not None:
            native_context.set_source_rgba(*native_color(color))
        else:
            # set color to black
            native_context.set_source_rgba(0, 0, 0, 1.0)

    @staticmethod
    def fill(native_context, color, fill_rule, preserve):
        native_context.apply_color(color, native_context)
        if fill_rule is "evenodd":
            native_context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        else:
            native_context.set_fill_rule(cairo.FILL_RULE_WINDING)
        if preserve:
            native_context.fill_preserve()
        else:
            native_context.fill()
            
    @staticmethod   
    def stroke(native_context, color, line_width):
        native_context.apply_color(color, native_context)
        native_context.set_line_width(line_width)
        native_context.stroke()

    # Transformations


    @staticmethod
    def rotate(native_context, radians):
        native_context.rotate(radians)

    @staticmethod
    def scale(native_context, sx, sy):
        native_context.scale(sx, sy)

    @staticmethod
    def translate(native_context, tx, ty):
        native_context.translate(tx, ty)

    @staticmethod
    def reset_transform(native_context):
        native_context.identity_matrix()

    # Text

    @staticmethod
    def write_text(native_context, text, x, y, font):
        # Set font family and size
        if font:
            write_font = font
        elif native_context.native.font:
            write_font = native_context.native.font
            write_font.family = native_context.native.font.get_family()
            write_font.size = native_context.native.font.get_size() / SCALE
        native_context.select_font_face(write_font.family)
        native_context.set_font_size(write_font.size)

        # Support writing multiline text
        for line in text.splitlines():
            width, height = write_font.measure(line)
            native_context.move_to(x, y)
            native_context.text_path(line)
            y += height

    @staticmethod
    def measure_text(native_context, text, font):
        # Set font family and size
        if font:
            native_context.select_font_face(font.family)
            native_context.set_font_size(font.size)
        elif native_context.native.font:
            native_context.select_font_face(native_context.native.font.get_family())
            native_context.set_font_size(native_context.native.font.get_size() / SCALE)

        x_bearing, y_bearing, width, height, x_advance, y_advance = native_context.text_extents(
            text
        )
        return width, height

    # Rehint

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()
