

class WebView:
    def __init__(self, id=None, url=None, on_key_down=None):
        self.id = id

        self.url = url

    def __html__(self):
        return """
            <div class="container">
                <iframe id="toga:%s" data-toga-class="toga.WebView" data-toga-ports="%s" class="webview" src="%s">
                </iframe>
            </div>""" % (
                self.id,
                '',  #  self.ports,
                self.url if self.url else ''
            )

    def set_url(self, value):
        self.impl.src = value

    def set_content(self, root_url, content):
        pass

    # def evaluate(self, javascript):
    #     raise NotImplementedError('Webview widget must define evaluate()')
