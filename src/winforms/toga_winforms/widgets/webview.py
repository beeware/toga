from asyncio import get_event_loop
import toga
import traceback
import webbrowser

from travertino.size import at_least

from toga_winforms.keys import toga_key
from toga_winforms.libs import (
    Action,
    CoreWebView2CreationProperties,
    String,
    Task,
    TaskScheduler,
    Uri,
    WebView2,
    WebView2RuntimeNotFoundException,
    WinForms
)

from .base import Widget


class TogaWebBrowser(WebView2):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self._edge_runtime_available = None  # Set to an unknown state initially


class WebView(Widget):
    def create(self):
        self.native = TogaWebBrowser(self.interface)
        self.native.CoreWebView2InitializationCompleted += self.winforms_initialization_completed
        self.native.NavigationCompleted += self.winforms_navigation_completed
        self.native.KeyDown += self.winforms_key_down

        props = CoreWebView2CreationProperties()
        props.UserDataFolder = str(toga.App.app.paths.cache / "WebView2")
        self.native.CreationProperties = props

        # Trigger the configuration of the webview
        self.native.EnsureCoreWebView2Async(None)

    def winforms_initialization_completed(self, sender, args):
        # The WebView2 widget has an "internal" widget (CoreWebView2) that is
        # the actual web view. The view isn't ready until the internal widget has
        # completed initialization, and that isn't done until an explicit
        # request is made (EnsureCoreWebView2Async).
        if args.IsSuccess:
            # We've initialized, so we must have the runtime
            self.native._edge_runtime_available = True
            try:
                settings = self.native.CoreWebView2.Settings

                debug = True
                settings.AreDefaultContextMenusEnabled = debug
                settings.AreDefaultScriptDialogsEnabled = True
                settings.AreDevToolsEnabled = debug
                settings.IsBuiltInErrorPageEnabled = True
                settings.IsScriptEnabled = True
                settings.IsWebMessageEnabled = True
                settings.IsStatusBarEnabled = debug
                settings.IsZoomControlEnabled = True

                self.set_user_agent(self.interface.user_agent)

                if self.interface._html_content:
                    self.set_content(self.interface.url, self.interface._html_content)
                else:
                    self.set_url(self.interface.url)

            except Exception:
                traceback.print_exc()
        else:
            if isinstance(
                args.InitializationException,
                WebView2RuntimeNotFoundException
            ):
                print("Could not find the Microsoft Edge WebView2 Runtime.")
                if self.native._edge_runtime_available is None:
                    # The initialize message is sent twice on failure.
                    # We only want to show the dialog once, so track that we
                    # know the runtime is missing.
                    self.native._edge_runtime_available = False
                    WinForms.MessageBox.Show(
                        "The Microsoft Edge WebView2 Runtime is not installed. "
                        "Web content will not be displayed.\n\n"
                        "Click OK to download the WebView2 Evergreen Runtime "
                        "Bootstrapper from Microsoft.",
                        "Missing Edge Webview2 runtime",
                        WinForms.MessageBoxButtons.OK,
                        WinForms.MessageBoxIcon.Error,
                    )
                    webbrowser.open("https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download-section")
            else:
                print(args.InitializationException)

    def winforms_navigation_completed(self, sender, args):
        if self.interface.on_webview_load:
            self.interface.on_webview_load(self.interface)

    def winforms_key_down(self, sender, args):
        if self.interface.on_key_down:
            self.interface.on_key_down(self.interface, **toga_key(args))

    def set_on_key_down(self, handler):
        pass

    def set_on_webview_load(self, handler):
        pass

    def get_url(self):
        return str(self.native.Source)

    def set_url(self, value):
        if value:
            self.native.Source = Uri(value)

    def set_content(self, root_url, content):
        if content and self.native.CoreWebView2:
            self.native.CoreWebView2.NavigateToString(content)

    def get_dom(self):
        self.interface.factory.not_implemented('WebView.get_dom()')

    def set_user_agent(self, value):
        user_agent = value if value else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46"  # NOQA
        if self.native.CoreWebView2:
            self.native.CoreWebView2.Settings.UserAgent = user_agent

    async def evaluate_javascript(self, javascript):
        loop = get_event_loop()
        future = loop.create_future()

        task_scheduler = TaskScheduler.FromCurrentSynchronizationContext()
        try:
            def callback(task):
                future.set_result(task.Result)

            self.native.ExecuteScriptAsync(javascript).ContinueWith(
                Action[Task[String]](callback),
                task_scheduler
            )
        except Exception:
            traceback.print_exc()
            future.set_result(None)

        return await future

    def invoke_javascript(self, javascript):
        # The script will execute async, but you weren't going to get the result
        # anyway, so it doesn't really matter.
        self.native.ExecuteScriptAsync(javascript)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
