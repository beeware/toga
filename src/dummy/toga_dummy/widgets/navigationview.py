from .base import Widget


class NavigationView(Widget):
    def create(self):
        self._action('create NavigationView')

    def push(self, content):
        self._action('push', content=content)

    def pop(self):
        self._action('pop')
