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
        self.native.styles.width = 20

    def get_readonly(self):
        return False

    def set_readonly(self, value):
        pass

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
