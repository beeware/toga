import asyncio

from rubicon.objc import objc_method
from rubicon.objc.eventloop import EventLoopPolicy, iOSLifecycle

from toga_iOS.libs import UIResponder
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
        App.app.native = application
        App.app.create()
        return True

    @objc_method
    def applicationWillTerminate_(self, application) -> None:
        print("App about to Terminate.")

    @objc_method
    def application_didChangeStatusBarOrientation_(
        self, application, oldStatusBarOrientation: int
    ) -> None:
        """This callback is invoked when rotating the device from landscape to portrait
        and vice versa."""
        App.app.interface.main_window.content.refresh()


class App:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        # Native instance doesn't exist until the lifecycle completes.
        self.native = None

        # Add a reference for the PythonAppDelegate class to use.
        App.app = self

        asyncio.set_event_loop_policy(EventLoopPolicy())
        self.loop = asyncio.new_event_loop()

    def create(self):
        """Calls the startup method on the interface."""
        self.interface._startup()

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

    def beep(self):
        self.interface.factory.not_implemented("App.beep()")

    def exit(self):
        pass

    def hide_cursor(self):
        pass

    def show_cursor(self):
        pass
