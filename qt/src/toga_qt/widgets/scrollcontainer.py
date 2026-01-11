from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QScrollArea
from travertino.constants import TRANSPARENT
from travertino.size import at_least

from ..container import Container
from .base import Widget


class ViewportMonitor(QObject):
    def __init__(self, impl):
        self.impl = impl
        super().__init__()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Resize:
            self.impl.qt_viewport_resize()
        return super().eventFilter(obj, event)


class ScrollContainer(Widget):
    def create(self):
        self.native = QScrollArea()

        self.native.setAutoFillBackground(True)
        # Background is not autofilled by default; but since we're
        # enabling it here, let the default color be transparent
        # so it autofills nothing by default.
        self._default_background_color = TRANSPARENT

        self.document_container = Container(
            layout_native=self.native.viewport(),
            on_refresh=self.content_refreshed,
        )
        self.native.setWidget(self.document_container.native)
        self.document_container.native.show()
        self.monitor = ViewportMonitor(self)
        self.native.viewport().installEventFilter(self.monitor)

        self.native.verticalScrollBar().valueChanged.connect(self.qt_on_changed)
        self.native.horizontalScrollBar().valueChanged.connect(self.qt_on_changed)

    def qt_viewport_resize(self):
        if self.interface.content is not None:
            self.interface.content.refresh()

    def qt_on_changed(self, *args):
        self.interface.on_scroll()

    def set_content(self, widget):
        self.document_container.content = widget

    def get_horizontal(self):
        return (
            self.native.horizontalScrollBarPolicy()
            != Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

    def set_horizontal(self, value):
        self.native.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
            if value
            else Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
        )
        if not value:
            self.native.horizontalScrollBar().setValue(0)

    def get_vertical(self):
        return (
            self.native.verticalScrollBarPolicy()
            != Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

    def set_vertical(self, value):
        self.native.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
            if value
            else Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
        )
        if not value:
            self.native.verticalScrollBar().setValue(0)

    def get_max_vertical_position(self):
        return self.native.verticalScrollBar().maximum()

    def get_vertical_position(self):
        return self.native.verticalScrollBar().value()

    def get_max_horizontal_position(self):
        return self.native.horizontalScrollBar().maximum()

    def get_horizontal_position(self):
        return self.native.horizontalScrollBar().value()

    def set_position(self, horizontal_position, vertical_position):
        self.native.horizontalScrollBar().setValue(horizontal_position)
        self.native.verticalScrollBar().setValue(vertical_position)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def content_refreshed(self, container):
        width = self.native.viewport().width()
        height = self.native.viewport().height()

        if self.interface.horizontal:
            width = max(self.interface.content.layout.width, width)

        if self.interface.vertical:
            height = max(self.interface.content.layout.height, height)

        self.document_container.native.setFixedSize(width, height)
