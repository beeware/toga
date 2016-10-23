from toga.constants import LEFT_ALIGNED
from toga.interface import Label as LabelInterface

from .base import WidgetMixin
from ..libs import UILabel, NSTextAlignment, NSLineBreakByWordWrapping, CGSize


class Label(LabelInterface, WidgetMixin):
    def __init__(self, text, id=None, style=None, alignment=LEFT_ALIGNED):
        super().__init__(id=id, style=style, text=text, alignment=alignment)
        self._create()

    def create(self):
        self._impl = UILabel.new()
        self._impl._interface = self

        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setLineBreakMode_(NSLineBreakByWordWrapping)

        # Add the layout constraints
        self._add_constraints()

    def _set_alignment(self, value):
        self._impl.setTextAlignment_(NSTextAlignment(value))

    def _set_text(self, value):
        self._impl.setText_(value)

    def rehint(self):
        fitting_size = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.style.hint(
            height=fitting_size.height,
            width=(fitting_size.width, None)
        )
