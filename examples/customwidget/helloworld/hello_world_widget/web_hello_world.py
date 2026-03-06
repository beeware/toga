from toga_web.widgets.base import Widget


class HelloWorld(Widget):
    def create(self):
        self.native = self._create_native_widget("span")
        self.native.innerHTML = "Hello World!"

    def set_text_align(self, value):
        pass

    def rehint(self):
        pass
