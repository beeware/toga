from PySide6.QtCore import QCoreApplication, QEvent, QPoint, Qt
from PySide6.QtGui import QMouseEvent
from toga_qt.widgets.openglview import TogaOpenGLWidget

from .base import SimpleProbe


class OpenGLViewProbe(SimpleProbe):
    native_class = TogaOpenGLWidget
    buttons = frozenset()

    async def mouse_state(self, buttons: frozenset, x=0, y=0):
        methods = [
            self.left_mouse_down,
            self.middle_mouse_down,
            self.right_mouse_down,
        ]
        for button in buttons:
            method = methods[button]
            await method(x, y)

    async def reset_buttons(self, x=0, y=0):
        for method in [
            self.left_mouse_up,
            self.middle_mouse_up,
            self.right_mouse_up,
        ]:
            method(x, y)
        await self.redraw("Buttons cleared")

    async def left_mouse_down(self, x=0, y=0):
        self._emit_event(
            QEvent.Type.MouseButtonPress, x, y, button=Qt.MouseButton.LeftButton
        )

    async def left_mouse_up(self, x, y):
        self._emit_event(
            QEvent.Type.MouseButtonRelease, x, y, button=Qt.MouseButton.LeftButton
        )

    async def middle_mouse_down(self, x=0, y=0):
        self._emit_event(
            QEvent.Type.MouseButtonPress, x, y, button=Qt.MouseButton.MiddleButton
        )

    async def middle_mouse_up(self, x, y):
        self._emit_event(
            QEvent.Type.MouseButtonRelease, x, y, button=Qt.MouseButton.MiddleButton
        )

    async def right_mouse_down(self, x=0, y=0):
        self._emit_event(
            QEvent.Type.MouseButtonPress, x, y, button=Qt.MouseButton.RightButton
        )

    async def right_mouse_up(self, x, y):
        self._emit_event(
            QEvent.Type.MouseButtonRelease, x, y, button=Qt.MouseButton.RightButton
        )

    def _emit_event(
        self,
        event_type: QEvent.Type,
        x,
        y,
        button=Qt.MouseButton.LeftButton,
    ):
        pos = QPoint(x, y)
        global_pos = self.native.mapToGlobal(pos)
        event = QMouseEvent(
            event_type, pos, global_pos, button, button, Qt.KeyboardModifier.NoModifier
        )
        app = QCoreApplication.instance()
        app.postEvent(self.native, event)
