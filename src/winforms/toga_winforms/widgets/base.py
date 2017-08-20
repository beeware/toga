# from ..container import Constraints
from ..libs import *


class WidgetMixin:
    def _set_app(self, app):
        pass

    def _set_window(self, window):
        pass

    def _set_container(self, container):
        if self._impl:
            self._container._impl.Controls.Add(self._impl)

        self.rehint()

    def _add_child(self, child):
        if self._container:
            child._set_container(self._container)

    def _apply_layout(self):
        if self._impl:
            self._impl.Size = Size(int(self.layout.width), int(self.layout.height))
            self._impl.Location = Point(int(self.layout.absolute.left), int(self.layout.absolute.top))

    def rehint(self):
        pass

    def _set_font(self, font):
        pass
