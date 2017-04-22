
class WebView:
    def __init__(self, id=None, url=None, on_key_down=None, style=None):
        self.id = id
        self._impl = None
        self._url = url
        self.style = style

    def __html__(self):
        return """
            <iframe id="toga:%s" class="toga WebView" style="%s" src="%s" data-toga-class="toga.WebView" data-toga-ports="%s">
            </iframe>""" % (
                self.id,
                self.style,
                self.url if self.url else '',
                '',  #  self.ports,
            )

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        if self._impl:
            self._impl.src = value

    def set_content(self, root_url, content):
        pass

    # def evaluate(self, javascript):
    #     raise NotImplementedError('Webview widget must define evaluate()')
