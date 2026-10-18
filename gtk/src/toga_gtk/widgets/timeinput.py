from datetime import time

from travertino.size import at_least

from ..libs import GTK_VERSION, Gtk
from .base import Widget


class TimeInput(Widget):
    def create(self):
        # GTK has no time picker. Compose native spin controls so editing, keyboard
        # navigation, and accessibility are still provided by GTK.
        self.native = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self._min_time = time(0, 0, 0)
        self._max_time = time(23, 59, 59)
        self._suppress_signals = False
        self.fields = []

        for name, upper in (("Hours", 23), ("Minutes", 59), ("Seconds", 59)):
            if self.fields:
                self.append(Gtk.Label(label=":"))
            field = Gtk.SpinButton.new_with_range(0, upper, 1)
            field.set_numeric(True)
            field.set_hexpand(True)
            field.set_name(f"toga-{self.interface.id}-{name.lower()}")
            field.set_tooltip_text(name)
            if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
                field.get_style_context().add_class("toga")
                field.get_accessible().set_name(name)
            else:  # pragma: no-cover-if-gtk3
                field.add_css_class("toga")
                field.update_property([Gtk.AccessibleProperty.LABEL], [name])
            field.connect("output", self.gtk_output)
            field.connect("value-changed", self.gtk_on_change)
            self.fields.append(field)
            self.append(field)

    def append(self, child):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.add(child)
        else:  # pragma: no-cover-if-gtk3
            self.native.append(child)

    def gtk_output(self, field):
        field.set_text(f"{field.get_value_as_int():02d}")
        return True

    def gtk_on_change(self, *_args):
        if not self._suppress_signals:
            self.set_value(max(self._min_time, min(self.get_value(), self._max_time)))

    def get_value(self):
        return time(*(field.get_value_as_int() for field in self.fields))

    def set_value(self, value):
        self._suppress_signals = True
        try:
            for field, component in zip(
                self.fields, (value.hour, value.minute, value.second), strict=True
            ):
                field.set_value(component)
        finally:
            self._suppress_signals = False
        self.interface.on_change()

    def get_min_time(self):
        return self._min_time

    def set_min_time(self, value):
        self._min_time = value

    def get_max_time(self):
        return self._max_time

    def set_max_time(self, value):
        self._max_time = value

    def focus(self):
        self.fields[0].grab_focus()

    @property
    def has_focus(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            return any(field.has_focus() for field in self.fields)
        else:  # pragma: no-cover-if-gtk3
            return super().has_focus

    def apply_css(self, property, css, native=None, selector=".toga"):
        super().apply_css(property, css, native, selector)
        for field in self.fields:
            super().apply_css(property, css, field, selector)

    def rehint(self):
        minimum, _ = self.native.get_preferred_size()
        self.interface.intrinsic.width = at_least(minimum.width)
        self.interface.intrinsic.height = minimum.height
