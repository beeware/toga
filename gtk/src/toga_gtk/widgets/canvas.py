from io import BytesIO

from travertino.size import at_least

from toga_gtk.colors import native_color
from toga_gtk.libs import Gdk, Gtk, Pango, cairo

from .base import Widget


class Canvas(Widget):
    def create(self):
        if cairo is None:  # pragma: no cover
            raise RuntimeError(
                "Unable to import Cairo. Ensure that the system package "
                "providing Cairo and its GTK bindings have been installed."
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

    def gtk_draw_callback(self, widget, cairo_context):
        """Creates a draw callback.

        Gtk+ uses a drawing callback to draw on a DrawingArea. Assignment of the
        callback function creates a Gtk+ canvas and Gtk+ context automatically using the
        canvas and cairo_context function arguments. This method calls the draw method
        on the interface Canvas to draw the objects.
        """

        # Explicitly render the background
        sc = self.native.get_style_context()
        bg = sc.get_property("background-color", sc.get_state())
        if bg:
            cairo_context.set_source_rgba(
                255 * bg.red,
                255 * bg.green,
                255 * bg.blue,
                bg.alpha,
            )
            width = self.native.get_allocation().width
            height = self.native.get_allocation().height
            cairo_context.rectangle(0, 0, width, height)
            cairo_context.fill()

        self.original_transform_matrix = cairo_context.get_matrix()
        self.interface.context._draw(self, cairo_context=cairo_context)

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
        elif event.button == 3:
            self.interface.on_alt_press(None, event.x, event.y)

    def mouse_move(self, obj, event):
        if event.state == Gdk.ModifierType.BUTTON1_MASK:
            self.interface.on_drag(None, event.x, event.y)
        if event.state == Gdk.ModifierType.BUTTON3_MASK:
            self.interface.on_alt_drag(None, event.x, event.y)

    def mouse_up(self, obj, event):
        if event.button == 1:
            self.interface.on_release(None, event.x, event.y)
        elif event.button == 3:
            self.interface.on_alt_release(None, event.x, event.y)

    def redraw(self):
        self.native.queue_draw()

    # Context management
    def push_context(self, cairo_context, **kwargs):
        cairo_context.save()

    def pop_context(self, cairo_context, **kwargs):
        cairo_context.restore()

    # Basic paths
    def begin_path(self, cairo_context, **kwargs):
        cairo_context.new_path()

    def close_path(self, cairo_context, **kwargs):
        cairo_context.close_path()

    def move_to(self, x, y, cairo_context, **kwargs):
        cairo_context.move_to(x, y)

    def line_to(self, x, y, cairo_context, **kwargs):
        cairo_context.line_to(x, y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, cairo_context, **kwargs):
        cairo_context.curve_to(cp1x, cp1y, cp2x, cp2y, x, y)

    def quadratic_curve_to(self, cpx, cpy, x, y, cairo_context, **kwargs):
        cairo_context.curve_to(cpx, cpy, cpx, cpy, x, y)

    def arc(
        self,
        x,
        y,
        radius,
        startangle,
        endangle,
        anticlockwise,
        cairo_context,
        **kwargs,
    ):
        if anticlockwise:
            cairo_context.arc_negative(x, y, radius, startangle, endangle)
        else:
            cairo_context.arc(x, y, radius, startangle, endangle)

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
        cairo_context,
        **kwargs,
    ):
        cairo_context.save()
        cairo_context.translate(x, y)
        if radiusx >= radiusy:
            cairo_context.scale(1, radiusy / radiusx)
            self.arc(0, 0, radiusx, startangle, endangle, anticlockwise, cairo_context)
        else:
            cairo_context.scale(radiusx / radiusy, 1)
            self.arc(0, 0, radiusy, startangle, endangle, anticlockwise, cairo_context)
        cairo_context.rotate(rotation)
        cairo_context.identity_matrix()
        cairo_context.restore()

    def rect(self, x, y, width, height, cairo_context, **kwargs):
        cairo_context.rectangle(x, y, width, height)

    # Drawing Paths

    def apply_color(self, color, cairo_context, **kwargs):
        if color is not None:
            cairo_context.set_source_rgba(*native_color(color))
        else:
            # set color to black
            cairo_context.set_source_rgba(0, 0, 0, 1.0)

    def fill(self, color, fill_rule, cairo_context, **kwargs):
        self.apply_color(color, cairo_context)
        if fill_rule == "evenodd":
            cairo_context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        else:
            cairo_context.set_fill_rule(cairo.FILL_RULE_WINDING)

        cairo_context.fill()

    def stroke(self, color, line_width, line_dash, cairo_context, **kwargs):
        self.apply_color(color, cairo_context)
        cairo_context.set_line_width(line_width)
        if line_dash is not None:
            cairo_context.set_dash(line_dash)
        cairo_context.stroke()
        cairo_context.set_dash([])

    # Transformations

    def rotate(self, radians, cairo_context, **kwargs):
        cairo_context.rotate(radians)

    def scale(self, sx, sy, cairo_context, **kwargs):
        cairo_context.scale(sx, sy)

    def translate(self, tx, ty, cairo_context, **kwargs):
        cairo_context.translate(tx, ty)

    def reset_transform(self, cairo_context, **kwargs):
        cairo_context.set_matrix(self.original_transform_matrix)

    # Text

    def write_text(self, text, x, y, font, cairo_context, **kwargs):
        # Set font family and size
        if font:
            write_font = font.interface
        elif self.native.font:
            write_font = self.native.font
            write_font.family = self.native.font.get_family()
            write_font.size = self.native.font.get_size() / Pango.SCALE

        cairo_context.select_font_face(write_font.family)
        cairo_context.set_font_size(write_font.size)

        # Support writing multiline text
        for line in text.splitlines():
            width, height = self.measure_text(line, write_font._impl)
            cairo_context.move_to(x, y)
            cairo_context.text_path(line)
            y += height

    def measure_text(self, text, font):
        layout = self.native.create_pango_layout(text)

        layout.set_font_description(font.native)
        _, logical = layout.get_extents()

        width = (logical.width / Pango.SCALE) - (logical.width * 0.2) / Pango.SCALE
        height = logical.height / Pango.SCALE

        return width, height

    def get_image_data(self):
        width = self.native.get_allocation().width
        height = self.native.get_allocation().height

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)

        self.native.draw(context)

        data = BytesIO()
        surface.write_to_png(data)
        return data.getbuffer()

    # Rehint
    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        # width = self.native.get_allocation().width
        # height = self.native.get_allocation().height
        width = self.interface._MIN_WIDTH
        height = self.interface._MIN_HEIGHT
        self.interface.intrinsic.height = at_least(width)
        self.interface.intrinsic.width = at_least(height)
