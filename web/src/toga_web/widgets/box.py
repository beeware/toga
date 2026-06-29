from .base import Widget


class Box(Widget):
    def create(self):
        self.native = self._create_native_widget("div", classes=["container"])

    def add_child(self, child):
        self.native.appendChild(child.native)

    def insert_child(self, index, child):
        children = self.native.children
        if index < children.length:
            self.native.insertBefore(child.native, children.item(index))
        else:
            self.native.appendChild(child.native)

    def remove_child(self, child):
        self.native.removeChild(child.native)
        child.container = None
