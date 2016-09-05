from .base import Widget


class SplitContainer(Widget):
    HORIZONTAL = False
    VERTICAL = True

    def __init__(self, id=None, style=None, direction=VERTICAL):
        super().__init__(id=None, style=None)
        self._content = None
        self.direction = direction

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        if len(content) < 2:
            raise ValueError('SplitContainer content must have at least 2 elements')

        self._content = content

        for widget in self._content:
            widget.window = self.window
            widget.app = self.app
            self._add_content(widget)

    def _set_app(self, app):
        if self._content:
            for content in self._content:
                content.app = self.app

    def _set_window(self, window):
        if self._content:
            for content in self._content:
                content.window = self.window
