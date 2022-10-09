from .base import Widget


class Label(Widget):
    def create(self):
        self.native = self._create_native_widget("span")

    def set_text(self, text):
        self.native.innerHTML = text

    def set_alignment(self, alignment):
        pass
