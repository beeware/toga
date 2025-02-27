from dataclasses import dataclass
from io import BytesIO
from math import ceil

from travertino.size import at_least

from toga import Font
from toga.constants import Baseline, FillRule
from toga.fonts import SYSTEM_DEFAULT_FONT_SIZE
from toga_gtk.colors import native_color
from toga_gtk.libs import GTK_VERSION, Gdk, Gtk, Pango, PangoCairo, cairo

from .base import Widget


class Canvas(Widget):
    def create(self):
        if cairo is None:  # pragma: no cover
            raise RuntimeError(
                "Unable to import Cairo. Ensure that the system package "
                "providing Cairo and its GTK bindings have been installed."
            )

        self.native = Gtk.DrawingArea()

        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
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
        else:  # pragma: no-cover-if-gtk3
            pass

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
        self.interface.on_resize(width=allocation.width, height=allocation.height)

    def mouse_down(self, obj, event):
        if event.button == 1:
            if event.type == Gdk.EventType._2BUTTON_PRESS:
                self.interface.on_activate(event.x, event.y)
            else:
                self.interface.on_press(event.x, event.y)
        elif event.button == 3:
            self.interface.on_alt_press(event.x, event.y)
        else:  # pragma: no cover
            # Don't handle other button presses
            pass

    def mouse_move(self, obj, event):
        if event.state == Gdk.ModifierType.BUTTON1_MASK:
            self.interface.on_drag(event.x, event.y)
        if event.state == Gdk.ModifierType.BUTTON3_MASK:
            self.interface.on_alt_drag(event.x, event.y)

    def mouse_up(self, obj, event):
        if event.button == 1:
            self.interface.on_release(event.x, event.y)
        elif event.button == 3:
            self.interface.on_alt_release(event.x, event.y)
        else:  # pragma: no cover
            # Don't handle other button presses
            pass

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
        # A Quadratic curve is a dimensionally reduced Bézier Cubic curve;
        # we can convert the single Quadratic control point into the
        # 2 control points required for the cubic Bézier.
        x0, y0 = cairo_context.get_current_point()
        cairo_context.curve_to(
            x0 + 2 / 3 * (cpx - x0),
            y0 + 2 / 3 * (cpy - y0),
            x + 2 / 3 * (cpx - x),
            y + 2 / 3 * (cpy - y),
            x,
            y,
        )

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
        cairo_context.rotate(rotation)
        if radiusx >= radiusy:
            cairo_context.scale(1, radiusy / radiusx)
            self.arc(0, 0, radiusx, startangle, endangle, anticlockwise, cairo_context)
        else:
            cairo_context.scale(radiusx / radiusy, 1)
            self.arc(0, 0, radiusy, startangle, endangle, anticlockwise, cairo_context)
        cairo_context.identity_matrix()
        cairo_context.restore()

    def rect(self, x, y, width, height, cairo_context, **kwargs):
        cairo_context.rectangle(x, y, width, height)

    # Drawing Paths

    def fill(self, color, fill_rule, cairo_context, **kwargs):
        cairo_context.set_source_rgba(*native_color(color))
        if fill_rule == FillRule.EVENODD:
            cairo_context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        else:
            cairo_context.set_fill_rule(cairo.FILL_RULE_WINDING)

        cairo_context.fill()

    def stroke(self, color, line_width, line_dash, cairo_context, **kwargs):
        cairo_context.set_source_rgba(*native_color(color))
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

    def write_text(
        self, text, x, y, font, baseline, cairo_context, line_height_factor, **kwargs
    ):
        for op in ["fill", "stroke"]:
            if color := kwargs.pop(f"{op}_color", None):
                self._text_path(
                    text, x, y, font, baseline, cairo_context, line_height_factor
                )
                getattr(self, op)(color, cairo_context=cairo_context, **kwargs)

    # No need to check whether Pango or PangoCairo are None, because if they were, the
    # user would already have received an exception when trying to create a Font.
    def _text_path(self, text, x, y, font, baseline, cairo_context, line_height_factor):
        pango_context = self._pango_context(font)
        metrics = self._font_metrics(pango_context)
        lines = text.splitlines()
        total_height = metrics.line_height * len(lines) * line_height_factor

        if baseline == Baseline.TOP:
            top = y + metrics.ascent
        elif baseline == Baseline.MIDDLE:
            top = y + metrics.ascent - (total_height / 2)
        elif baseline == Baseline.BOTTOM:
            top = y + metrics.ascent - total_height
        else:
            # Default to Baseline.ALPHABETIC
            top = y

        layout = Pango.Layout(pango_context)
        for line_num, line in enumerate(lines):
            layout.set_text(line)
            cairo_context.move_to(x, top + (metrics.line_height * line_num))
            PangoCairo.layout_line_path(cairo_context, layout.get_line(0))

    def _pango_context(self, font):
        # TODO: detect the actual default family and size (see tests_backend/fonts.py).
        if font.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
            font = Font(
                font.interface.family,
                size=10,
                weight=font.interface.weight,
                style=font.interface.style,
                variant=font.interface.variant,
            )._impl

        pango_context = self.native.create_pango_context()
        pango_context.set_font_description(font.native)
        return pango_context

    def _font_metrics(self, pango_context):
        pango_metrics = pango_context.load_font(
            pango_context.get_font_description()
        ).get_metrics()
        ascent = pango_metrics.get_ascent() / Pango.SCALE
        descent = pango_metrics.get_descent() / Pango.SCALE

        # get_height was added in Pango 1.44, but Debian Buster comes with 1.42.
        line_height = ascent + descent
        return FontMetrics(ascent, descent, line_height)

    def measure_text(self, text, font, line_height_factor):
        pango_context = self._pango_context(font)
        layout = Pango.Layout(pango_context)

        widths = []
        for line in text.splitlines():
            layout.set_text(line)
            ink, logical = layout.get_extents()
            widths.append(logical.width / Pango.SCALE)

        return (
            ceil(max(width for width in widths)),
            self._font_metrics(pango_context).line_height
            * len(widths)
            * line_height_factor,
        )

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
        # print(
        #     "REHINT",
        #     self,
        #     self.native.get_preferred_width(),
        #     self.native.get_preferred_height(),
        # )
        # width = self.native.get_allocation().width
        # height = self.native.get_allocation().height
        width = self.interface._MIN_WIDTH
        height = self.interface._MIN_HEIGHT
        self.interface.intrinsic.height = at_least(width)
        self.interface.intrinsic.width = at_least(height)


@dataclass
class FontMetrics:
    ascent: float
    descent: float
    line_height: int
