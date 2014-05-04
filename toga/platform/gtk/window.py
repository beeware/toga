from __future__ import print_function, unicode_literals, absolute_import, division

from gi.repository import Gtk


class Window(object):
    _IMPL_CLASS = Gtk.Window

    def __init__(self, position=(100, 100), size=(640, 480)):
        self._impl = self._IMPL_CLASS()
        self._impl.connect("delete-event", self._on_close)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._impl.add(self._content._impl)

    def show(self):
        self._impl.show_all()

    def _on_close(self, widget, data):
        self.on_close()

    def on_close(self):
        pass
