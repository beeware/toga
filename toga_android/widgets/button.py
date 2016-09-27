from android.widget import Button as AndroidButton

from toga.interface import Button as ButtonInterface

from .base import WidgetMixin
from ..utils import wrapped_handler


class TogaButtonListener(implements=android.view.View[OnClickListener]):
    def onClick(self, v: android.view.View) -> None:
        process_callback(self._interface.on_press(self._interface))


class Button(ButtonInterface, WidgetMixin):
    def __init__(self, label, id=None, style=None, on_press=None):
        super().__init__(label, id=id, style=style, on_press=on_press)
        self._create()

    def create(self):
        self._impl = AndroidButton()

        self._listener = TogaButtonListener()
        self._listener._interface = self
        self._impl.setOnClickListener(self._listener)

        self.rehint()

    def _set_label(self, label):
        self._impl.setText(self.label)
        self.rehint()

    def rehint(self):
        # print("REHINT", self, self._impl.get_preferred_width(), self._impl.get_preferred_height(), getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False))
        # hints = {}
        # width = self._impl.get_preferred_width()
        # minimum_width = width[0]
        # natural_width = width[1]

        # height = self._impl.get_preferred_height()
        # minimum_height = height[0]
        # natural_height = height[1]

        # if minimum_width > 0:
        #     hints['min_width'] = minimum_width
        # if minimum_height > 0:
        #     hints['min_height'] = minimum_height
        # if natural_height > 0:
        #     hints['height'] = natural_height

        # if hints:
        #     self.style.hint(**hints)

        self.style.hint(
            min_width=200,
            height=30
        )
