from toga_web.libs import js

from .base import Widget


class TextInput(Widget):

    def create(self):
        self.native = js.document.createElement("input")
        self.native.id = f"toga_{self.interface.id}"

        self.native.classList.add("toga")
        self.native.classList.add("input")
        self.native.classList.add("btn-block")

        self.native.style = self.interface.style.__css__()

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
