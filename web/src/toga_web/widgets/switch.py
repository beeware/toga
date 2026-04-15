from toga_web.libs import create_proxy

from .base import Widget


class Switch(Widget):
    def create(self):
        self.native = self._create_native_widget("wa-switch")
        self.native.addEventListener("change", create_proxy(self.dom_onchange))

    def dom_onchange(self, event):
        self.interface.on_change()

    def get_text(self):
        return self.native.innerHTML

    def set_text(self, text):
        self.native.innerHTML = text

    def get_value(self):
        try:
            return self.native.checked
        except AttributeError:
            return False

    def set_value(self, value):
        old_value = self.get_value()
        self.native.checked = value
        if value != old_value:
            self.interface.on_change()
