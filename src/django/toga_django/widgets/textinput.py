from toga.interface import TextInput as TextInputInterface

from .base import WidgetMixin
from .. import impl


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

    def set_placeholder(self, value):
        raise NotImplementedError()

    def set_readonly(self, value):
        raise NotImplementedError()

    def get_value(self):
        return self._impl.value

    def set_value(self, value):
        raise NotImplementedError()

    def rehint(self):
        pass
