from http.cookiejar import Cookie, CookieJar

from rubicon.objc import ObjCBlock, objc_id, objc_method, objc_property, py_from_ns
from travertino.size import at_least

from toga.widgets.webview import CookiesResult, JavaScriptResult

from ..libs import (
    NSURL,
    NSModalResponseOK,
    NSOpenPanel,
    NSURLRequest,
    WKUIDelegate,
    WKWebView,
)
from .base import Widget


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
    def webView_didFinishNavigation_(self, navigation) -> None:
        # It's possible for this handler to be invoked *after* the interface/impl object
        # has been destroyed. If the interface/impl doesn't exist there's no handler to
        # invoke either, so ignore the edge case. This can't be reproduced reliably, so
        # don't check coverage on the `is None` case.
        if self.interface:  # pragma: no branch
            self.interface.on_webview_load()

        if self.impl and self.impl.loaded_future:  # pragma: no branch
            self.impl.loaded_future.set_result(None)
            self.impl.loaded_future = None

    @objc_method
    def acceptsFirstResponder(self) -> bool:
        return True

    # WKUIDelegate protocol method required to utilize the open file dialog for
    # uploading a file to a website. Difficult to automatically test because it
    # uses :param: completionHandler, which is a method utilized by the under-
    # lying WKWebView objective-C codebase. :param: completionHandler cannot be
    # created manually for testing because it is difficult to pull it up from
    # the native codebase.
    @objc_method
    def webView_runOpenPanelWithParameters_initiatedByFrame_completionHandler_(
        self, webView, parameters, frame, completionHandler
    ) -> None:  # pragma: no cover
        """Required by the WKUIDelegate protocol.

        Called when the user clicks on an <input type="file"> HTML tag,
        or something like the js func window.showOpenFilePicker.

        :param webView: The web view invoking the delegate method.
        :param parameters: The parameters describing the file upload control.
        Has two attributes: allowsMultipleSelection and allowsDirectories
        :param frame: The frame whose file upload control initiated the call.
        :param completionHandler: The completion handler called after the open
        panel has been dismissed.
        :returns: Nothing
        """
        # Create open file dialog panel and set parameters
        # Because of the "native" approach required for this method,
        # the OpenFileDialog and SelectFolderDialog classes were not
        # reused from dialogs.py
        open_panel = NSOpenPanel.alloc().init()
        open_panel.allowsMultipleSelection = parameters.allowsMultipleSelection
        open_panel.canChooseDirectories = parameters.allowsDirectories
        open_panel.canCreateDirectories = parameters.allowsDirectories
        open_panel.canChooseFiles = not parameters.allowsDirectories
        open_panel.resolvesAliases = parameters.allowsDirectories

        def _completion_handler(res: int) -> None:
            if res == NSModalResponseOK:
                ObjCBlock(completionHandler, None, objc_id)(open_panel.URLs)
            else:
                ObjCBlock(completionHandler, None, objc_id)(None)

        open_panel.beginWithCompletionHandler(_completion_handler)


class WebView(Widget):
    def create(self):
        self.native = TogaWebView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        # Enable the content inspector. This was added in macOS 13.3 (Ventura). It will
        # be a no-op on newer versions of macOS; you need to package the app, then run:
        #
        #     defaults write com.example.appname WebKitDeveloperExtras -bool true
        #
        # from the command line.
        self.native.inspectable = True
        self.native.navigationDelegate = self.native
        # Set UIDelegate to self for file dialog support
        self.native.UIDelegate = self.native

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

    def evaluate_javascript(self, javascript: str, on_result=None) -> str:
        result = JavaScriptResult(on_result=on_result)
        self.native.evaluateJavaScript(
            javascript,
            completionHandler=js_completion_handler(result),
        )

        return result

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
