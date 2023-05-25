import asyncio

from toga.handlers import AsyncResult, wrapped_handler

from .base import Widget


class JavaScriptResult(AsyncResult):
    RESULT_TYPE = "JavaScript"


class WebView(Widget):
    def __init__(
        self,
        id=None,
        style=None,
        url: str = None,
        user_agent: str = None,
        on_webview_load=None,
    ):
        """Create a new WebView widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param url: The full URL to load in the WebView. Optional; if not provided,
            an empty page will be displayed
        :param user_agent: The user agent to use for web requests. Optional; if not
            provided, the default user agent for the platform will be used.
        :param on_webview_load: A handler that will be invoked when a key is pressed while
            the web view has focus.
        """

        super().__init__(id=id, style=style)

        self._impl = self.factory.WebView(interface=self)
        self.user_agent = user_agent

        # Set the load handler before loading the first URL.
        self.on_webview_load = on_webview_load
        self.url = url

    def _set_url(self, url, future):
        # Utility method for validating and setting the URL with a future.
        if url and not (url.startswith("https://") or url.startswith("http://")):
            raise ValueError("WebView can only display http:// and https:// URLs")

        self._impl.set_url(url, future=future)

    @property
    def url(self) -> str:
        """The current URL.

        WebView can only display ``http://`` and ``https://`` URLs.

        Returns ``None`` if no URL is currently displayed.
        """
        return self._impl.get_url()

    @url.setter
    def url(self, value):
        self._set_url(value, future=None)

    async def load_url(self, url: str):
        """Load a URL, and wait until the loading has completed.

        :param url: The URL to load.
        """
        if url and not (url.startswith("https://") or url.startswith("http://")):
            raise ValueError("WebView can only display http:// and https:// URLs")

        loop = asyncio.get_event_loop()
        loaded_future = loop.create_future()

        self._set_url(url, future=loaded_future)

        return await loaded_future

    @property
    def on_webview_load(self):
        """The handler to invoke when the web view finishes loading."""
        return self._on_webview_load

    @on_webview_load.setter
    def on_webview_load(self, handler):
        self._on_webview_load = wrapped_handler(self, handler)

    @property
    def user_agent(self) -> str:
        """The user agent for the web view."""
        return self._impl.get_user_agent()

    @user_agent.setter
    def user_agent(self, value):
        self._impl.set_user_agent(value)

    def set_content(self, root_url: str, content: str):
        """Set the HTML content of the WebView.

        :param root_url: The URL
        :param content: The HTML content for the WebView
        """
        self._impl.set_content(root_url, content)

    def evaluate_javascript(self, javascript, on_result=None) -> JavaScriptResult:
        """Evaluate a JavaScript expression.

        **This method is asynchronous**. It does not guarantee that the provided
        JavaScript has finished evaluating when the method returns. The value
        returned by this method can be awaited in an asynchronous context.
        Alternatively, you can provide an ``on_result`` callback that will be
        invoked when the JavaScript has been evaluated.

        :param javascript: The JavaScript expression to evaluate.
        :param on_result: Optional; a callback that will be invoked when the the
            evaluated JavaScript completes.
        :returns: An asynchronous JavaScriptResult object.
        """
        return self._impl.evaluate_javascript(javascript, on_result=on_result)
