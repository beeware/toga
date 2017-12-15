from toga.interface import WebView as WebViewInterface

from .base import WidgetMixin
from .. import impl


class WebView(WebViewInterface, WidgetMixin):
    def __init__(self, id=None, url=None, on_key_down=None, style=None):
        super().__init__(id=id, style=style, url=url, on_key_down=on_key_down)
        self._create()

    def create(self):
        self._impl = impl.WebView(
            id=self.id,
            url=self._config['url'],
            on_key_down=self.handler(self._config['on_key_down'], 'on_key_down') if self._config['on_key_down'] else None,
            style=self.style,
        )

    def set_url(self, value):
        self._impl.url = value

    # def _set_window(self, window):
    #     super()._set_window(window)
    #     if self.on_press:
    #         self.window.callbacks[(self.id, 'on_press')] = self.on_press

    def get_dom(self):
        raise NotImplementeException()

    def set_user_agent(self, value):
        raise NotImplementeException()

    def set_placeholder(self, value):
        raise NotImplementeException()

    def set_readonly(self, value):
        raise NotImplementeException()

    def get_value(self):
        return self._impl.value

    def set_value(self, value):
        raise NotImplementeException()

    def set_content(self, root_url, content):
        raise NotImplementeException()

    def evaluate(self, javascript):
        raise NotImplementeException()
