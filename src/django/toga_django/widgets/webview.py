from toga.interface import WebView as WebViewInterface

from .. import impl
from .base import WidgetMixin
# from ..libs import WebView as TogaWebView


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

    def _set_url(self, value):
        self._impl.url = value

    # def _set_window(self, window):
    #     super()._set_window(window)
    #     if self.on_press:
    #         self.window.callbacks[(self.id, 'on_press')] = self.on_press

    def _set_placeholder(self, value):
        pass

    def _set_readonly(self, value):
        pass

    def _get_value(self):
        return self._impl.value

    def _set_value(self, value):
        pass

    def _set_content(self, root_url, content):
        pass
