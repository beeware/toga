from .base import Widget


class SplitContainer(Widget):
    _CONTAINER_CLASS = None
    HORIZONTAL = False
    VERTICAL = True

    def __init__(self, id=None, style=None, direction=VERTICAL, content=None):
        super().__init__(id=id, style=style, direction=direction, content=content)
        self._direction = direction
        self._containers = []

    def _configure(self, direction, content):
        self.content = content
        self.direction = direction

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        if content is None:
            self._content = None
            return

        if len(content) < 2:
            raise ValueError('SplitContainer content must have at least 2 elements')

        self._content = content

        for position, widget in enumerate(self._content):
            widget.window = self.window
            widget.app = self.app

            if widget._impl is None:
                container = _CONTAINER_CLASS()
                container.root_content = widget
                widget._container = container
            else:
                container = widget

            self._add_content(position, container)

            self._containers.append(container)

    def _set_app(self, app):
        if self._content:
            for content in self._content:
                content.app = self.app

    def _set_window(self, window):
        if self._content:
            for content in self._content:
                content.window = self.window

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value
        self._set_direction(value)
        self.rehint()

    def on_resize(self):
        pass
