from textual.widgets import Input as TextualInput

from .base import Widget


class TogaInput(TextualInput):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface
        self.impl = impl


class TextInput(Widget):
    def create(self):
        self.native = TogaInput(self)

    def get_readonly(self):
        return self.native.disabled

    def set_readonly(self, value):
        self.native.disabled = value

    def get_placeholder(self):
        return self.native.placeholder

    def set_placeholder(self, value):
        self.native.placeholder = value

    def get_value(self):
        return self.native.value

    def set_value(self, value):
        self.native.value = value

    def set_error(self, error_message):
        pass

    def clear_error(self):
        pass

    def is_valid(self):
        return True
