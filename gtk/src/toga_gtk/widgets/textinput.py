from travertino.size import at_least

from toga.keys import Key
from toga_gtk.keys import toga_key

from ..libs import GTK_VERSION, Gtk, gtk_text_align
from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = Gtk.Entry()

        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.connect("changed", self.gtk_on_change)
            self.native.connect("focus-in-event", self.gtk_focus_in_event)
            self.native.connect("focus-out-event", self.gtk_focus_out_event)
            self.native.connect("key-press-event", self.gtk_key_press_event)
        else:  # pragma: no-cover-if-gtk3
            pass

    def gtk_on_change(self, *_args):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.interface._value_changed()
        else:  # pragma: no-cover-if-gtk3
            self.interface._value_changed(self.interface)

    def gtk_focus_in_event(self, *_args):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.interface.on_gain_focus()
        else:  # pragma: no-cover-if-gtk3
            self.interface.on_gain_focus(self.interface)

    def gtk_focus_out_event(self, *_args):
        self.interface.on_lose_focus()

    def gtk_key_press_event(self, _, key_val, *_args):
        key_pressed = toga_key(key_val)
        if key_pressed and key_pressed["key"] in {Key.ENTER, Key.NUMPAD_ENTER}:
            self.interface.on_confirm()

    def get_readonly(self):
        return not self.native.get_property("editable")

    def set_readonly(self, value):
        self.native.set_property("editable", not value)

    def get_placeholder(self):
        return self.native.get_placeholder_text()

    def set_placeholder(self, value):
        self.native.set_placeholder_text(value)

    def set_text_align(self, value):
        xalign, justify = gtk_text_align(value)
        self.native.set_alignment(
            xalign
        )  # Aligns the whole text block within the widget.

    def get_value(self):
        return self.native.get_text()

    def set_value(self, value):
        self.native.set_text(value)

    def rehint(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            # print(
            #     "REHINT",
            #     self,
            #     self._impl.get_preferred_width(),
            #     self._impl.get_preferred_height(),
            #     getattr(self, "_fixed_height", False),
            #     getattr(self, "_fixed_width", False),
            # )
            width = self.native.get_preferred_width()
            height = self.native.get_preferred_height()

            self.interface.intrinsic.width = at_least(
                max(self.interface._MIN_WIDTH, width[1])
            )
            self.interface.intrinsic.height = height[1]
        else:  # pragma: no-cover-if-gtk3
            pass

    def set_error(self, error_message):
        self.native.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "error")

    def clear_error(self):
        self.native.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)

    def is_valid(self):
        return self.native.get_icon_name(Gtk.EntryIconPosition.SECONDARY) is None
