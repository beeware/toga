from .base import Widget

class NumberInput(Widget):
    def create(self):
        self._return_listener = None
        self.native = self._create_native_widget("sl-input")
        self.native.type = 'number'
        self.native.value = None
        self.native.onkeyup = self.dom_keyup

    def dom_keyup(self, event):
        if event.key == "Enter":
            self.interface.on_confirm()

    def get_readonly(self, value):
        return self.native.readOnly

    def set_readonly(self, value):
        self.native.readOnly = value

    def set_step(self, step):
        self.native.step = step

    def set_min_value(self, value):
        self.native.min = value

    def set_max_value(self, value):
        self.native.max = value

    def get_value(self):
        if self.native.value == '' or self.native.value is None:
            return None
        else:
            return float(self.native.value)

    def set_value(self, value):
        self.native.value = value

    def set_text_align(self, value):
        pass