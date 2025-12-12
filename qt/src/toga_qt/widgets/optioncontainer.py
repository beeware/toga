from PySide6.QtWidgets import QTabWidget
from travertino.size import at_least

from ..container import Container
from .base import Widget


class OptionContainer(Widget):
    uses_icons = False

    def create(self):
        self.native = QTabWidget()
        self.native.currentChanged.connect(self.qt_current_changed)
        self.sub_containers = []

    def qt_current_changed(self, *args):
        self.interface.on_select()

    def add_option(self, index, text, widget, icon):
        sub_container = Container()
        sub_container.content = widget

        self.sub_containers.insert(index, sub_container)
        if icon is None:
            self.native.insertTab(index, sub_container.native, text)
        else:  # pragma: nocover
            # This shouldn't ever be invoked, but it's included for completeness.
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

    def set_option_icon(self, index, value):  # pragma: nocover
        # This shouldn't ever be invoked, but it's included for completeness.
        self.native.setTabIcon(index, value._impl.native)

    def get_option_icon(self, index):
        # Icons aren't supported right now
        # return self.native.tabIcon(index)
        return None

    def get_current_tab_index(self):
        return self.native.currentIndex()

    def set_current_tab_index(self, current_tab_index):
        return self.native.setCurrentIndex(current_tab_index)

    def rehint(self):
        size = self.native.sizeHint()
        self.interface.intrinsic.width = at_least(
            max(size.width(), self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = at_least(
            max(size.height(), self.interface._MIN_HEIGHT)
        )
