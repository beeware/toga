from toga_web.libs import js

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = js.document.createElement("span")
        self.native.id = f"toga_{self.interface.id}"

        self.native.classList.add("toga")
        self.native.classList.add("label")

        self.native.style = self.interface.style.__css__()

    def set_text(self, text):
        self.native.innerHTML = text

    def set_alignment(self, alignment):
        pass
