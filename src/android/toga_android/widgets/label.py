from toga.constants import *
from toga.interface import Label as LabelInterface

from android.view import Gravity

from .base import WidgetMixin


class TogaLabel(extends=android.widget.TextView):
    @super({context: android.content.Context})
    def __init__(self, context, interface):
        self._interface = interface


class Label(LabelInterface, WidgetMixin):
    def __init__(self, text, id=None, style=None, alignment=LEFT_ALIGNED):
        super().__init__(id=id, style=style, text=text, alignment=alignment)

    def create(self):
        print("create label")
        self._impl = TogaLabel(self.app._impl, self)
        self._impl.setSingleLine()

    def _set_alignment(self, value):
        self._impl.setGravity({
                LEFT_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.LEFT,
                RIGHT_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.RIGHT,
                CENTER_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
                JUSTIFIED_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
                NATURAL_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
            }[value])

    def _set_text(self, value):
        self._impl.setText(value)

    def rehint(self):
        # print("REHINT label", self, self._impl.getMeasuredWidth(), self._impl.getMeasuredHeight())
        self.style.hint(
            width=self._impl.getMeasuredWidth() / self.app._impl.device_scale,
            height=self._impl.getMeasuredHeight() / self.app._impl.device_scale,
        )
