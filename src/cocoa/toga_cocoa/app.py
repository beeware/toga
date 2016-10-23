import os
import signal

from toga.interface.app import App as AppInterface

from .libs import *
from .window import Window
from .widgets.icon import Icon, TIBERIUS_ICON


class MainWindow(Window):
    def __init__(self, title=None, position=(100, 100), size=(640, 480)):
        super(MainWindow, self).__init__(title, position, size)

    def on_close(self):
        self.app._impl.terminate_(self._delegate)


class AppDelegate(NSObject):
    @objc_method
    def applicationOpenUntitledFile_(self, sender) -> bool:
        # FIXME This should be all we need; but for some reason, application types
        # aren't being registered correctly..
        # NSDocumentController.sharedDocumentController().openDocument_(None)

        # ...so we do this instead.
        panel = NSOpenPanel.openPanel()
        print("Open documents of type", NSDocumentController.sharedDocumentController().defaultType)

        fileTypes = NSArray.alloc().initWithObjects_(*([d for d in self._interface.document_types] + [None]))
        NSDocumentController.sharedDocumentController().runModalOpenPanel_forTypes_(panel, fileTypes)

        print("Untitled File opened?", panel.URLs)
        self.application_openFiles_(None, panel.URLs)

        return True

    @objc_method
    def addDocument_(self, document) -> None:
        print("Add Document", document)
        super().addDocument_(document)

    @objc_method
    def applicationShouldOpenUntitledFile_(self, sender) -> bool:
        return True

    @objc_method
    def application_openFiles_(self, app, filenames) -> None:
        print("open file ", filenames)
        for i in range(0, filenames.count):
            filename = filenames.objectAtIndex_(i)
            print("OPEN", filename)
            if isinstance(filename, str):
                print("convert", filename, 'to URL')
                fileURL = NSURL.fileURLWithPath_(filename)

            elif filename.__dict__['objc_class'].__dict__['name'] == 'NSURL':
                # This case only exists because we aren't using the
                # DocumentController to display the file open dialog.
                # If we were, *all* filenames passed in would be
                # string paths.
                print("ALREADY A URL")
                fileURL = filename
            else:
                return

            self._interface.open_document(fileURL.absoluteString)
            # NSDocumentController.sharedDocumentController().openDocumentWithContentsOfURL_display_completionHandler_(fileURL, True, None)


class App(AppInterface):
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, name, app_id, icon=None, startup=None, document_types=None):
        # Set the icon for the app
        Icon.app_icon = Icon.load(icon, default=TIBERIUS_ICON)

        super().__init__(
            name=name,
            app_id=app_id,
            icon=Icon.app_icon,
            startup=startup,
            document_types=document_types
        )

    def _startup(self):
        self._impl = NSApplication.sharedApplication()
        self._impl.setActivationPolicy_(NSApplicationActivationPolicyRegular)

        self._impl.setApplicationIconImage_(self.icon._impl)

        self.resource_path = os.path.dirname(os.path.dirname(NSBundle.mainBundle().bundlePath))

        appDelegate = AppDelegate.alloc().init()
        appDelegate._interface = self
        self._impl.setDelegate_(appDelegate)

        app_name = self.name

        self.menu = NSMenu.alloc().initWithTitle_('MainMenu')

        # App menu
        self.app_menuItem = self.menu.addItemWithTitle_action_keyEquivalent_(app_name, None, '')
        submenu = NSMenu.alloc().initWithTitle_(app_name)

        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('About ' + app_name, None, '')
        submenu.addItem_(menu_item)

        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Preferences', None, '')
        submenu.addItem_(menu_item)

        submenu.addItem_(NSMenuItem.separatorItem())

        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit ' + app_name, get_selector('terminate:'), "q")
        submenu.addItem_(menu_item)

        self.menu.setSubmenu_forItem_(submenu, self.app_menuItem)

        # Help menu
        self.help_menuItem = self.menu.addItemWithTitle_action_keyEquivalent_('Apple', None, '')
        submenu = NSMenu.alloc().initWithTitle_('Help')

        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Visit homepage', None, '')
        submenu.addItem_(menu_item)

        self.menu.setSubmenu_forItem_(submenu, self.help_menuItem)

        # Set the menu for the app.
        self._impl.setMainMenu_(self.menu)

        # Call user code to populate the main window
        self.startup()

    def main_loop(self):
        # Stimulate the build of the app
        self._startup()
        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self._impl.activateIgnoringOtherApps_(True)
        self._impl.run()
