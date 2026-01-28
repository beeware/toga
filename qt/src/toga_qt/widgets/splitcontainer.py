import asyncio

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplitter
from travertino.size import at_least

from ..container import Container
from .base import Widget


class SplitContainer(Widget):
    def create(self):
        self.native = QSplitter()
        self.native.setOrientation(Qt.Orientation.Vertical)
        self.native.splitterMoved.connect(self.qt_splitter_moved)

        self.sub_containers = [
            Container(on_refresh=self.content_refreshed),
            Container(on_refresh=self.content_refreshed),
        ]
        for container in self.sub_containers:
            self.native.addWidget(container.native)
            container.native.show()
        self.native.setChildrenCollapsible(False)

        self._split_proportion = 0.5

    def qt_splitter_moved(self, pos, index):
        self.interface.refresh()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)

        # If we've got a pending split to apply, set the split position.
        # However, only do this if the layout is more than the min size;
        # there are initial 0-sized layouts for which the split is meaningless.
        if (
            self._split_proportion
            and width >= self.interface._MIN_WIDTH
            and height > self.interface._MIN_HEIGHT
        ):
            if self.interface.direction == self.interface.VERTICAL:
                sizes = [
                    int(self._split_proportion * width),
                    width - int(self._split_proportion * width),
                ]
            else:
                sizes = [
                    int(self._split_proportion * height),
                    height - int(self._split_proportion * height),
                ]
            self.native.setSizes(sizes)
            self._split_proportion = None
        for container in self.sub_containers:
            if container.content:
                container.content.interface.refresh()

    def content_refreshed(self, container):
        container.native.setMinimumSize(
            container.content.interface.layout.min_width,
            container.content.interface.layout.min_height,
        )
        # re-layout and schedule a second refresh if intrinsic size has changed
        prev_intrinsic_size = (
            self.interface.intrinsic.width,
            self.interface.intrinsic.height,
        )
        self.rehint()
        intrinsic_size = (
            self.interface.intrinsic.width,
            self.interface.intrinsic.height,
        )
        if prev_intrinsic_size != intrinsic_size:
            asyncio.get_running_loop().call_soon_threadsafe(self.interface.refresh)

    def set_content(self, content, flex):
        # Clear any existing content
        for container in self.sub_containers:
            container.content = None

        # Add all children to the content widget.
        for position, widget in enumerate(content):
            self.sub_containers[position].content = widget

        # We now know the initial positions of the split. However, we can't *set* the
        # because Qt requires a pixel position, and the widget isn't visible yet. So -
        # store the split; and when we do our first layout, apply that proportion.
        # print(flex)
        self._split_proportion = flex[0] / sum(flex)

    def get_direction(self):
        # Qt uses the orientation of the layout, not the handle
        if self.native.orientation() == Qt.Orientation.Vertical:
            return self.interface.HORIZONTAL
        else:
            return self.interface.VERTICAL

    def set_direction(self, value):
        # Qt uses the orientation of the layout, not the handle
        if value == self.interface.VERTICAL:
            self.native.setOrientation(Qt.Orientation.Horizontal)
        else:
            self.native.setOrientation(Qt.Orientation.Vertical)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.native.minimumSizeHint().width())
        self.interface.intrinsic.height = at_least(
            self.native.minimumSizeHint().height()
        )
