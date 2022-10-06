
from toga_web.libs import create_element

from .base import Widget


class Button(Widget):
    def create(self):
        self.native = create_element(
            "button",
            id = f"toga_{self.interface.id}",
            classes=["button", "btn-block"],
            style=self.interface.style.__css__(),
        )

        self.native.onclick = self.dom_onclick

    def dom_onclick(self, event):
        if self.interface.on_press:
            self.interface.on_press(self.interface)

    def set_text(self, text):
        self.native.innerHTML = text

    def set_enabled(self, value):
        self.native.disabled = not value

    def set_background_color(self, value):
        pass

    def set_on_press(self, handler):
        pass

    def rehint(self):
        pass
