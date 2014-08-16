from __future__ import print_function, absolute_import, division

from toga_cassowary.widget import Container as CassowaryContainer


class Win32Container(object):
    def add(self, widget):
        pass

class Container(CassowaryContainer):

    def _create_container(self):
        # No impl is requried for a container, but we need a placeholder
        # to keep the cross-platform logic happy.
        return Win32Container()

    def _resize(self, width, height):
        with self._layout_manager.layout(width, height):
            for widget in self._layout_manager.children:
                widget._resize()

    def _set_app(self, app):
        for child in self.children:
            child.app = app

    def _set_window(self, window):
        for child in self.children:
            child.window = window
            child.startup()

    @property
    def _width_hint(self):
        width = self._layout_manager.bounding_box.width.value
        print("PREFERRED WIDTH", width)
        return width, width

    @property
    def _height_hint(self):
        height = self._layout_manager.bounding_box.height.value
        print("PREFERRED HEIGHT", height)
        return height, height
