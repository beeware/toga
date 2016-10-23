from .base import Widget


class OptionContainer(Widget):
    _CONTAINER_CLASS = None

    def __init__(self, id=None, style=None, content=None):
        super().__init__(id=id, style=style, content=content)
        self._containers = []

    def _configure(self, content):
        if content:
            for label, widget in content:
                self.add(label, widget)

    def add(self, label, widget):
        if widget._impl is None:
            container = self._CONTAINER_CLASS()
            container.content = widget
        else:
            container = widget

        self._containers.append((label, container, widget))

        widget.window = self.window
        widget.app = self.app

        self._add_content(label, container, widget)

    def _update_child_layout(self):
        for label, container, widget in self._containers:
            container._update_layout()
