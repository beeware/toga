from toga_web.libs import create_proxy

from .base import Widget


class DateInput(Widget):
    def create(self):
        self._return_listener = None
        self.native = self._create_native_widget("sl-input")
        self.native.setAttribute("type", "date")
        self.native.addEventListener("sl-change", create_proxy(self.dom_onchange))

    def set_value(self, value):
        self.native.value = value

    def dom_onchange(self, event):
        self.interface.on_change(None)

    def get_min_date(self):
        return self.native.min

    def get_max_date(self):
        return self.native.max

    def set_min_date(self, value):
        # you might have to
        self.native.min = value

    def set_max_date(self, value):
        # you might have to
        self.native.max = value
