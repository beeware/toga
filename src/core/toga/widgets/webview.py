from .base import Widget


class WebView(Widget):
    def __init__(self, id=None, style=None, factory=None, url=None, on_key_down=None):
        """ Instantiate a new instance of the Web view widget.

        :param id:          An identifier for this widget.
        :type  id:          ``str``

        :param style:       an optional style object. If no style is provided then a
                            new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`

        :param url: The URL to start with
        :type  url: ``str``

        :param on_key_down: The callback method for when the a key is pressed within
            the web view
        :type  on_key_down: ``callable``
        """
        super(WebView, self).__init__(id=id, style=style, factory=factory)

        self._impl = self.factory.WebView(interface=self)
        self.url = url
        self.on_key_down = on_key_down

    @property
    def url(self):
        """
        The current URL

        :rtype: ``str``
        """
        return self._url

    @url.setter
    def url(self, value):
        """
        Set URL
        :param value: url
        :type value: ``str`
        """
        self._url = value
        self._impl.set_url(value)

    def set_content(self, root_url, content):
        """
        Set the content of the web view

        :param root_url: The URL
        :type  root_url: ``str``

        :param content: The new content
        :type  content: ``str``
        """
        self._url = root_url
        self._impl.set_content(root_url, content)

    def evaluate(self, javascript):
        """
        Evaluate a JavaScript expression

        :param javascript: The javascript expression
        :type  javascript: ``str``
        """
        self._impl.set_evaluate(javascript)