from PySide6.QtOpenGLWidgets import QOpenGLWidget
from travertino.size import at_least

from .base import Widget


class TogaOpenGLWidget(QOpenGLWidget):
    def __init__(self, impl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.impl = impl
        self.interface = impl.interface

    def initializeGL(self):
        print("here")
        self.interface.renderer.on_init(self.interface)

    def resizeGL(self, w, h):
        self._redraw()

    def paintGL(self):
        self._redraw()

    def _redraw(self):
        size = self.impl.native.size()
        width = size.width()
        height = size.height()
        self.interface.renderer.on_render(self.interface, size=(width, height))


class OpenGLView(Widget):
    def create(self):
        self.native = TogaOpenGLWidget(self)

    def redraw(self):
        self.native.update()

    def rehint(self):
        size = self.native.sizeHint()
        self.interface.intrinsic.width = at_least(
            max(size.width(), self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = at_least(
            max(size.height(), self.interface._MIN_HEIGHT)
        )
