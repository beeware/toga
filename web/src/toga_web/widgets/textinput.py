from .base import Widget


class TextInput(Widget):
    def create(self):
        self._return_listener = None
        self.native = self._create_native_widget("sl-input")
        self.native.onkeyup = self.dom_keyup

    def dom_keyup(self, event):
        if event.key == "Enter":
            self.interface.on_confirm()

    def set_readonly(self, value):
        self.native.readOnly = value

    def set_placeholder(self, value):
        if value:
            self.native.placeholder = value

    def get_value(self):
        return self.native.value

    def set_value(self, value):
        self.native.value = value

    def set_font(self, font):
        pass

    def set_alignment(self, value):
        pass

    def rehint(self):
        pass

    def set_on_change(self, handler):
        pass

    def set_on_gain_focus(self, handler):
        pass

    def set_on_lose_focus(self, handler):
        pass

    def set_error(self, error_message):
        pass

    def clear_error(self):
        pass

    def is_valid(self):
        self.interface.factory.not_implemented("TextInput.is_valid()")
        return True
