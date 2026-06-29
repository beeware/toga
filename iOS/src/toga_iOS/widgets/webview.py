from http.cookiejar import Cookie, CookieJar

from rubicon.objc import (
    Block,
    NSInteger,
    ObjCBlock,
    objc_id,
    objc_method,
    objc_property,
    py_from_ns,
)
from travertino.size import at_least

from toga.widgets.webview import CookiesResult, JavaScriptResult
from toga_iOS.libs import (
    NSURL,
    NSURLRequest,
    UIAlertAction,
    UIAlertActionStyle,
    UIAlertController,
    UIAlertControllerStyle,
    WKNavigationResponsePolicy,
    WKUIDelegate,
    WKWebView,
)
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
        # Convert cookies from Objective-C to Python objects
        cookies_array = py_from_ns(cookies)

        # Initialize a CookieJar
        cookie_jar = CookieJar()

        # Add each cookie from the array into the CookieJar
        for cookie in cookies_array:
            cookie_obj = Cookie(
                version=0,
                name=str(cookie.name),
                value=str(cookie.value),
                port=None,
                port_specified=False,
                domain=str(cookie.domain),
                domain_specified=True,
                domain_initial_dot=False,
                path=str(cookie.path),
                path_specified=True,
                secure=bool(cookie.Secure),
                expires=None,
                discard=bool(cookie.isSessionOnly()),
                comment=None,
                comment_url=None,
                rest={},
            )
            cookie_jar.set_cookie(cookie_obj)

        # Set the result in the AsyncResult
        result.set_result(cookie_jar)

    return _completion_handler


class TogaWebView(WKWebView, protocols=[WKUIDelegate]):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def webView_decidePolicyForNavigationAction_decisionHandler_(
        self,
        webview,
        navigationAction,
        decisionHandler,
    ) -> None:
        _decision_handler = ObjCBlock(decisionHandler, None, NSInteger)
        if (
            str(navigationAction.request.URL) == self.impl._allowed_url
            or self.impl.interface.on_navigation_starting._raw is None
        ):
            # If URL is pre-approved, or there's no navigation handler,
            # allow the navigation.
            _decision_handler(WKNavigationResponsePolicy.Allow)
            self.impl._allowed_url = None
        else:
            url = str(navigationAction.request.URL)
            allow = self.impl.interface.on_navigation_starting(url=url)
            if isinstance(allow, bool | None):
                # on_navigation_starting handler is synchronous
                if allow:
                    decision = WKNavigationResponsePolicy.Allow
                else:
                    decision = WKNavigationResponsePolicy.Cancel

                _decision_handler(decision)
            else:
                # on_navigation_starting handler is asynchronous. Attach a completion
                # handler so that when the async handler completes, the webView
                # decision handler is invoked.

                def on_navigation_decision(future):
                    if future.result():
                        decision = WKNavigationResponsePolicy.Allow
                    else:
                        decision = WKNavigationResponsePolicy.Cancel

                    ObjCBlock(decisionHandler, None, NSInteger)(decision)

                allow.add_done_callback(on_navigation_decision)

    @objc_method
    def webView_didFinishNavigation_(self, webView, navigation) -> None:
        # It's possible for this handler to be invoked *after* the interface/impl object
        # has been destroyed. If the interface/impl doesn't exist there's no handler to
        # invoke either, so ignore the edge case. This can't be reproduced reliably, so
        # don't check coverage on the `is None` case.
        if self.interface:  # pragma: no branch
            self.interface.on_webview_load()

        if self.impl and self.impl.loaded_future:  # pragma: no branch
            self.impl.loaded_future.set_result(None)
            self.impl.loaded_future = None

    # WKUIDelegate protocol methods required to display dialogs to the user.
    # These are difficult to automatically test because they use
    # completionHandler, which is a method utilized by the underlying WKWebView
    # objective-C codebase. completionHandler cannot be created manually for
    # testing because it is difficult to pull it up from the native codebase.
    @objc_method
    def webView_runJavaScriptAlertPanelWithMessage_initiatedByFrame_completionHandler_(
        self, webView, message, frame, completionHandler
    ) -> None:  # pragma: no cover
        alert = UIAlertController.alertControllerWithTitle(
            "Alert!",
            message=message,
            preferredStyle=UIAlertControllerStyle.Alert,
        )

        # Add OK button
        def _ok(action: objc_id) -> None:
            ObjCBlock(completionHandler, None)()

        alert.addAction(
            UIAlertAction.actionWithTitle(
                "OK",
                style=UIAlertActionStyle.Default,
                handler=Block(_ok, None, objc_id),
            )
        )

        # Display dialog
        view_controller = self.interface.window._impl.native.rootViewController
        view_controller.presentViewController(
            alert,
            animated=False,
            completion=None,
        )

    @objc_method
    def webView_runJavaScriptConfirmPanelWithMessage_initiatedByFrame_completionHandler_(  # noqa: E501
        self, webView, message, frame, completionHandler
    ) -> None:  # pragma: no cover
        alert = UIAlertController.alertControllerWithTitle(
            "Confirm?",
            message=message,
            preferredStyle=UIAlertControllerStyle.Alert,
        )

        # Add OK button
        def _ok(action: objc_id) -> None:
            ObjCBlock(completionHandler, None, bool)(True)

        alert.addAction(
            UIAlertAction.actionWithTitle(
                "OK",
                style=UIAlertActionStyle.Default,
                handler=Block(_ok, None, objc_id),
            )
        )

        # Add cancel button
        def _cancel(action: objc_id) -> None:
            ObjCBlock(completionHandler, None, bool)(False)

        alert.addAction(
            UIAlertAction.actionWithTitle(
                "Cancel",
                style=UIAlertActionStyle.Default,
                handler=Block(_cancel, None, objc_id),
            )
        )

        # Display dialog
        view_controller = self.interface.window._impl.native.rootViewController
        view_controller.presentViewController(
            alert,
            animated=False,
            completion=None,
        )


