from .base import Widget


class Button(Widget):
    def __init__(self, label, id=None, style=None, on_press=None):
        super().__init__(id=id, style=style, label=label, on_press=on_press)

    def _configure(self, label, on_press):
        self.label = label
        self.on_press = on_press

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if value is None:
            self._label = ''
        else:
            self._label = str(value)
        self._set_label(value)
        self.rehint()

    def _set_label(self, value):
        raise NotImplementedError('Button widget must define _set_label()')

    @property
    def on_press(self):
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        self._on_press = handler
        self._set_on_press(handler)

    def _set_on_press(self, value):
        pass