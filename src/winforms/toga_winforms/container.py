from .libs import *


class Container:
    def __init__(self):
        self._impl = WinForms.Panel()
        self._content = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content._container = self

    @property
    def root_content(self):
        return self._content

    @root_content.setter
    def root_content(self, widget):
        self._content = widget
        self._content._container = self

    def _update_layout(self, **style):
        if self._content:
            self._content._update_layout(**style)
