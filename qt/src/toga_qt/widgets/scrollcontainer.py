from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QScrollArea
from travertino.constants import TRANSPARENT
from travertino.size import at_least

from ..container import Container
from .base import Widget


class TogaScrollArea(QScrollArea):
    def __init__(self, interface, *args, **kwargs):
        self.interface = interface
        super().__init__(*args, **kwargs)

    def wheelEvent(self, event):
        if event.type() == QEvent.Type.Wheel:
            # Constrain mouse wheel scrolling (or trackpad scrolling)
            # Only scroll in allowed directions.
            angle_delta = event.angleDelta()
            pixel_delta = event.pixelDelta()
            if not self.interface.horizontal:
                # zero out x delta
                angle_delta.setX(0)
                pixel_delta.setX(0)
            if not self.interface.vertical:
                # zero out y delta
                angle_delta.setY(0)
                pixel_delta.setY(0)
            # Can't modify an event, so need to create new one.
            event = QWheelEvent(
                event.position(),
                event.globalPosition(),
                pixel_delta,
                angle_delta,
                event.buttons(),
                event.modifiers(),
                event.phase(),
                event.inverted(),
                # event.source(),
                # Qt.MouseEventSource.MouseEventNotSynthesized,
                device=event.device(),
            )
        # continue doing whatever we were going to do.
        super().wheelEvent(event)


class ScrollContainer(Widget):
    def create(self):
        self.native = TogaScrollArea(self.interface)

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
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        if self.interface.content is not None:
            self.interface.content.refresh()

    def content_refreshed(self, container):
        # get sizes of decorations - assume horizontal / vertical symmetry
        scroll_size = self.native.horizontalScrollBar().height()
        margins = self.native.contentsMargins()
        margin_size = margins.left() + margins.right()

        # get size of area inside
        # (can't use viewport, as it may be out of date about scrollbar visibility)
        size = self.native.size()
        area_width = size.width() - margin_size
        area_height = size.height() - margin_size

        # get the minimum size of the content
        content_width = self.interface.content.layout.min_width
        content_height = self.interface.content.layout.min_height

        # start with available area
        height = area_height
        width = area_width

        # If we will get a scrollbar adjust height and width
        if content_width > area_width and self.interface.horizontal:
            # remove space for scrollbar
            height -= scroll_size
        if content_height > area_height and self.interface.vertical:
            # remove space for scrollbar
            width -= scroll_size

        # If we can scroll, grab the extra space
        if self.interface.horizontal:
            width = max(self.interface.content.layout.min_width, width)
        if self.interface.vertical:
            height = max(self.interface.content.layout.min_height, height)

        self.document_container.native.setMinimumSize(width, height)
