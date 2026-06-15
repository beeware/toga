from .base import Widget


class OpenGLView(Widget):
    def create(self):
        self._action("create OpenGLView")
        self.interface.renderer.on_init(self.interface)

    # Resize handlers

    def redraw(self):
        self._action("redraw")
        self.interface.renderer.on_render(self.interface, self.get_size())

    def simulate_resize(self):
        self.interface.renderer.on_render(self.interface, self.get_size())
