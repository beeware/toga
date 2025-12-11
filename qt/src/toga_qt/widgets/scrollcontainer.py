from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea
from travertino.constants import TRANSPARENT
from travertino.size import at_least

from ..container import Container
from .base import Widget


class ScrollContainer(Widget):
    def create(self):
        self.native = QScrollArea()
        self.native.setWidgetResizable(False)

        self.native.setAutoFillBackground(True)
        # Background is not autofilled by default; but since we're
        # enabling it here, let the default color be transparent
        # so it autofills nothing by default.
        self._default_background_color = TRANSPARENT

        self.document_container = Container(
            on_refresh=self.content_refreshed,
        )
        self.native.setWidget(self.document_container.native)
        self.native.setWidgetResizable(True)
        self.document_container.native.show()

        self.native.verticalScrollBar().valueChanged.connect(self.qt_on_changed)
        self.native.horizontalScrollBar().valueChanged.connect(self.qt_on_changed)

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
        size = self.native.viewportSizeHint()
        self.interface.intrinsic.width = at_least(
            max(size.width(), self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = at_least(
            max(size.height(), self.interface._MIN_HEIGHT)
        )

    def content_refreshed(self, container):
        min_width = self.interface.content.layout.min_width
        min_height = self.interface.content.layout.min_height
        self.document_container.native.setMinimumSize(min_width, min_height)
        self.document_container.min_width = min_width
        self.document_container.min_height = min_height
