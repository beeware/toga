from ..colors import native_color
from ..libs import Gdk, Gtk, Pango, cairo
from .base import Widget


class Canvas(Widget):
    def create(self):
        if cairo is None:
            raise RuntimeError(
                "'import cairo' failed; may need to install python-gi-cairo."
            )

        self.native = Gtk.DrawingArea()

        self.native.connect("draw", self.gtk_draw_callback)
        self.native.connect("size-allocate", self.gtk_on_size_allocate)
        self.native.connect("button-press-event", self.mouse_down)
        self.native.connect("button-release-event", self.mouse_up)
        self.native.connect("motion-notify-event", self.mouse_move)
        self.native.set_events(
            Gdk.EventMask.BUTTON_PRESS_MASK
            | Gdk.EventMask.BUTTON_RELEASE_MASK
            | Gdk.EventMask.BUTTON_MOTION_MASK
        )

    def gtk_draw_callback(self, canvas, gtk_context):
        """Creates a draw callback.

        Gtk+ uses a drawing callback to draw on a DrawingArea. Assignment of the
        callback function creates a Gtk+ canvas and Gtk+ context automatically using the
        canvas and gtk_context function arguments. This method calls the draw method on
        the interface Canvas to draw the objects.
        """
        self.original_transform_matrix = gtk_context.get_matrix()
        self.interface._draw(self, draw_context=gtk_context)

    def gtk_on_size_allocate(self, widget, allocation):
        """Called on widget resize, and calls the handler set on the interface, if
        any."""
        self.interface.on_resize(None, allocation.width, allocation.height)

    def mouse_down(self, obj, event):
        if event.button == 1:
            if event.type == Gdk.EventType._2BUTTON_PRESS:
                self.interface.on_activate(None, event.x, event.y)
            else:
                self.interface.on_press(None, event.x, event.y)
        if event.button == 3:
            self.interface.on_alt_press(None, event.x, event.y)

    def mouse_move(self, obj, event):
        # TODO? Is mouse pressed
        # if self.clicks == 0:
        #     return
        if event.state == Gdk.ModifierType.BUTTON1_MASK:
            self.interface.on_drag(None, event.x, event.y)
        if event.state == Gdk.ModifierType.BUTTON3_MASK:
            self.interface.on_alt_drag(None, event.x, event.y)

    def mouse_up(self, obj, event):
        if event.button == 1:
            self.interface.on_release(None, event.x, event.y)
        if event.button == 3:
            self.interface.on_alt_release(None, event.x, event.y)

    def redraw(self):
        self.native.queue_draw()

    # Context management
    def push_context(self, draw_context, **kwargs):
        draw_context.save()

    def pop_context(self, draw_context, **kwargs):
        draw_context.restore()

    # Basic paths
    def begin_path(self, draw_context, **kwargs):
        draw_context.new_path()

    def close_path(self, x, y, draw_context, **kwargs):
        draw_context.close_path()

    def move_to(self, x, y, draw_context, **kwargs):
        draw_context.move_to(x, y)

    def line_to(self, x, y, draw_context, **kwargs):
        draw_context.line_to(x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, draw_context, **kwargs):
        draw_context.curve_to(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y, draw_context, **kwargs):
        draw_context.curve_to(cpx, cpy, cpx, cpy, x, y)

    def arc(
        self,
        x,
        y,
        radius,
        startangle,
        endangle,
        anticlockwise,
        draw_context,
        **kwargs,
    ):
        if anticlockwise:
            draw_context.arc_negative(x, y, radius, startangle, endangle)
        else:
            draw_context.arc(x, y, radius, startangle, endangle)

    def ellipse(
        self,
        x,
        y,
        radiusx,
        radiusy,
        rotation,
        startangle,
        endangle,
        anticlockwise,
        draw_context,
        *args,
        **kwargs,
    ):
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

    def rect(self, x, y, width, height, draw_context, **kwargs):
        draw_context.rectangle(x, y, width, height)

    # Drawing Paths

    def apply_color(self, color, draw_context, **kwargs):
        if color is not None:
            draw_context.set_source_rgba(*native_color(color))
        else:
            # set color to black
            draw_context.set_source_rgba(0, 0, 0, 1.0)

    def fill(self, color, fill_rule, draw_context, **kwargs):
        self.apply_color(color, draw_context)
        if fill_rule == "evenodd":
            draw_context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        else:
            draw_context.set_fill_rule(cairo.FILL_RULE_WINDING)

        draw_context.fill()

    def stroke(self, color, line_width, line_dash, draw_context, **kwargs):
        self.apply_color(color, draw_context)
        draw_context.set_line_width(line_width)
        if line_dash is not None:
            draw_context.set_dash(line_dash)
        draw_context.stroke()
        draw_context.set_dash([])

    # Transformations

    def rotate(self, radians, draw_context, **kwargs):
        draw_context.rotate(radians)

    def scale(self, sx, sy, draw_context, **kwargs):
        draw_context.scale(sx, sy)

    def translate(self, tx, ty, draw_context, **kwargs):
        draw_context.translate(tx, ty)

    def reset_transform(self, draw_context, **kwargs):
        draw_context.set_matrix(self.original_transform_matrix)

    # Text

    def write_text(self, text, x, y, font, draw_context, **kwargs):
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
            width, height = self.measure_text(line, write_font)
            draw_context.move_to(x, y)
            draw_context.text_path(line)
            y += height

    def measure_text(self, text, font):
        layout = self.native.create_pango_layout(text)

        layout.set_font_description(font.native)
        _, logical = layout.get_extents()

        width = (logical.width / Pango.SCALE) - (logical.width * 0.2) / Pango.SCALE
        height = logical.height / Pango.SCALE

        return width, height

    def get_image_data(self):
        self.interface.factory.not_implemented("Canvas.get_image_data()")

    # Rehint

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        # width = self.native.get_preferred_width()
        # height = self.native.get_preferred_height()
        pass
