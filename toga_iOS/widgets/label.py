from ..libs import UILabel, NSTextAlignment, NSLineBreakByWordWrapping, CGSize
from .base import Widget
from toga.constants import *


class Label(Widget):
    def __init__(self, text=None, alignment=LEFT_ALIGNED, style=None):
        super().__init__(style=style)

        self.startup()

        self.alignment = alignment
        self.text = text

    def startup(self):
        self._impl = UILabel.new()

        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setLineBreakMode_(NSLineBreakByWordWrapping)

        # Height of a button is known. Set the minimum width
        # of a button to be a square
        fitting_size = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.style.hint(
            height=fitting_size.height,
            width=(fitting_size.width, None)
        )

        # Add the layout constraints
        self._add_constraints()

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = value
        self._impl.setTextAlignment_(NSTextAlignment(self._alignment))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._impl.setText_(self._text)
