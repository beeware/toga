import asyncio

from rubicon.objc import SEL, objc_method
from rubicon.objc.eventloop import EventLoopPolicy, iOSLifecycle

from toga_iOS.libs import (
    NSNotificationCenter,
    UIKeyboardFrameEndUserInfoKey,
    UIKeyboardWillHideNotification,
    UIKeyboardWillShowNotification,
    UIResponder,
)
from toga_iOS.window import Window


class MainWindow(Window):
    pass


class PythonAppDelegate(UIResponder):
    @objc_method
    def applicationDidBecomeActive_(self, application) -> None:
        print("App became active.")

    @objc_method
    def applicationWillResignActive_(self, application) -> None:
        print("App about to leave foreground.", flush=True)

    @objc_method
    def applicationDidEnterBackground_(self, application) -> None:
        print("App entered background.")

    @objc_method
    def applicationWillEnterForeground_(self, application) -> None:
        print("App about to enter foreground.")

    @objc_method
    def application_didFinishLaunchingWithOptions_(
        self, application, launchOptions
    ) -> bool:
        print("App finished launching.")
        App.app.create()

        NSNotificationCenter.defaultCenter.addObserver(
            self,
            selector=SEL("keyboardWillShow:"),
            name=UIKeyboardWillShowNotification,
            object=None,
        )
        NSNotificationCenter.defaultCenter.addObserver(
            self,
            selector=SEL("keyboardWillHide:"),
            name=UIKeyboardWillHideNotification,
            object=None,
        )
        # Set the initial keyboard size.
        App.app.interface.main_window.content._impl.viewport.kb_height = 0.0

        return True

    @objc_method
    def applicationWillTerminate_(self, application) -> None:
        print("App about to Terminate.")

    @objc_method
    def application_didChangeStatusBarOrientation_(
        self, application, oldStatusBarOrientation: int
    ) -> None:
        """This callback is invoked when rotating the device from landscape to
        portrait and vice versa."""
        App.app.interface.main_window.content.refresh()

    @objc_method
    def keyboardWillShow_(self, notification) -> None:
        # Keyboard is about to be displayed.
        # This will fire multiple times - once to display the keyboard,
        # and again to display the autocomplete bar.
        kb_height = App.app.interface.main_window._impl.controller.view.convertRect(
            notification.userInfo.objectForKey(
                UIKeyboardFrameEndUserInfoKey
            ).CGRectValue,
            fromView=None,
        ).size.height
        App.app.interface.main_window.content._impl.viewport.kb_height = kb_height

        App.app.interface.main_window.content.refresh()

    @objc_method
    def keyboardWillHide_(self, notification) -> None:
        # Reset the layout to the size of the screen.
        App.app.interface.main_window.content._impl.viewport.kb_height = 0.0
        App.app.interface.main_window.content.refresh()


class App:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        App.app = self  # Add a reference for the PythonAppDelegate class to use.

        asyncio.set_event_loop_policy(EventLoopPolicy())
        self.loop = asyncio.new_event_loop()

    def create(self):
        """Calls the startup method on the interface."""
        self.interface.startup()

    def open_document(self, fileURL):
        """Add a new document to this app."""
        pass

    def main_loop(self):
        # Main loop is non-blocking on iOS. The app loop is integrated with the
        # main iOS event loop, so this call will return; however, it will leave
        # the app in a state such that asyncio events will be scheduled on the
        # iOS event loop.
        self.loop.run_forever_cooperatively(lifecycle=iOSLifecycle())

    def set_main_window(self, window):
        pass

    def show_about_dialog(self):
        self.interface.factory.not_implemented("App.show_about_dialog()")

    def exit(self):
        pass

    def set_on_exit(self, value):
        pass
