from .base import Widget
from ..libs import TextInput as TogaTextInput


class TextInput(Widget):
    def __init__(self, initial='', placeholder=None, readonly=False, **style):
        default_style = {
            'margin': 7
        }
        default_style.update(style)
        super(TextInput, self).__init__(**default_style)

        self.startup()

        self.readonly = readonly
        self.placeholder = placeholder
        self.initial = initial

    def startup(self):
        pass
        # Height of a text input is known and fixed.
        # if self.height is None:
        #     self.height = self._impl.fittingSize().height
        # if self.min_width is None:
        #     self.min_width = 100

    def materialize(self):
        return TogaTextInput(
            widget_id=self.widget_id,
            initial=self.initial,
            placeholder=self.placeholder,
            readonly=self.readonly,
        )
