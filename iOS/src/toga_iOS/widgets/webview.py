from rubicon.objc import objc_id, objc_method, objc_property, py_from_ns
from travertino.size import at_least

from toga.widgets.webview import CookiesResult, JavaScriptResult
from toga_iOS.libs import NSURL, NSURLRequest, WKWebView
from toga_iOS.widgets.base import Widget


def js_completion_handler(result):
    def _completion_handler(res: objc_id, error: objc_id) -> None:
        if error:
            error = py_from_ns(error)
            exc = RuntimeError(str(error))
            result.set_exception(exc)
        else:
            result.set_result(py_from_ns(res))

    return _completion_handler


def cookies_completion_handler(result):
    def _completion_handler(cookies: objc_id) -> None:
        try:
            # Convert cookies from Objective-C to Python objects
            cookies_array = py_from_ns(cookies)

            # Structure the cookies as a list of dictionaries
            structured_cookies = []
            for cookie in cookies_array:
                structured_cookies.append(
                    {
                        "name": str(cookie.name),
                        "value": str(cookie.value),
                        "domain": str(cookie.domain),
                        "path": str(cookie.path),
                        "secure": bool(cookie.isSecure),
                        "http_only": bool(cookie.isHTTPOnly),
                        "expiration": (
                            cookie.expiresDate.description
                            if cookie.expiresDate
                            else None
                        ),
                    }
                )

            # Set the result in the AsyncResult
            result.set_result(structured_cookies)
        except Exception as exc:
            # Set an exception in the AsyncResult if something goes wrong
            result.set_exception(exc)

    return _completion_handler


class TogaWebView(WKWebView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def webView_didFinishNavigation_(self, navigation) -> None:
        self.interface.on_webview_load()

        if self.impl.loaded_future:
            self.impl.loaded_future.set_result(None)
            self.impl.loaded_future = None


class WebView(Widget):
    def create(self):
        self.native = TogaWebView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        # Enable the content inspector. This was added in iOS 16.4.
        # It is a no-op on earlier versions.
        self.native.inspectable = True
        self.native.navigationDelegate = self.native

        self.loaded_future = None

        # Add the layout constraints
        self.add_constraints()

    def get_url(self):
        url = str(self.native.URL)
        return None if url == "about:blank" else url

    def set_url(self, value, future=None):
        if value:
            request = NSURLRequest.requestWithURL(NSURL.URLWithString(value))
        else:
            request = NSURLRequest.requestWithURL(NSURL.URLWithString("about:blank"))

        self.loaded_future = future
        self.native.loadRequest(request)

    def set_content(self, root_url, content):
        self.native.loadHTMLString(content, baseURL=NSURL.URLWithString(root_url))

    def get_user_agent(self):
        return str(self.native.valueForKey("userAgent"))

    def set_user_agent(self, value):
        self.native.customUserAgent = value

    def evaluate_javascript(self, javascript, on_result=None):
        result = JavaScriptResult(on_result)
        self.native.evaluateJavaScript(
            javascript,
            completionHandler=js_completion_handler(result),
        )

        return result

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def get_cookies(self, on_result=None):
        """
        Retrieve all cookies asynchronously from the WebView.

        :param on_result: Optional callback to handle the cookies.
        :return: An AsyncResult object that can be awaited.
        """
        # Create an AsyncResult to manage the cookies
        result = CookiesResult(on_result)

        # Retrieve the cookie store from the WebView
        cookie_store = self.native.configuration.websiteDataStore.httpCookieStore

        # Call the method to retrieve all cookies and pass the completion handler
        cookie_store.getAllCookies_(cookies_completion_handler(result))

        return result
