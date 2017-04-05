from toga.interface import Button as ButtonInterface

from .. import impl
from .base import WidgetMixin
# from ..utils import process_callback


class Button(ButtonInterface, WidgetMixin):
    def __init__(self, label, id=None, style=None, on_press=None):
        super().__init__(label, id=id, style=style, on_press=on_press)
        self._create()

    def create(self):
        self._impl = impl.Button(
            id=self.id,
            label=self._config['label'],
            on_press=self.handler(self._config['on_press'], 'on_press') if self._config['on_press'] else None,
            style=self.style,
        )

    def _set_window(self, window):
        super()._set_window(window)
        if self.on_press:
            self.window.callbacks[(self.id, 'on_press')] = self.on_press

    def _set_label(self, label):
        pass

    def _set_enabled(self, value):
        pass