class WebView(Widget):
    def create(self):
        self.native = TogaWebView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        # Enable the content inspector. This was added in iOS 16.4.
        # It is a no-op on earlier versions.
        self.native.inspectable = True
        self.native.navigationDelegate = self.native
        # Set UIDelegate to self for file dialog support
        self.native.UIDelegate = self.native

        self.loaded_future = None

        # attribute to store the URL allowed by user interaction or
        # user on_navigation_starting handler
        self._allowed_url = None

        # Add the layout constraints
        self.add_constraints()

    def get_url(self):
        url = str(self.native.URL)
        return None if url == "about:blank" else url

    def set_url(self, value, future=None):
        if value is None:
            value = "about:blank"

        if self.interface.on_navigation_starting._raw:
            # mark URL as being allowed
            self._allowed_url = value

        request = NSURLRequest.requestWithURL(NSURL.URLWithString(value))

        self.loaded_future = future
        self.native.loadRequest(request)

    def set_content(self, root_url, content):
        if root_url is None:
            root_url = "about:blank"

        if self.interface.on_navigation_starting._raw:
            # mark URL as being allowed
            self._allowed_url = root_url

        self.native.loadHTMLString(content, baseURL=NSURL.URLWithString(root_url))

    def get_user_agent(self):
        return str(self.native.valueForKey("userAgent"))

    def set_user_agent(self, value):
        self.native.customUserAgent = value

    def get_cookies(self):
        """
        Retrieve all cookies asynchronously from the WebView.

        :returns: An AsyncResult object that can be awaited.
        """
        # Create an AsyncResult to manage the cookies
        result = CookiesResult()

        # Retrieve the cookie store from the WebView
        cookie_store = self.native.configuration.websiteDataStore.httpCookieStore

        # Call the method to retrieve all cookies and pass the completion handler
        cookie_store.getAllCookies(cookies_completion_handler(result))

        return result

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
