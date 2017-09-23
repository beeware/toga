from .libs import *


class Container:
    def __init__(self):
        self.native = WinForms.Panel()
        self._content = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.container = self

    @property
    def root_content(self):
        return self._content

    @root_content.setter
    def root_content(self, widget):
        self._content = widget
        self._content.container = self

    def update_layout(self, **style):
        if self.content:
            self.content.interface._update_layout(**style)
