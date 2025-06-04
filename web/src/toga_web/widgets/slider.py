from toga_web.libs import create_proxy

from .base import Widget


class Slider(Widget):
    def create(self):
        self.native = self._create_native_widget("sl-range")
        self.native.addEventListener("sl-input", create_proxy(self.dom_sl_input))
        self.native.addEventListener(
            "pointerdown", create_proxy(self.dom_onpointerdown)
        )
        self.native.addEventListener("pointerup", create_proxy(self.dom_onpointerup))

    def dom_sl_input(self, event):
        self.interface.value = float(self.native.value)
        if self.interface.on_change:
            self.interface.on_change()

    def dom_onpointerdown(self, event):
        self.interface.on_press()

    def dom_onpointerup(self, event):
        self.interface.on_release()

    def get_value(self):
        return float(self.native.value)

    def set_value(self, value):
        self.native.value = value

    def get_min(self):
        return float(self.native.min)

    def set_min(self, value):
        self.native.min = value

    def get_max(self):
        return float(self.native.max)

    def set_max(self, value):
        self.native.max = value

    def get_tick_count(self):
        step = float(self.native.step or 0)
        return int((float(self.native.max) - float(self.native.min)) / step) + 1

    def set_tick_count(self, tick_count):
        if tick_count:
            self.native.step = (self.interface.max - self.interface.min) / (
                tick_count - 1
            )
        else:
            self.native.step = 0.0001
