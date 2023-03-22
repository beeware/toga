from .base import Widget


class Label(Widget):
    def create(self):
        self.native = self._create_native_widget("span")

    def get_text(self):
        return self.native.innerHTML

    def set_text(self, value):
        self.native.innerHTML = value

    def set_alignment(self, value):
        pass

    def rehint(self):
        pass
