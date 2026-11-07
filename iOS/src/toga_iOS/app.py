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
        App.app.uikit_scene_willConnectToSession_options(scene, session, options)

    @objc_method
    def sceneDidDisconnect_(self, scene) -> None:
        App.app.uikit_sceneDidDisconnect(scene)

    @objc_method
    def sceneDidBecomeActive_(self, scene) -> None:
        App.app.uikit_sceneDidBecomeActive(scene)

    @objc_method
    def sceneWillResignActive_(self, scene) -> None:
        App.app.uikit_sceneWillResignActive(scene)

    @objc_method
    def sceneDidEnterBackground_(self, scene) -> None:
        App.app.uikit_sceneDidEnterBackground(scene)

    @objc_method
    def sceneWillEnterForeground_(self, scene) -> None:
        App.app.uikit_sceneWillEnterForeground(scene)


class PythonAppDelegate(UIResponder):
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
    def application_willFinishLaunchingWithOptions_(
        self, application, launchOptions
    ) -> bool:
        return App.app.uikit_application_willFinishLaunchingWithOptions(
            application, launchOptions
        )

    @objc_method
    def application_didFinishLaunchingWithOptions_(
        self, application, launchOptions
    ) -> bool:
        return App.app.uikit_application_didFinishLaunchingWithOptions(
            application, launchOptions
        )

    @objc_method
    def applicationDidReceiveMemoryWarning_(self, application) -> None:
        App.app.uikit_applicationDidReceiveMemoryWarning(application)

    @objc_method
    def applicationSignificantTimeChange_(self, application) -> None:
        App.app.uikit_applicationSignificantTimeChange(application)

    @objc_method
    def applicationProtectedDataWillBecomeUnavailable_(self, application) -> None:
        App.app.uikit_applicationProtectedDataWillBecomeUnavailable(application)

    @objc_method
    def applicationProtectedDataDidBecomeAvailable_(self, application) -> None:
        App.app.uikit_applicationProtectedDataDidBecomeAvailable(application)

    @objc_method
    def applicationWillTerminate_(self, application) -> None:
        App.app.uikit_applicationWillTerminate(application)


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
    # Platform-specific app lifecycle hooks
    ######################################################################

    def uikit_application_willFinishLaunchingWithOptions(
        self, application, launchOptions
    ) -> bool:
        """Invoked by `application:willFinishLaunchingWithOptions:`.

        Returns `True` by default. The return value is passed back to iOS.
        """
        return True

    def uikit_application_didFinishLaunchingWithOptions(
        self, application, launchOptions
    ) -> bool:
        """Invoked by `application:didFinishLaunchingWithOptions:`.

        By default, this creates the app and shows the main window. An override
        must call the base implementation and return its result.
        """
        self.native = application
        self.create()
        self.interface.current_window.on_show()
        return True

    def uikit_applicationDidReceiveMemoryWarning(self, application):
        """Invoked by `applicationDidReceiveMemoryWarning:`. No-op by default."""

    def uikit_applicationSignificantTimeChange(self, application):
        """Invoked by `applicationSignificantTimeChange:`. No-op by default."""

    def uikit_applicationProtectedDataWillBecomeUnavailable(self, application):
        """Invoked by `applicationProtectedDataWillBecomeUnavailable:`. No-op by
        default."""

    def uikit_applicationProtectedDataDidBecomeAvailable(self, application):
        """Invoked by `applicationProtectedDataDidBecomeAvailable:`. No-op by
        default."""

    def uikit_applicationWillTerminate(self, application):
        """Invoked by `applicationWillTerminate:`. No-op by default."""

    def uikit_scene_willConnectToSession_options(self, scene, session, options):
        """Invoked by `scene:willConnectToSession:options:`.

        By default, this attaches the main window to the scene and makes it
        visible.
        """
        assert isinstance(scene, UIWindowScene), "iOS should provide UIWindowScene"
        window = self.interface.current_window._impl.native
        window.windowScene = scene
        scene.delegate.window = window
        window.makeKeyAndVisible()

    def uikit_sceneDidDisconnect(self, scene):
        """Invoked by `sceneDidDisconnect:`. No-op by default."""

    def uikit_sceneDidBecomeActive(self, scene):
        """Invoked by `sceneDidBecomeActive:`. By default, this triggers
        `on_gain_focus` on the current window."""
        self.interface.current_window.on_gain_focus()

    def uikit_sceneWillResignActive(self, scene):
        """Invoked by `sceneWillResignActive:`. By default, this triggers
        `on_lose_focus` on the current window."""
        self.interface.current_window.on_lose_focus()

    def uikit_sceneDidEnterBackground(self, scene):
        """Invoked by `sceneDidEnterBackground:`. By default, this triggers
        `on_hide` on the current window."""
        self.interface.current_window.on_hide()

    def uikit_sceneWillEnterForeground(self, scene):
        """Invoked by `sceneWillEnterForeground:`. By default, this triggers
        `on_show` on the current window."""
        self.interface.current_window.on_show()

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
