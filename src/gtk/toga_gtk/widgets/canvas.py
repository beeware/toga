from toga_gtk.colors import native_color
from toga_gtk.libs import Gtk, Pango, cairo

from .base import Widget


class Canvas(Widget):
    def create(self):
        if cairo is None:
            raise RuntimeError(
                "'import cairo' failed; may need to install python-gi-cairo."
            )

        self.native = Gtk.DrawingArea()
        self.native.interface = self.interface
        self.native.connect("draw", self.gtk_draw_callback)

    def gtk_draw_callback(self, canvas, gtk_context):
        """Creates a draw callback

        Gtk+ uses a drawing callback to draw on a DrawingArea. Assignment of the
        callback function creates a Gtk+ canvas and Gtk+ context automatically
        using the canvas and gtk_context function arguments. This method calls
        the draw method on the interface Canvas to draw the objects.

        """
        self.interface._draw(self, draw_context=gtk_context)

    def redraw(self):
        pass

    # Basic paths

    def new_path(self, draw_context, *args, **kwargs):
        draw_context.new_path()

    def closed_path(self, x, y, draw_context, *args, **kwargs):
        draw_context.close_path()

    def move_to(self, x, y, draw_context, *args, **kwargs):
        draw_context.move_to(x, y)

    def line_to(self, x, y, draw_context, *args, **kwargs):
        draw_context.line_to(x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, draw_context, *args, **kwargs):
        draw_context.curve_to(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y, draw_context, *args, **kwargs):
        draw_context.curve_to(cpx, cpy, cpx, cpy, x, y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise, draw_context, *args, **kwargs):
        if anticlockwise:
            draw_context.arc_negative(x, y, radius, startangle, endangle)
        else:
            draw_context.arc(x, y, radius, startangle, endangle)

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise,
                draw_context, *args, **kwargs):
        draw_context.save()
        draw_context.translate(x, y)
        if radiusx >= radiusy:
            draw_context.scale(1, radiusy / radiusx)
            self.arc(0, 0, radiusx, startangle, endangle, anticlockwise, draw_context)
        else:
            draw_context.scale(radiusx / radiusy, 1)
            self.arc(0, 0, radiusy, startangle, endangle, anticlockwise, draw_context)
        draw_context.rotate(rotation)
        draw_context.identity_matrix()
        draw_context.restore()

    def rect(self, x, y, width, height, draw_context, *args, **kwargs):
        draw_context.rectangle(x, y, width, height)

    # Drawing Paths

    def apply_color(self, color, draw_context, *args, **kwargs):
        if color is not None:
            draw_context.set_source_rgba(*native_color(color))
        else:
            # set color to black
            draw_context.set_source_rgba(0, 0, 0, 1.0)

    def fill(self, color, fill_rule, preserve, draw_context, *args, **kwargs):
        self.apply_color(color, draw_context)
        if fill_rule is "evenodd":
            draw_context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        else:
            draw_context.set_fill_rule(cairo.FILL_RULE_WINDING)
        if preserve:
            draw_context.fill_preserve()
        else:
            draw_context.fill()

    def stroke(self, color, line_width, line_dash, draw_context, *args, **kwargs):
        self.apply_color(color, draw_context)
        draw_context.set_line_width(line_width)
        if line_dash is not None:
            draw_context.set_dash(line_dash)
        draw_context.stroke()
        draw_context.set_dash([])

    # Transformations

    def rotate(self, radians, draw_context, *args, **kwargs):
        draw_context.rotate(radians)

    def scale(self, sx, sy, draw_context, *args, **kwargs):
        draw_context.scale(sx, sy)

    def translate(self, tx, ty, draw_context, *args, **kwargs):
        draw_context.translate(tx, ty)

    def reset_transform(self, draw_context, *args, **kwargs):
        draw_context.identity_matrix()

    # Text

    def write_text(self, text, x, y, font, draw_context, *args, **kwargs):
        # Set font family and size
        if font:
            write_font = font
        elif self.native.font:
            write_font = self.native.font
            write_font.family = self.native.font.get_family()
            write_font.size = self.native.font.get_size() / Pango.SCALE
        draw_context.select_font_face(write_font.family)
        draw_context.set_font_size(write_font.size)

        # Support writing multiline text
        for line in text.splitlines():
            width, height = write_font.measure(line)
            draw_context.move_to(x, y)
            draw_context.text_path(line)
            y += height

    def measure_text(self, text, font, draw_context, *args, **kwargs):
        # Set font family and size
        if font:
            draw_context.select_font_face(font.family)
            draw_context.set_font_size(font.size)
        elif self.native.font:
            draw_context.select_font_face(self.native.font.get_family())
            draw_context.set_font_size(self.native.font.get_size() / Pango.SCALE)

        x_bearing, y_bearing, width, height, x_advance, y_advance = draw_context.text_extents(
            text
        )
        return width, height

    # Rehint

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()
