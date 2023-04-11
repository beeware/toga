from travertino.size import at_least

from ..libs import Gtk, gtk_alignment
from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = Gtk.Entry()
        self.native.connect("show", lambda event: self.refresh())
        self.native.connect("changed", self.gtk_on_change)
        self.native.connect("focus-in-event", self.gtk_focus_in_event)
        self.native.connect("focus-out-event", self.gtk_focus_in_event)

    def gtk_on_change(self, entry):
        if self.interface.on_change:
            self.interface.on_change(self.interface)

    def gtk_focus_in_event(self, entry, user_data):
        if self.interface.on_gain_focus:
            self.interface.on_gain_focus(self.interface)

    def gtk_focus_out_event(self, entry, user_data):
        if self.interface.on_lose_focus:
            self.interface.on_lose_focus(self.interface)

    def set_readonly(self, value):
        self.native.set_property("editable", not value)

    def set_placeholder(self, value):
        self.native.set_placeholder_text(value)

    def set_alignment(self, value):
        xalign, justify = gtk_alignment(value)
        self.native.set_alignment(
            xalign
        )  # Aligns the whole text block within the widget.

    def set_font(self, font):
        super().set_font(font)

    def get_value(self):
        return self.native.get_text()

    def set_value(self, value):
        self.native.set_text(value)

    def rehint(self):
        # print("REHINT", self,
        #     self._impl.get_preferred_width(), self._impl.get_preferred_height(),
        #     getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False)
        # )
        # width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = height[1]

    def set_on_change(self, handler):
        # No special handling required
        pass

    def set_on_gain_focus(self, handler):
        # No special handling required
        pass

    def set_on_lose_focus(self, handler):
        # No special handling required
        pass

    def set_error(self, error_message):
        self.interface.factory.not_implemented("TextInput.set_error()")

    def clear_error(self):
        self.interface.factory.not_implemented("TextInput.clear_error()")

    def is_valid(self):
        self.interface.factory.not_implemented("TextInput.is_valid()")
