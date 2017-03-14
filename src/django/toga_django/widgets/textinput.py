from toga.interface import TextInput as TextInputInterface

from .. import impl
from .base import WidgetMixin
# from ..libs import TextInput as TogaTextInput


class TextInput(TextInputInterface, WidgetMixin):
    def __init__(self, id=None, initial='', placeholder=None, readonly=False, style=None):
        super().__init__(id=id, style=style, initial=initial, placeholder=placeholder, readonly=readonly)
        self._create()

    def create(self):
        self._impl = impl.TextInput(
            id=self.id,
            initial=self._config['initial'],
            placeholder=self._config['placeholder'],
            readonly=self._config['readonly'],
            # on_press=self.handler(self._config['on_press'], 'on_press') if self._config['on_press'] else None
            style=self.style,
        )

    # def _set_window(self, window):
    #     super()._set_window(window)
    #     if self.on_press:
    #         self.window.callbacks[(self.id, 'on_press')] = self.on_press

    def _set_placeholder(self, value):
        pass

    def _set_readonly(self, value):
        pass

    def _get_value(self):
        return self._impl.value

    def _set_value(self, value):
        pass
