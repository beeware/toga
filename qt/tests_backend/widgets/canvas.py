from io import BytesIO

from PIL import Image
from PySide6.QtCore import QCoreApplication, QEvent, QPoint, Qt
from PySide6.QtGui import QMouseEvent
from toga_qt.widgets.canvas import TogaCanvas

from .base import SimpleProbe


class CanvasProbe(SimpleProbe):
    native_class = TogaCanvas

    def reference_variant(self, reference):
        if reference in {
            "multiline_text",
            "write_text",
            "write_text_and_path",
            "miter_join",
        }:
            return f"{reference}-qt"
        else:
            return reference

    def get_image(self):
        return Image.open(BytesIO(self.impl.get_image_data()))

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

    async def mouse_press(self, x, y):
        self._emit_event(
            QEvent.Type.MouseButtonPress, x, y, button=Qt.MouseButton.LeftButton
        )
        self._emit_event(
            QEvent.Type.MouseButtonRelease, x, y, button=Qt.MouseButton.LeftButton
        )

    async def mouse_activate(self, x, y):
        self._emit_event(
            QEvent.Type.MouseButtonPress, x, y, button=Qt.MouseButton.LeftButton
        )
        self._emit_event(
            QEvent.Type.MouseButtonRelease, x, y, button=Qt.MouseButton.LeftButton
        )
        self._emit_event(
            QEvent.Type.MouseButtonDblClick, x, y, button=Qt.MouseButton.LeftButton
        )
        self._emit_event(
            QEvent.Type.MouseButtonRelease, x, y, button=Qt.MouseButton.LeftButton
        )

    async def mouse_drag(self, x1, y1, x2, y2):
        self._emit_event(
            QEvent.Type.MouseButtonPress, x1, y1, button=Qt.MouseButton.LeftButton
        )
        self._emit_event(
            QEvent.Type.MouseMove,
            (x1 + x2) // 2,
            (y1 + y2) // 2,
            button=Qt.MouseButton.LeftButton,
        )
        self._emit_event(
            QEvent.Type.MouseButtonRelease, x2, y2, button=Qt.MouseButton.LeftButton
        )

    async def alt_mouse_press(self, x, y):
        self._emit_event(
            QEvent.Type.MouseButtonPress, x, y, button=Qt.MouseButton.RightButton
        )
        self._emit_event(
            QEvent.Type.MouseButtonRelease, x, y, button=Qt.MouseButton.RightButton
        )

    async def alt_mouse_drag(self, x1, y1, x2, y2):
        self._emit_event(
            QEvent.Type.MouseButtonPress, x1, y1, button=Qt.MouseButton.RightButton
        )
        self._emit_event(
            QEvent.Type.MouseMove,
            (x1 + x2) // 2,
            (y1 + y2) // 2,
            button=Qt.MouseButton.RightButton,
        )
        self._emit_event(
            QEvent.Type.MouseButtonRelease, x2, y2, button=Qt.MouseButton.RightButton
        )
