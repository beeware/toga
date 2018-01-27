from .base import Widget


class WebView(Widget):
    """ A widget to display and open html content.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
        url (str): The URL to start with.
        user_agent (str): The user agent for the web view.
        on_key_down (``callable``): The callback method for when a key is pressed within
            the web view
        on_webview_load (``callable``): The callback method for when the webview loads (or reloads).
    """
    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    def __init__(self, id=None, style=None, factory=None,
                 url=None, user_agent=None, on_key_down=None, on_webview_load=None):
        super(WebView, self).__init__(id=id, style=style, factory=factory)

        self._impl = self.factory.WebView(interface=self)
        self.user_agent = user_agent
        self.url = url
        self.on_key_down = on_key_down
        self.on_webview_load = on_webview_load

    @property
    def dom(self):
        """ The current DOM

        Returns:
            The current DOM as a ``str``.
        """
        return self._impl.get_dom()

    @property
    def url(self):
        """ The current URL

        Returns:
            The current URL as a ``str``.
        """
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        self._impl.set_url(value)

    @property
    def user_agent(self):
        """ The user agent for the web view as a ``str``.

        Returns:
            The user agent as a ``str``.
        """
        return self._user_agent

    @user_agent.setter
    def user_agent(self, value):
        self._user_agent = value
        self._impl.set_user_agent(value)

    def set_content(self, root_url, content):
        """ Set the content of the web view.

        Args:
            root_url (str): The URL.
            content (str): The new content.

        Returns:

        """
        self._url = root_url
        self._impl.set_content(root_url, content)

    def evaluate(self, javascript):
        """ Evaluate a JavaScript expression

        Args:
            javascript (str): The javascript expression to evaluate.
        """
        return self._impl.evaluate(javascript)
