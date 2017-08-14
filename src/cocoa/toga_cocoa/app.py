import os
import signal
import sys

from toga.interface.app import App as AppInterface
from toga.interface.command import GROUP_BREAK, SECTION_BREAK

from .command import Command, Group
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
        # print("Open documents of type", NSDocumentController.sharedDocumentController().defaultType)

        fileTypes = NSMutableArray.alloc().init()
        for filetype in self._interface.document_types:
            fileTypes.addObject(filetype)

        NSDocumentController.sharedDocumentController().runModalOpenPanel(panel, forTypes=fileTypes)

        # print("Untitled File opened?", panel.URLs)
        self.application_openFiles_(None, panel.URLs)

        return True

    @objc_method
    def addDocument_(self, document) -> None:
        # print("Add Document", document)
        super().addDocument_(document)

    @objc_method
    def applicationShouldOpenUntitledFile_(self, sender) -> bool:
        return True

    @objc_method
    def application_openFiles_(self, app, filenames) -> None:
        for i in range(0, len(filenames)):
            filename = filenames.objectAtIndex(i)
            if isinstance(filename, str):
                fileURL = NSURL.fileURLWithPath(filename)

            elif filename.objc_class.name == 'NSURL':
                # This case only exists because we aren't using the
                # DocumentController to display the file open dialog.
                # If we were, *all* filenames passed in would be
                # string paths.
                fileURL = filename
            else:
                return

            self._interface.open_document(fileURL.absoluteString)
            # NSDocumentController.sharedDocumentController().openDocumentWithContentsOfURL_display_completionHandler_(fileURL, True, None)

    @objc_method
    def selectMenuItem_(self, sender) -> None:
        cmd = self._interface._menu_items[sender]
        if cmd.action:
            cmd.action(None)


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

        self.resource_path = os.path.dirname(os.path.dirname(NSBundle.mainBundle.bundlePath))

        appDelegate = AppDelegate.alloc().init()
        appDelegate._interface = self
        self._impl.delegate = appDelegate

        app_name = self.name

        self.commands.add(
            Command(None, 'About ' + app_name, group=Group.APP),
            Command(None, 'Preferences', group=Group.APP),
            # Quit should always be the last item, in a section on it's own
            Command(lambda s: self.exit(), 'Quit ' + app_name, shortcut='q', group=Group.APP, section=sys.maxsize),

            Command(None, 'Visit homepage', group=Group.HELP)
        )

        # Call user code to populate the main window
        self.startup()

        # Create the lookup table of menu items,
        # then force the creation of the menus.
        self._menu_items = {}
        self._create_menus()

    def open_document(self, fileURL):
        '''Add a new document to this app.'''
        print("STUB: If you want to handle opening documents, implement App.open_document(fileURL)")

    def _create_menus(self):
        # Only create the menu if the menu item index has been created.
        if hasattr(self, '_menu_items'):
            self._menu_items = {}
            menubar = NSMenu.alloc().initWithTitle('MainMenu')
            submenu = None
            for cmd in self.commands:
                if cmd == GROUP_BREAK:
                    menubar.setSubmenu(submenu, forItem=menuItem)
                    submenu = None
                elif cmd == SECTION_BREAK:
                    submenu.addItem_(NSMenuItem.separatorItem())
                else:
                    if submenu is None:
                        menuItem = menubar.addItemWithTitle(cmd.group.label, action=None, keyEquivalent='')
                        submenu = NSMenu.alloc().initWithTitle(cmd.group.label)
                        submenu.setAutoenablesItems(False)

                    item = NSMenuItem.alloc().initWithTitle(
                        cmd.label,
                        action=SEL('selectMenuItem:'),
                        keyEquivalent=cmd.shortcut if cmd.shortcut else ''
                    )

                    cmd._widgets.append(item)
                    self._menu_items[item] = cmd

                    cmd._set_enabled(cmd.enabled)
                    submenu.addItem(item)

            if submenu:
                menubar.setSubmenu(submenu, forItem=menuItem)

            # Set the menu for the app.
            self._impl.mainMenu = menubar

    def main_loop(self):
        # Stimulate the build of the app
        self._startup()
        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self._impl.activateIgnoringOtherApps_(True)
        self._impl.run()

    def exit(self):
        self._impl.terminate(None)

