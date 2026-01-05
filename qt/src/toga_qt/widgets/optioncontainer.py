import asyncio

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QTabWidget
from travertino.size import at_least

from ..container import Container
from ..icons import IMPL_DICT
from .base import Widget


class OptionContainer(Widget):
    uses_icons = True

    def create(self):
        self.native = QTabWidget()
        self.native.currentChanged.connect(self.qt_current_changed)

        self.sub_containers = []

    def qt_current_changed(self, *args):
        self.interface.on_select()

    def add_option(self, index, text, widget, icon=None):
        sub_container = Container(on_refresh=self.content_refreshed)
        sub_container.content = widget

        self.sub_containers.insert(index, sub_container)
        if icon is None:
            self.native.insertTab(index, sub_container.native, text)
        else:
            self.native.insertTab(index, sub_container.native, icon._impl.native, text)

    def remove_option(self, index):
        self.native.removeTab(index)
        self.sub_containers[index].content = None
        del self.sub_containers[index]

    def set_option_enabled(self, index, enabled):
        self.native.setTabEnabled(index, enabled)

    def is_option_enabled(self, index):
        return self.native.isTabEnabled(index)

    def set_option_text(self, index, value):
        self.native.setTabText(index, value)

    def get_option_text(self, index):
        return self.native.tabText(index)

    def set_option_icon(self, index, value):
        if value is None:
            self.native.setTabIcon(index, QIcon())
        else:
            self.native.setTabIcon(index, value._impl.native)

    def get_option_icon(self, index):
        impl = IMPL_DICT.get(self.native.tabIcon(index).cacheKey(), None)
        if impl is None:
            return None
        else:
            return impl.interface

    def get_current_tab_index(self):
        return self.native.currentIndex()

    def set_current_tab_index(self, current_tab_index):
        return self.native.setCurrentIndex(current_tab_index)

    def rehint(self):
        size = self.native.minimumSizeHint()
        self.interface.intrinsic.width = at_least(
            max(size.width(), self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = at_least(
            max(size.height(), self.interface._MIN_HEIGHT)
        )

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        for item in self.interface.content:
            item.content.refresh()

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
