from toga_web.libs import js

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = js.document.createElement("div")
        self.native.id = f"toga_{self.interface.id}"

        self.native.classList.add("toga")
        self.native.classList.add("box")
        self.native.classList.add("container")

        self.native.style = self.interface.style.__css__()

    def add_child(self, child):
        self.native.appendChild(child.native)
