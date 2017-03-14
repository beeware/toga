from .base import Widget


class NavigationView(Widget):
    def __init__(self, title, content, on_action=None, style=None):
        super().__init__(title=title, content=content, on_action=on_action, style=style)

    def _configure(self, title, content, on_action):
        self.title = title
        self.content = [content]
        self.on_action = on_action

    def push(self, content):
        self.content.push(content)
        self._push(content)

    def _pop(self):
        self.content.pop()
        self._pop()
