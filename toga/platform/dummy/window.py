from __future__ import print_function, unicode_literals, absolute_import, division


class Window(object):
    def __init__(self, position=(100, 100), size=(640, 480)):
        self._content = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget

    def show(self):
        pass

    def on_close(self):
        pass
