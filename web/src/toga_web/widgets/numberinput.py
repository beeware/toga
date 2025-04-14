from .base import Widget


class NumberInput(Widget):
    def create(self):
        self._return_listener = None
        self.native = self._create_native_widget("sl-input")
        self.native.type = "number"
        self.native.value = None
        self.native.onblur = self.lost_focus

    def lost_focus(self, event):
        print(self.native.value == "-")
        if self.native.value == "":
            self.native.value = None

        if self.native.value is not None and self.native.min is not None:
            if float(self.native.value) < self.native.min:
                self.native.value = self.native.min

        if self.native.value is not None and self.native.max is not None:
            if float(self.native.value) > self.native.max:
                self.native.value = self.native.max

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
        if self.native.value == "" or self.native.value is None:
            return None
        else:
            return float(self.native.value)

    def set_value(self, value):
        self.native.value = value

    def set_text_align(self, value):
        pass
