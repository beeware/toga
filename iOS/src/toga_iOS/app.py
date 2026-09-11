from rubicon.objc import objc_method, objc_property
from rubicon.objc.eventloop import RubiconEventLoop, iOSLifecycle

import toga
from toga_iOS.libs import (
    UIResponder,
    UISceneConfiguration,
    UIScreen,
    UIWindowScene,
    UIWindowSceneDelegate,
    UIWindowSceneSessionRoleApplication,
    av_foundation,
)

from .screens import Screen as ScreenImpl


class PythonSceneDelegate(UIResponder, protocols=(UIWindowSceneDelegate,)):
    # UIWindowSceneDelegate requires a 'window' property
    window = objc_property()

    @objc_method
    def scene_willConnectToSession_options_(self, scene, session, options) -> None:
        assert isinstance(scene, UIWindowScene), "iOS should provide UIWindowScene"

        # Associate pre-created single main window with the scene
        window = App.app.interface.current_window._impl.native
        window.windowScene = scene

        self.window = window
        window.makeKeyAndVisible()

    @objc_method
    def sceneDidBecomeActive_(self, scene) -> None:
        print("Scene became active.")
        App.app.interface.current_window.on_gain_focus()

    @objc_method
    def sceneWillResignActive_(self, scene) -> None:
        print("Scene about to leave foreground.", flush=True)
        App.app.interface.current_window.on_lose_focus()

    @objc_method
    def sceneDidEnterBackground_(self, scene) -> None:
        print("Scene entered background.")
        App.app.interface.current_window.on_hide()

    @objc_method
    def sceneWillEnterForeground_(self, scene) -> None:
        print("Scene about to enter foreground.")
        App.app.interface.current_window.on_show()


class PythonAppDelegate(UIResponder):
    @objc_method
    def applicationDidBecomeActive_(self, application) -> None:
        print("App became active.")
        App.app.interface.current_window.on_gain_focus()

    @objc_method
    def applicationWillResignActive_(self, application) -> None:
        print("App about to leave foreground.", flush=True)
        App.app.interface.current_window.on_lose_focus()

    @objc_method
    def applicationDidEnterBackground_(self, application) -> None:
        print("App entered background.")
        App.app.interface.current_window.on_hide()

    @objc_method
    def applicationWillEnterForeground_(self, application) -> None:
        print("App about to enter foreground.")
        App.app.interface.current_window.on_show()

    @objc_method
    def application_configurationForConnectingSceneSession_options_(
        self, application, connectingSceneSession, options
    ):
        configuration = UISceneConfiguration.alloc().initWithName_sessionRole_(
            "Default Configuration", UIWindowSceneSessionRoleApplication
        )
        configuration.delegateClass = PythonSceneDelegate
        return configuration

    @objc_method
    def application_didFinishLaunchingWithOptions_(
        self, application, launchOptions
    ) -> bool:
        print("App finished launching.")
        App.app.native = application
        App.app.create()
        App.app.interface.current_window.on_show()
        return True

    @objc_method
    def applicationWillTerminate_(self, application) -> None:
        print("App about to Terminate.")


class App:
    # iOS apps exit when the last window is closed
    CLOSE_ON_LAST_WINDOW = True
    # iOS doesn't have command line handling;
    # but saying it does shortcuts the default handling
    HANDLES_COMMAND_LINE = True

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        # Native instance doesn't exist until the lifecycle completes.
        self.native = None

        # Add a reference for the PythonAppDelegate class to use.
        App.app = self

        self._exiting_presentation = False

        self.loop = RubiconEventLoop()

    def create(self):
        """Calls the startup method on the interface."""
        self.interface._startup()

    ######################################################################
    # Commands and menus
    ######################################################################

    def create_standard_commands(self):
        pass

    def create_menus(self):
        # No menus on an iOS app (for now)
        pass

    ######################################################################
    # App lifecycle
    ######################################################################

    def exit(self):  # pragma: no cover
        # Mobile apps can't be exited, but the entry point needs to exist
        pass

    def main_loop(self):
        # Main loop is non-blocking on iOS. The app loop is integrated with the
        # main iOS event loop, so this call will return; however, it will leave
        # the app in a state such that asyncio events will be scheduled on the
        # iOS event loop.
        self.loop.run_forever_cooperatively(lifecycle=iOSLifecycle())

    def set_icon(self, icon):
        # iOS apps don't have runtime icons, so this can't be invoked
        pass  # pragma: no cover

    def set_main_window(self, window):
        if window is None or window == toga.App.BACKGROUND:
            raise ValueError("Apps without main windows are not supported on iOS")

    ######################################################################
    # App resources
    ######################################################################

    def get_screens(self):
        return [ScreenImpl(UIScreen.mainScreen)]

    ######################################################################
    # App state
    ######################################################################

    def get_dark_mode_state(self):
        # UIUserInterfaceStyle is an enum with the following values:
        # 0: Unspecified
        # 1: Light
        # 2: Dark
        return UIScreen.mainScreen.traitCollection.userInterfaceStyle == 2

    ######################################################################
    # App capabilities
    ######################################################################

    def beep(self):
        # 1013 is a magic constant that is the "SMS RECEIVED 5" sound,
        # sounding like a single strike of a bell.
        av_foundation.AudioServicesPlayAlertSound(1013)

    def open_document(self, fileURL):  # pragma: no cover
        """Add a new document to this app."""

    def show_about_dialog(self):
        self.interface.factory.not_implemented("App.show_about_dialog()")

    ######################################################################
    # Cursor control
    ######################################################################

    def hide_cursor(self):
        # No-op; mobile doesn't support cursors
        pass

    def show_cursor(self):
        # No-op; mobile doesn't support cursors
        pass

    ######################################################################
    # Window control
    ######################################################################

    def get_current_window(self):
        # iOS only has a main window.
        return self.interface.main_window._impl

    def set_current_window(self, window):
        # iOS only has a main window, so this is a no-op
        pass
