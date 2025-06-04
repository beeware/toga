from travertino.size import at_least

from toga.keys import Key
from toga_gtk.keys import toga_key

from ..libs import Gtk, gtk_text_align
from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = Gtk.Entry()

        self.native.connect("changed", self.gtk_on_change)
        self.native.connect("focus-in-event", self.gtk_focus_in_event)
        self.native.connect("focus-out-event", self.gtk_focus_out_event)
        self.native.connect("key-press-event", self.gtk_key_press_event)

    def gtk_on_change(self, *_args):
        self.interface._value_changed()

    def gtk_focus_in_event(self, *_args):
        self.interface.on_gain_focus()

    def gtk_focus_out_event(self, *_args):
        self.interface.on_lose_focus()

    def gtk_key_press_event(self, _entry, event):
        key_pressed = toga_key(event.keyval, event.state)
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

    def set_error(self, error_message):
        self.native.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "error")

    def clear_error(self):
        self.native.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)

    def is_valid(self):
        return self.native.get_icon_name(Gtk.EntryIconPosition.SECONDARY) is None
