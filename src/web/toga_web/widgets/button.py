
from toga_web.libs import js

from .base import Widget


class Button(Widget):
    def create(self):
        self.native = js.document.createElement("button")
        self.native.id = f"toga_{self.interface.id}"

        self.native.classList.add("toga")
        self.native.classList.add("button")
        self.native.classList.add("btn-block")

        self.native.style = self.interface.style.__css__()

        self.native.onclick = self.dom_onclick

    def dom_onclick(self, event):
        if self.interface.on_press:
            self.interface.on_press(self.interface)

    def set_text(self, text):
        self.native.innerHTML = text

    def set_enabled(self, value):
        pass

    def set_background_color(self, value):
        pass

    def set_on_press(self, handler):
        pass
        # register_handler('mouse_press', self.interface, handler)

    def rehint(self):
        pass
