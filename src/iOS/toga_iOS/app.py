import asyncio

from rubicon.objc import objc_method
from rubicon.objc.async import EventLoopPolicy, iOSLifecycle

from .libs import *
from .window import Window


class MainWindow(Window):
    def __init__(self, interface):
        super().__init__(interface)

    # def startup(self):
    #     super(MainWindow, self).startup()
    #     self.native.setBackgroundColor_(UIColor.whiteColor())


class PythonAppDelegate(UIResponder):
    @objc_method
    def applicationDidBecomeActive(self) -> None:
        print("App became active.")

    @objc_method
    def application_didFinishLaunchingWithOptions_(self, application, launchOptions) -> bool:
        print("App finished launching.")
        App.app.create()

        NSNotificationCenter.defaultCenter.addObserver(
            self,
            selector=SEL('keyboardWillShow:'),
            name=UIKeyboardWillShowNotification,
            object=None
        )
        NSNotificationCenter.defaultCenter.addObserver(
            self,
            selector=SEL('keyboardWillHide:'),
            name=UIKeyboardWillHideNotification,
            object=None
        )
        # Set the initial keyboard size.
        self.kb_height = 0.0

        return True

    @objc_method
    def application_didChangeStatusBarOrientation_(self, application, oldStatusBarOrientation: int) -> None:
        """ This callback is invoked when rotating the device from landscape to portrait and vice versa. """
        App.app.interface.main_window.content._update_layout(
            width=App.app.interface.main_window._impl.screen.bounds.size.width,
            height=App.app.interface.main_window._impl.screen.bounds.size.height,
        )

    @objc_method
    def keyboardWillShow_(self, notification) -> None:
        # Keyboard is about to be displayed.
        # This will fire multiple times - once to display the keyboard,
        # and again to display the autocomplete bar.
        kb_height = App.app.interface.main_window._impl.controller.view.convertRect(
                notification.userInfo.objectForKey(UIKeyboardFrameEndUserInfoKey).CGRectValue,
                fromView=None
            ).size.height

        old_rect = App.app.interface.main_window._impl.controller.view.frame
        # Adjust the content rectangle so that it is smaller.
        # A different sized keyboard might already be displayed, so
        # offset
        # rect = NSMakeRect(
        #     old_rect.origin.x, old_rect.origin.y,
        #     old_rect.size.width, old_rect.size.height + self.kb_height - kb_height
        # )
        new_rect = NSMakeRect(
            old_rect.origin.x, -kb_height,
            old_rect.size.width, old_rect.size.height
        )
        App.app.interface.main_window._impl.controller.view.frame = new_rect

        # Preserve the new keyboard height.
        self.kb_height = kb_height

    @objc_method
    def keyboardWillHide_(self, notification) -> None:
        old_rect = App.app.interface.main_window._impl.controller.view.frame

        # Reset the size of the content rectangle, compensating for the
        # keyboard that was most recently displayed
        # new_rect = NSMakeRect(
        #     old_rect.origin.x, old_rect.origin.x,
        #     old_rect.size.width, old_rect.size.height + self.kb_height
        # )
        new_rect = NSMakeRect(
            old_rect.origin.x, 0.0,
            old_rect.size.width, old_rect.size.height
        )
        App.app.interface.main_window._impl.controller.view.frame = new_rect


class App:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        App.app = self  # Add a reference for the PythonAppDelegate class to use.

        asyncio.set_event_loop_policy(EventLoopPolicy())
        self.loop = asyncio.get_event_loop()

    def create(self):
        """ Calls the startup method on the interface """
        self.interface.startup()

    def open_document(self, fileURL):
        """ Add a new document to this app."""
        pass

    def main_loop(self):
        # Main loop is a no-op on iOS; the app loop is integrated with the
        # main iOS event loop.

        self.loop.run_forever(lifecycle=iOSLifecycle())
