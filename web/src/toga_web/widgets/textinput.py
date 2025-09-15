from toga_web.libs import create_proxy

from .base import Widget


class TextInput(Widget):
    def create(self):
        self._return_listener = None
        self.native = self._create_native_widget("sl-input")
        self.native.onkeyup = self.dom_onkeyup
        self.native.addEventListener("onkeyup", create_proxy(self.dom_onkeyup))
        self.native.addEventListener("sl-change", create_proxy(self.dom_sl_change))

    def dom_onkeyup(self, event):
        self.interface.on_change()

    def dom_sl_change(self, event):
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

    def set_text_align(self, value):
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
