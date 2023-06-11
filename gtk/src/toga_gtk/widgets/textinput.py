from travertino.size import at_least

from toga.keys import Key
from toga_gtk.keys import toga_key

from ..libs import Gtk, gtk_alignment
from .base import Widget


class TextInput(Widget):
    def create(self):
        focus_controller = Gtk.EventControllerFocus()
        focus_controller.connect("enter", self.gtk_focus_in_event)
        focus_controller.connect("leave", self.gtk_focus_out_event)

        key_press_controller = Gtk.EventControllerKey()
        key_press_controller.connect("key-pressed", self.gtk_key_press_event)

        self.native = Gtk.Entry()
        self.native.connect("changed", self.gtk_on_change)
        self.native.add_controller(focus_controller)
        self.native.add_controller(key_press_controller)

    def gtk_on_change(self, entry):
        self.interface.on_change(self.interface)
        self.interface._validate()

    def gtk_focus_in_event(self, *args):
        self.interface.on_gain_focus(self.interface)

    def gtk_focus_out_event(self, *args):
        self.interface.on_lose_focus(self.interface)

    def gtk_key_press_event(self, *args):
        key_pressed = toga_key(args[0])
        if key_pressed and key_pressed["key"] in {Key.ENTER, Key.NUMPAD_ENTER}:
            self.interface.on_confirm(None)

    def get_readonly(self):
        return not self.native.get_property("editable")

    def set_readonly(self, value):
        self.native.set_property("editable", not value)

    def get_placeholder(self):
        return self.native.get_placeholder_text()

    def set_placeholder(self, value):
        self.native.set_placeholder_text(value)

    def set_alignment(self, value):
        xalign, justify = gtk_alignment(value)
        self.native.set_alignment(
            xalign
        )  # Aligns the whole text block within the widget.

    def get_value(self):
        return self.native.get_text()

    def set_value(self, value):
        self.native.set_text(value)

    def rehint(self):
        # print("REHINT", self,
        #     self._impl.get_preferred_size()[0],
        #     self._impl.get_preferred_size()[1],
        #     getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False)
        # )
        _, size = self.native.get_preferred_size()

        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = size.height

    def set_error(self, error_message):
        self.native.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "error")

    def clear_error(self):
        self.native.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)

    def is_valid(self):
        return self.native.get_icon_name(Gtk.EntryIconPosition.SECONDARY) is None
