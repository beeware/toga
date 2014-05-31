from __future__ import print_function, absolute_import, division

from toga.cassowary.widget import Container as CassowaryContainer


class Win32Container(object):
    def add(self, widget):
        pass

class Container(CassowaryContainer):
    def __init__(self):
        super(Container, self).__init__()
        self.window = None

    def _create_container(self):
        # No impl is requried for a container, but we need a placeholder
        # to keep the cross-platform logic happy.
        return Win32Container()

    def _resize(self, width, height):
        with self._layout_manager.layout(width, height):
            for widget in self._layout_manager.children:
                widget._resize()

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
