from http.cookiejar import CookieJar

from toga.widgets.webview import CookiesResult, JavaScriptResult

from .base import Widget


class WebView(Widget):
    def create(self):
        self._action("create WebView")
        # attribute to store the URL allowed by user interaction or
        # user on_navigation_starting handler
        self._allowed_url = None

    def set_content(self, root_url, content):
        if self.interface.on_navigation_starting:
            # mark URL as being allowed
            self._allowed_url = "about:blank"
        self._action("set content", root_url=root_url, content=content)

    def get_user_agent(self):
        agent = self._get_value("user_agent")
        return "Toga dummy backend" if agent is None else agent

    def set_user_agent(self, value):
        self._set_value("user_agent", value)

    def get_url(self):
        return self._get_value("url", None)

    def set_url(self, value, future=None):
        if self.interface.on_navigation_starting:
            # mark URL as being allowed
            self._allowed_url = value
        self._set_value("url", value)
        self._set_value("loaded_future", future)
        # allow the URL only once
        self._allowed_url = None

    def get_cookies(self):
        self._action("cookies")
        self._cookie_result = CookiesResult()
        return self._cookie_result

    def evaluate_javascript(self, javascript, on_result=None):
        self._action("evaluate_javascript", javascript=javascript)
        self._js_result = JavaScriptResult(on_result)
        return self._js_result

    def simulate_page_loaded(self):
        self.interface.on_webview_load()

        loaded_future = self._get_value("loaded_future", None)
        if loaded_future:
            loaded_future.set_result(None)
            self._set_value("loaded_future", None)

    def simulate_javascript_result(self, value):
        self._js_result.set_result(42)

    def simulate_cookie_retrieval(self, cookies):
        """Simulate completion of cookie retrieval."""
        cookie_jar = CookieJar()
        for cookie in cookies:
            cookie_jar.set_cookie(cookie)
        self._cookie_result.set_result(cookie_jar)

    def simulate_navigation_starting(self, url):
        """Simulate a navigation"""
        allow = True
        if self.interface.on_navigation_starting._raw:
            if self._allowed_url == "about:blank" or self._allowed_url == url:
                # URL is allowed by user code
                allow = True
            else:
                # allow the URL only once
                self._allowed_url = None
                result = self.interface.on_navigation_starting(url=url)
                if isinstance(result, bool):
                    # on_navigation_starting handler is synchronous
                    allow = result
                else:
                    # on_navigation_starting handler is asynchronous
                    # deny navigation until the user defined on_navigation_starting
                    # coroutine has completed.
                    allow = False
        if allow:
            self.set_url(url)
