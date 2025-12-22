from dataclasses import dataclass
from io import BytesIO
from math import ceil

from travertino.size import at_least

from toga import Font
from toga.constants import Baseline, FillRule
from toga.fonts import SYSTEM_DEFAULT_FONT_SIZE
from toga.handlers import WeakrefCallable
from toga_gtk.colors import native_color
from toga_gtk.libs import (
    GTK_VERSION,
    Gdk,
    Gtk,
    Pango,
    PangoCairo,
    cairo,
    parse_css_color,
)

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
            self.native.connect("draw", self.gtk3_draw_callback)
            self.native.connect("size-allocate", self.gtk_on_size_allocate)
            self.native.connect("button-press-event", self.gtk_button_press)
            self.native.connect("button-release-event", self.gtk_button_release)
            self.native.connect("motion-notify-event", self.gtk_motion_notify)
            self.native.set_events(
                Gdk.EventMask.BUTTON_PRESS_MASK
                | Gdk.EventMask.BUTTON_RELEASE_MASK
                | Gdk.EventMask.BUTTON_MOTION_MASK
            )
        else:  # pragma: no-cover-if-gtk3
            self.native.set_draw_func(WeakrefCallable(self.gtk_draw_callback))
            self.native.connect("resize", self.gtk_resize)

            self.gesture_click = {}
            self.gesture_drag = {}
            for button in (1, 3):
                self.gesture_click[button] = Gtk.GestureClick()
                self.native.add_controller(self.gesture_click[button])
                self.gesture_click[button].set_button(button)
                self.gesture_click[button].connect(
                    "pressed", WeakrefCallable(self.gtk_pressed)
                )
                self.gesture_click[button].connect(
                    "released", WeakrefCallable(self.gtk_released)
                )

                self.gesture_drag[button] = Gtk.GestureDrag()
                self.native.add_controller(self.gesture_drag[button])
                self.gesture_drag[button].set_button(button)
                self.gesture_drag[button].connect(
                    "drag-update", WeakrefCallable(self.gtk_drag_update)
                )

    def _size(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            width = self.native.get_allocation().width
            height = self.native.get_allocation().height
        else:  # pragma: no-cover-if-gtk3
            width = self.native.compute_bounds(self.native)[1].get_width()
            height = self.native.compute_bounds(self.native)[1].get_height()
        return width, height

    if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4  # pragma: no branch

        def gtk3_draw_callback(self, widget, cairo_context):
            self.gtk_draw_callback(widget, cairo_context, *self._size())

    def gtk_draw_callback(self, widget, cairo_context, width, height):
        """Creates a draw callback.

        Gtk+ uses a drawing callback to draw on a DrawingArea. Assignment of the
        callback function creates a Gtk+ canvas and Gtk+ context automatically using the
        canvas and cairo_context function arguments. This method calls the draw method
        on the interface Canvas to draw the objects.
        """

        # Explicitly render the background
        sp = self.style_providers.get(("background_color", id(self.native)))
        bg = (
            parse_css_color(sp.to_string().split(": ")[1].split(";")[0]) if sp else None
        )
        if bg:
            cairo_context.set_source_rgba(
                255 * bg.r,
                255 * bg.g,
                255 * bg.b,
                bg.a,
            )
            cairo_context.rectangle(0, 0, width, height)
            cairo_context.fill()

        self.original_transform_matrix = cairo_context.get_matrix()
        self.interface.context._draw(self, cairo_context=cairo_context)

    if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4

        def gtk_on_size_allocate(self, widget, allocation):
            """Called on widget resize, and calls the handler set on the interface, if
            any."""
            self.interface.on_resize(width=allocation.width, height=allocation.height)

        def gtk_button_press(self, obj, event):
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

        def gtk_motion_notify(self, obj, event):
            """Handles mouse movement by calling the drag and/or alternative drag
            methods. Modifier keys have no effect."""
            if event.state & Gdk.ModifierType.BUTTON1_MASK:
                self.interface.on_drag(event.x, event.y)
            if event.state & Gdk.ModifierType.BUTTON3_MASK:
                self.interface.on_alt_drag(event.x, event.y)

        def gtk_button_release(self, obj, event):
            if event.button == 1:
                self.interface.on_release(event.x, event.y)
            elif event.button == 3:
                self.interface.on_alt_release(event.x, event.y)
            else:  # pragma: no cover
                # Don't handle other button presses
                pass

    else:  # pragma: no-cover-if-gtk3

        def gtk_resize(self, widget, width, height):
            self.interface.on_resize(width=width, height=height)

        def gtk_pressed(self, obj, n_press, x, y):
            if obj == self.gesture_click[1]:
                if n_press == 2:
                    self.interface.on_activate(x, y)
                else:
                    self.interface.on_press(x, y)
            elif obj == self.gesture_click[3]:
                self.interface.on_alt_press(x, y)
            else:  # pragma: no cover
                # Don't handle other button presses
                pass

        def gtk_released(self, obj, n_press, x, y):
            if obj == self.gesture_click[1]:
                self.interface.on_release(x, y)
            elif obj == self.gesture_click[3]:
                self.interface.on_alt_release(x, y)
            else:  # pragma: no cover
                # Don't handle other button presses
                pass

        def gtk_drag_update(self, obj, x, y):
            if obj == self.gesture_drag[1]:
                self.interface.on_drag(x, y)
            elif obj == self.gesture_drag[3]:
                self.interface.on_alt_drag(x, y)
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
        counterclockwise,
        cairo_context,
        **kwargs,
    ):
        if counterclockwise:
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
        counterclockwise,
        cairo_context,
        **kwargs,
    ):
        cairo_context.save()
        cairo_context.translate(x, y)
        cairo_context.rotate(rotation)
        if radiusx >= radiusy:
            cairo_context.scale(1, radiusy / radiusx)
            self.arc(
                0, 0, radiusx, startangle, endangle, counterclockwise, cairo_context
            )
        else:
            cairo_context.scale(radiusx / radiusy, 1)
            self.arc(
                0, 0, radiusy, startangle, endangle, counterclockwise, cairo_context
            )
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

        cairo_context.fill_preserve()

    def stroke(self, color, line_width, line_dash, cairo_context, **kwargs):
        cairo_context.set_source_rgba(*native_color(color))
        cairo_context.set_line_width(line_width)
        if line_dash is not None:
            cairo_context.set_dash(line_dash)
        cairo_context.stroke_preserve()

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
        self, text, x, y, font, baseline, line_height, cairo_context, **kwargs
    ):
        # Writing text should not affect current path, so save current path
        current_path = cairo_context.copy_path()
        # New path for text
        cairo_context.new_path()
        self._text_path(text, x, y, font, baseline, line_height, cairo_context)
        for op in ["fill", "stroke"]:
            if color := kwargs.pop(f"{op}_color", None):
                getattr(self, op)(color, cairo_context=cairo_context, **kwargs)
        # Restore previous path
        cairo_context.new_path()
        cairo_context.add_path(current_path)

    # No need to check whether Pango or PangoCairo are None, because if they were, the
    # user would already have received an exception when trying to create a Font.
    def _text_path(self, text, x, y, font, baseline, line_height, cairo_context):
        pango_context = self._pango_context(font)
        metrics = self._font_metrics(pango_context, line_height)
        lines = text.splitlines()
        total_height = metrics.line_height * len(lines)

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

    def _font_metrics(self, pango_context, line_height):
        pango_font = pango_context.load_font(pango_context.get_font_description())
        pango_metrics = pango_font.get_metrics()
        ascent = pango_metrics.get_ascent() / Pango.SCALE
        descent = pango_metrics.get_descent() / Pango.SCALE

        if line_height is None:
            # get_height was added in Pango 1.44, but Debian Buster comes with 1.42.
            scaled_line_height = ascent + descent
        else:
            font_size = (
                pango_font.describe_with_absolute_size().get_size() / Pango.SCALE
            )
            scaled_line_height = font_size * line_height

        return FontMetrics(ascent, descent, scaled_line_height)

    def measure_text(self, text, font, line_height):
        pango_context = self._pango_context(font)
        layout = Pango.Layout(pango_context)
        metrics = self._font_metrics(pango_context, line_height)

        widths = []
        for line in text.splitlines():
            layout.set_text(line)
            ink, logical = layout.get_extents()
            widths.append(logical.width / Pango.SCALE)

        return (
            ceil(max(width for width in widths)),
            metrics.line_height * len(widths),
        )

    def get_image_data(self):
        width, height = self._size()

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))
        context = cairo.Context(surface)

        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.draw(context)
        else:  # pragma: no-cover-if-gtk3
            self.gtk_draw_callback(self.native, context, width, height)

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
