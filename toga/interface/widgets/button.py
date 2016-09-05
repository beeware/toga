from .base import Widget


class Button(Widget):
    def __init__(self, label, id=None, style=None, on_press=None):
        super().__init__(id=id, style=style)
        self._label = label
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

    def _set_label(self, value):
        raise NotImplementedError('Button widget must define _set_label()')
