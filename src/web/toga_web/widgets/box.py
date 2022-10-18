from .base import Widget


class Box(Widget):
    def create(self):
        self.native = self._create_native_widget("div", classes=["container"])

    def add_child(self, child):
        self.native.appendChild(child.native)
