from toga_web.libs import create_element

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = create_element(
            "span",
            id=f"toga_{self.interface.id}",
            classes=["label"],
            style=self.interface.style.__css__(),
        )

    def set_text(self, text):
        self.native.innerHTML = text

    def set_alignment(self, alignment):
        pass
