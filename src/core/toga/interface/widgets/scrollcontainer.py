from .base import Widget


class ScrollContainer(Widget):
    _CONTAINER_CLASS = None

    def __init__(self, id=None, style=None, horizontal=True, vertical=True, content=None):
        super().__init__(id=id, style=style, horizontal=horizontal, vertical=vertical, content=content)

    def _configure(self, horizontal, vertical, content):
        self.horizontal = horizontal
        self.vertical = vertical
        self.content = content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        if widget:
            self._content.window = self.window
            self._content.app = self.app

            if widget._impl is None:
                self._inner_container = self._CONTAINER_CLASS()
                self._inner_container.root_content = widget
            else:
                self._inner_container = widget

            self._set_content(self._inner_container, widget)

    @property
    def vertical(self):
        return self._vertical

    @vertical.setter
    def vertical(self, value):
        self._vertical = value
        self._set_vertical(value)

    @property
    def horizontal(self):
        return self._horizontal

    @horizontal.setter
    def horizontal(self, value):
        self._horizontal = value
        self._set_horizontal(value)

    def _set_vertical(self, value):
        raise NotImplementedError('ScrollContainer must define _set_vertical()')

    def _set_horizontal(self, value):
        raise NotImplementedError('ScrollContainer must define _set_horizontal()')
