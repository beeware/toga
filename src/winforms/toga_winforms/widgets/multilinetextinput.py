from __future__ import print_function, absolute_import, division

from toga.interface import MultilineTextInput as MultilineTextInputInterface

from ..libs import *

from .base import WidgetMixin


class MultilineTextInput(MultilineTextInputInterface, WidgetMixin):
    # because https://stackoverflow.com/a/612234
    _IMPL_CLASS = WinForms.RichTextBox

    def __init__(self, id=None, style=None, initial=None, placeholder=None, readonly=False, _delegate=None):
        self._delegate = _delegate
        super().__init__(id=id, style=style, initial=initial, placeholder=placeholder, readonly=readonly)
        self._create()

    def create(self):
        self._impl = self._IMPL_CLASS()
        self._impl.Multiline = True

    def _set_readonly(self, value):
        self._impl.ReadOnly = value

    def _set_placeholder(self, value):
        # self._impl.cell.placeholderString = self._placeholder
        pass

    @property
    def value(self):
        return self._impl.Text

    @value.setter
    def value(self, value):
        self._impl.Text = value
        self.rehint()

    def rehint(self):
        # Width must be > 100
        s = Size(self._impl.Width, 0)
        self.style.hint(
            height=self._impl.GetPreferredSize(s).Height,
            min_width=100,
        )

