import asyncio

from rubicon.objc import objc_method
from rubicon.objc.eventloop import EventLoopPolicy, iOSLifecycle

from toga_iOS.libs import UIResponder, av_foundation
from toga_iOS.window import Window


class MainWindow(Window):
    _is_main_window = True


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

    def open_document(self, fileURL):  # pragma: no cover
        """Add a new document to this app."""
        pass

    def create_menus(self):
        # No menus on an iOS app (for now)
        pass

    def main_loop(self):
        # Main loop is non-blocking on iOS. The app loop is integrated with the
        # main iOS event loop, so this call will return; however, it will leave
        # the app in a state such that asyncio events will be scheduled on the
        # iOS event loop.
        self.loop.run_forever_cooperatively(lifecycle=iOSLifecycle())

    def set_main_window(self, window):
        pass

    def get_current_window(self):
        # iOS only has a main window.
        return self.interface.main_window._impl

    def set_current_window(self, window):
        # iOS only has a main window, so this is a no-op
        pass

    def show_about_dialog(self):
        self.interface.factory.not_implemented("App.show_about_dialog()")

    def beep(self):
        # 1013 is a magic constant that is the "SMS RECEIVED 5" sound,
        # sounding like a single strike of a bell.
        av_foundation.AudioServicesPlayAlertSound(1013)

    def exit(self):  # pragma: no cover
        # Mobile apps can't be exited, but the entry point needs to exist
        pass

    def enter_full_screen(self, windows):
        # No-op; mobile doesn't support full screen
        pass

    def exit_full_screen(self, windows):
        # No-op; mobile doesn't support full screen
        pass

    def hide_cursor(self):
        # No-op; mobile doesn't support cursors
        pass

    def show_cursor(self):
        # No-op; mobile doesn't support cursors
        pass
