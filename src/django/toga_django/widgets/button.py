from .base import Widget
from ..libs import Button as TogaButton


class Button(Widget):
    def __init__(self, label, on_press=None, **style):
        default_style = {
            'margin': 7
        }
        default_style.update(style)
        super(Button, self).__init__(**default_style)
        self.label = label

        self.on_press = on_press
        self.startup()

    def startup(self):
        pass

    def materialize(self):
        return TogaButton(
            widget_id=self.widget_id,
            label=self.label,
            on_press=self.handler(self.on_press, 'on_press') if self.on_press else None
        )

    def _set_window(self, window):
        super()._set_window(window)
        if self.on_press:
            self.window.callbacks[(self.widget_id, 'on_press')] = self.on_press
