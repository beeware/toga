from toga_web.libs import create_proxy

from .base import Widget


class Button(Widget):
    def create(self):
        self.native = self._create_native_widget("sl-button")
        self.native.addEventListener("click", create_proxy(self.dom_click))

    def dom_click(self, event):
        self.interface.on_press()

    def get_text(self):
        return self.native.innerHTML

    def set_text(self, text):
        self.native.innerHTML = text

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        self._icon = icon
        if icon:
            self.interface.factory.not_implemented("Button.icon")

    def set_enabled(self, value):
        self.native.disabled = not value

    def set_background_color(self, value):
        pass

    def rehint(self):
        pass
