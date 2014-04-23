from .base import Widget


class Button(Widget):
    def __init__(self, label, on_press=None):
        super(Button, self).__init__()
