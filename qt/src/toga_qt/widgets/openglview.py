from PySide6.QtCore import Qt
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QApplication
from travertino.size import at_least

from toga.widgets.openglview import LEFT, MIDDLE, RIGHT

from .base import Widget

BUTTON_MAP = {
    LEFT: Qt.MouseButton.LeftButton,
    MIDDLE: Qt.MouseButton.MiddleButton,
    RIGHT: Qt.MouseButton.RightButton,
}


class TogaOpenGLWidget(QOpenGLWidget):
    def __init__(self, impl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.impl = impl
        self.interface = impl.interface

    def initializeGL(self):
        self.interface.renderer.on_init(self.interface)

    def resizeGL(self, w, h):
        self._redraw()

    def paintGL(self):
        self._redraw()

    def _redraw(self):
        pixel_ratio = self.devicePixelRatio()
        size = self.impl.native.size()
        width = size.width() * pixel_ratio
        height = size.height() * pixel_ratio
        mouse_postion = self.mapFromGlobal(self.cursor().pos())
        pointer = (
            mouse_postion.x() * pixel_ratio,
            height - mouse_postion.y() * pixel_ratio,
        )
        qt_buttons = QApplication.mouseButtons()
        buttons = frozenset(
            {
                button
                for button, qt_button in BUTTON_MAP.items()
                if qt_buttons & qt_button
            }
        )
        self.interface.renderer.on_render(
            self.interface,
            size=(width, height),
            pointer=pointer,
            buttons=buttons,
        )


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
