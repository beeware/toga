from toga_web.libs import create_element

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = create_element(
            "div",
            id=f"toga_{self.interface.id}",
            classes=["box", "container"],
            style=self.interface.style.__css__()
        )

    def add_child(self, child):
        self.native.appendChild(child.native)
