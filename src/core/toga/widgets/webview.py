from toga.handlers import wrapped_handler

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
        super().__init__(id=id, style=style, factory=factory)

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
    def on_key_down(self):
        """The handler to invoke when the button is pressed.

        Returns:
            The function ``callable`` that is called on button press.
        """
        return self._on_key_down

    @on_key_down.setter
    def on_key_down(self, handler):
        """Set the handler to invoke when a key is pressed.

        Args:
            handler (:obj:`callable`): The handler to invoke when a key is pressed.
        """
        self._on_key_down = wrapped_handler(self, handler)
        self._impl.set_on_key_down(self._on_key_down)

    @property
    def on_webview_load(self):
        """The handler to invoke when the webview finishes loading pressed.

        Returns:
            The function ``callable`` that is called when the webview finished loading.
        """
        return self._on_webview_load

    @on_webview_load.setter
    def on_webview_load(self, handler):
        """Set the handler to invoke when the button is pressed.

        Args:
            handler (:obj:`callable`): The handler to invoke when the button is pressed.
        """
        self._on_webview_load = wrapped_handler(self, handler)
        self._impl.set_on_webview_load(self._on_webview_load)

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

    async def evaluate_javascript(self, javascript):
        """Evaluate a JavaScript expression, returning the result.

        **This is an asynchronous operation**. The method will complete
        when the return value is available.

        Args:
            javascript (str): The javascript expression to evaluate.
        """
        return await self._impl.evaluate_javascript(javascript)

    def invoke_javascript(self, javascript):
        """Invoke a JavaScript expression.

        The result (if any) of the javascript is ignored.

        **No guarantee is provided that the javascript has completed
        execution when `invoke()` returns**

        Args:
            javascript (str): The javascript expression to evaluate.
        """
        self._impl.invoke_javascript(javascript)
