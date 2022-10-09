from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = self._create_native_widget("input", classes=["btn-block"])

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
