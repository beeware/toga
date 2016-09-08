from .base import Widget


class WebView(Widget):
    def __init__(self, id=None, style=None, url=None, on_key_down=None):
        super(WebView, self).__init__(id=id, style=style, url=url, on_key_down=on_key_down)

    def _configure(self, url, on_key_down):
        self.url = url
        self.on_key_down = on_key_down

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        self._set_url(value)

    def set_content(self, root_url, content):
        self._url = root_url
        self._set_content(root_url, content)

    def _set_url(self, value):
        raise NotImplementedError('Webview widget must define _set_url()')

    def _set_content(self, root_url, content):
        raise NotImplementedError('Webview widget must define _set_content()')

    def evaluate(self, javascript):
        raise NotImplementedError('Webview widget must define evaluate()')
