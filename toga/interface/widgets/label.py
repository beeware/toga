from .base import Widget
from toga.constants import *


class Label(Widget):
    def __init__(self, text, id=None, style=None, alignment=LEFT_ALIGNED):
        super().__init__(id=id, style=style, text=text, alignment=alignment)

    def _configure(self, text, alignment):
        self.text = text
        self.alignment = alignment
        
    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = value
        self._set_alignment(value)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if value is None:
            self._text = ''
        else:
            self._text = str(value)
        self._set_text(value)
        self.rehint()

    def _set_alignment(self, value):
        raise NotImplementedError('Label widget must define _set_alignment()')

    def _set_text(self, value):
        raise NotImplementedError('Label widget must define _set_text()')
