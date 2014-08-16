from __future__ import print_function, absolute_import, division

from toga_cassowary.widget import Widget as CassowaryWidget


class Widget(CassowaryWidget):

    @property
    def _width_hint(self):
        return self._impl.get_preferred_width()

    @property
    def _height_hint(self):
        return self._impl.get_preferred_height()
