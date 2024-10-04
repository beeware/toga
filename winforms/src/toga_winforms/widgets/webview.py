import json
import webbrowser

import System.Windows.Forms as WinForms
from System import (
    Action,
    String,
    Uri,
)
from System.Drawing import Color
from System.Threading.Tasks import Task, TaskScheduler

import toga
from toga.widgets.webview import JavaScriptResult
from toga_winforms.libs.extensions import (
    CoreWebView2CreationProperties,
    WebView2,
    WebView2RuntimeNotFoundException,
)

from ..libs.wrapper import WeakrefCallable
from .base import Widget


def requires_initialization(method):
    def wrapper(self, *args, **kwargs):
        def task():
            method(self, *args, **kwargs)

        self.run_after_initialization(task)

    return wrapper


class WebView(Widget):
    def create(self):
        self.native = WebView2()
        self.native.CoreWebView2InitializationCompleted += WeakrefCallable(
            self.winforms_initialization_completed
        )
        self.native.NavigationCompleted += WeakrefCallable(
            self.winforms_navigation_completed
        )
        self.loaded_future = None

        props = CoreWebView2CreationProperties()
        props.UserDataFolder = str(toga.App.app.paths.cache / "WebView2")
        self.native.CreationProperties = props

        # Trigger the configuration of the webview
        self.corewebview2_available = None
        self.pending_tasks = []
        self.native.EnsureCoreWebView2Async(None)
        self.native.DefaultBackgroundColor = Color.Transparent

    # Any non-trivial use of the WebView requires the CoreWebView2 object to be
    # initialized, which is asynchronous. Since most of this class's methods are not
    # asynchronous, they cannot handle this using `await`. Instead, they add a callable
    # to a queue of pending tasks, which is processed once we receive the
    # CoreWebView2InitializationCompleted event.
    def run_after_initialization(self, task):
        if self.corewebview2_available:
            task()
        else:
            self.pending_tasks.append(task)

    def winforms_initialization_completed(self, sender, args):
        # The WebView2 widget has an "internal" widget (CoreWebView2) that is
        # the actual web view. The view isn't ready until the internal widget has
        # completed initialization, and that isn't done until an explicit
        # request is made (EnsureCoreWebView2Async).
        if args.IsSuccess:
            # We've initialized, so we must have the runtime
            self.corewebview2_available = True
            settings = self.native.CoreWebView2.Settings
            self.default_user_agent = settings.UserAgent

            debug = True
            settings.AreBrowserAcceleratorKeysEnabled = debug
            settings.AreDefaultContextMenusEnabled = debug
            settings.AreDefaultScriptDialogsEnabled = True
            settings.AreDevToolsEnabled = debug
            settings.IsBuiltInErrorPageEnabled = True
            settings.IsScriptEnabled = True
            settings.IsWebMessageEnabled = True
            settings.IsStatusBarEnabled = debug
            settings.IsSwipeNavigationEnabled = False
            settings.IsZoomControlEnabled = True

            for task in self.pending_tasks:
                task()
            self.pending_tasks = None

        elif isinstance(
            args.InitializationException, WebView2RuntimeNotFoundException
        ):  # pragma: nocover
            print("Could not find the Microsoft Edge WebView2 Runtime.")
            if self.corewebview2_available is None:
                # The initialize message is sent twice on failure.
                # We only want to show the dialog once, so track that we
                # know the runtime is missing.
                self.corewebview2_available = False
                WinForms.MessageBox.Show(
                    "The Microsoft Edge WebView2 Runtime is not installed. "
                    "Web content will not be displayed.\n\n"
                    "Click OK to download the WebView2 Evergreen Runtime "
                    "Bootstrapper from Microsoft.",
                    "Missing Edge Webview2 runtime",
                    WinForms.MessageBoxButtons.OK,
                    WinForms.MessageBoxIcon.Error,
                )
                webbrowser.open(
                    "https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download"
                )

        else:  # pragma: nocover
            WinForms.MessageBox.Show(
                "A critical error has occurred and functionality may be impaired.\n\n"
                "The WebView2 initialization failed with an exception:\n\n"
                f"{args.InitializationException}",
                "Error",
                WinForms.MessageBoxButtons.OK,
                WinForms.MessageBoxIcon.Error,
            )

    def winforms_navigation_completed(self, sender, args):
        self.interface.on_webview_load()

        if self.loaded_future:
            self.loaded_future.set_result(None)
            self.loaded_future = None

    def get_url(self):
        source = self.native.Source
        if source is None:  # pragma: nocover
            return None  # CoreWebView2 is not yet initialized.
        else:
            url = str(source)
            return None if url == "about:blank" else url

    @requires_initialization
    def set_url(self, value, future=None):
        self.loaded_future = future
        if value is None:
            self.set_content("about:blank", "")
        else:
            self.native.Source = Uri(value)

    @requires_initialization
    def set_content(self, root_url, content):
        # There appears to be no way to pass the root_url.
        self.native.NavigateToString(content)

    def get_user_agent(self):
        if self.corewebview2_available:
            return self.native.CoreWebView2.Settings.UserAgent
        else:  # pragma: nocover
            return ""

    @requires_initialization
    def set_user_agent(self, value):
        self.native.CoreWebView2.Settings.UserAgent = (
            self.default_user_agent if value is None else value
        )

    def evaluate_javascript(self, javascript, on_result=None):
        result = JavaScriptResult(on_result)
        task_scheduler = TaskScheduler.FromCurrentSynchronizationContext()

        def callback(task):
            # If the evaluation fails, task.Result will be "null", with no way to
            # distinguish it from an actual null return value.
            value = json.loads(task.Result)
            result.set_result(value)

        def execute():
            self.native.ExecuteScriptAsync(javascript).ContinueWith(
                Action[Task[String]](callback), task_scheduler
            )

        self.run_after_initialization(execute)
        return result
