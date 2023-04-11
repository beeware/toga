import warnings

from toga.handlers import wrapped_handler

from .base import Widget


class WebView(Widget):
    """A widget to display and open html content.

    :param id: An identifier for this widget.
    :type  id: ``str``
    :param style: An optional style object. If no style is provided then a new one will be created for the widget.
    :type  style: ``Style``
    :param url: The URL to start with.
    :type  url: ``str``
    :param user_agent: The user agent for the web view.
    :type  user_agent: ``str``
    :param on_key_down: The callback method for when a key is pressed within the web view
    :type  on_key_down: ``callable``
    :param on_webview_load: The callback method for when the webview loads (or reloads).
    :type  on_webview_load: ``callable``
    """

    def __init__(
        self,
        id=None,
        style=None,
        factory=None,  # DEPRECATED!
        url=None,
        user_agent=None,
        on_key_down=None,
        on_webview_load=None,
    ):
        super().__init__(id=id, style=style)

        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        # Prime some internal property-backing variables
        self._html_content = None
        self._user_agent = None

        self._impl = self.factory.WebView(interface=self)
        self.user_agent = user_agent
        self.url = url
        self.on_key_down = on_key_down
        self.on_webview_load = on_webview_load

    @property
    def dom(self):
        """The current DOM.

        :return: The current DOM
        :rtype:  ``str``
        """
        return self._impl.get_dom()

    @property
    def url(self):
        """The current URL.

        :return: The current URL
        :rtype:  ``str``
        """
        return self._impl.get_url()

    @url.setter
    def url(self, value):
        """Set the current URL of the web view.

        :param value: The URL
        :type  value: ``str``
        """
        self._html_content = None
        self._impl.set_url(value)

    @property
    def on_key_down(self):
        """The handler to invoke when the button is pressed.

        :return: The function that is called on button press.
        :rtype:  ``callable``
        """
        return self._on_key_down

    @on_key_down.setter
    def on_key_down(self, handler):
        """Set the handler to invoke when a key is pressed.

        :param handler: The handler to invoke when a key is pressed.
        :type  handler: ``callable``
        """
        self._on_key_down = wrapped_handler(self, handler)
        self._impl.set_on_key_down(self._on_key_down)

    @property
    def on_webview_load(self):
        """The handler to invoke when the webview finishes loading.

        :return: The function that is called when the webview finishes loading.
        :rtype:  ``callable``
        """
        return self._on_webview_load

    @on_webview_load.setter
    def on_webview_load(self, handler):
        """Set the handler to invoke when the webview finishes loading.

        :param handler: The handler to invoke when the webview finishes loading.
        :type  handler: ``callable``
        """
        self._on_webview_load = wrapped_handler(self, handler)
        self._impl.set_on_webview_load(self._on_webview_load)

    @property
    def user_agent(self):
        """The user agent for the web view as a ``str``.

        :return: The user agent
        :rtype:  ``str``
        """
        return self._user_agent

    @user_agent.setter
    def user_agent(self, value):
        self._user_agent = value
        self._impl.set_user_agent(value)

    def set_content(self, root_url, content):
        """Set the content of the web view.

        :param root_url: The URL
        :type  root_url: ``str``
        :param content: The new content
        :type  content: ``str``
        """
        self._html_content = content
        self._impl.set_content(root_url, content)

    async def evaluate_javascript(self, javascript):
        """Evaluate a JavaScript expression, returning the result.

        **This is an asynchronous operation**. The method will complete
        when the return value is available.

        :param javascript: The javascript expression to evaluate.
        :type  javascript: ``str``
        """
        return await self._impl.evaluate_javascript(javascript)

    def invoke_javascript(self, javascript):
        """Invoke a JavaScript expression.

        The result (if any) of the javascript is ignored.

        **No guarantee is provided that the javascript has completed
        execution when `invoke()` returns**

        :param javascript: The javascript expression to evaluate.
        :type  javascript: ``str``
        """
        self._impl.invoke_javascript(javascript)
