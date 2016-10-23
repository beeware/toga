from __future__ import print_function, absolute_import, division

from ..libs import *
from ctypes import c_wchar_p

from .base import Widget

class TextInput(Widget):
    window_class = 'edit'
    default_style = WS_VISIBLE | WS_CHILD | WS_TABSTOP| ES_AUTOHSCROLL

    def __init__(self, initial=None, placeholder=None, readonly=False):
        super(TextInput, self).__init__(text=initial)
        self.placeholder = placeholder #not used on win32!
        self._readonly = readonly

    def startup(self):
        super(TextInput, self).startup()
        self.readonly = self._readonly

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        user32.SendMessageW(self._impl, EM_SETREADONLY, int(value), 0)

    @property
    def value(self):
        length = user32.GetWindowTextLengthW(self._impl)
        text = user32.GetWindowTextW(self._impl, length)
        return text.value

    @value.setter
    def value(self, value):
        value = c_wchar_p(value)
        user32.SetWindowTextW(self._impl, value)
