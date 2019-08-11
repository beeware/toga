import asyncio
import os
import sys
from urllib.parse import unquote, urlparse

import toga
from rubicon.objc import objc_method, NSMutableArray, NSMutableDictionary, NSObject, SEL
from rubicon.objc.eventloop import EventLoopPolicy, CocoaLifecycle

from .libs import (
    NSURL, NSBundle, NSOpenPanel, NSDocumentController, NSString, NSApplication,
    NSApplicationActivationPolicyRegular, NSNumber, NSMenu, NSMenuItem, NSScreen,
    NSCursor
)
from .window import Window


class MainWindow(Window):
    def on_close(self):
        self.interface.app.exit()


class AppDelegate(NSObject):
    @objc_method
    def applicationWillTerminate_(self, sender):
        if self.interface.app.on_exit:
            self.interface.app.on_exit(self.interface.app)

    @objc_method
    def applicationDidFinishLaunching_(self, notification):
        self.native.activateIgnoringOtherApps(True)

    @objc_method
    def applicationOpenUntitledFile_(self, sender) -> bool:
        self.impl.select_file()
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
            filename = filenames[i]
            if isinstance(filename, NSString):
                fileURL = NSURL.fileURLWithPath(filename)

            elif isinstance(filename, NSURL):
                # This case only exists because we aren't using the
                # DocumentController to display the file open dialog.
                # If we were, *all* filenames passed in would be
                # string paths.
                fileURL = filename
            else:
                return

            self.impl.open_document(str(fileURL.absoluteString))

    @objc_method
    def selectMenuItem_(self, sender) -> None:
        cmd = self.interface._impl._menu_items[sender]
        if cmd.action:
            cmd.action(None)


class App:
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self._cursor_visible = True

        asyncio.set_event_loop_policy(EventLoopPolicy())
        self.loop = asyncio.get_event_loop()

    def create(self):
        self.native = NSApplication.sharedApplication
        self.native.setActivationPolicy(NSApplicationActivationPolicyRegular)

        self.native.setApplicationIconImage_(self.interface.icon.bind(self.interface.factory).native)

        self.resource_path = os.path.dirname(os.path.dirname(NSBundle.mainBundle.bundlePath))

        self.appDelegate = AppDelegate.alloc().init()
        self.appDelegate.impl = self
        self.appDelegate.interface = self.interface
        self.appDelegate.native = self.native
        self.native.setDelegate_(self.appDelegate)

        app_name = self.interface.name

        self.interface.commands.add(
            toga.Command(None, 'About ' + app_name, group=toga.Group.APP),
            toga.Command(None, 'Preferences', group=toga.Group.APP),
            # Quit should always be the last item, in a section on it's own
            toga.Command(lambda s: self.exit(), 'Quit ' + app_name, shortcut='q', group=toga.Group.APP, section=sys.maxsize),

            toga.Command(None, 'Visit homepage', group=toga.Group.HELP)
        )
        self._create_app_commands()

        # Call user code to populate the main window
        self.interface.startup()

        # Create the lookup table of menu items,
        # then force the creation of the menus.
        self._menu_items = {}
        self.create_menus()

    def _create_app_commands(self):
        # No extra commands
        pass

    def create_menus(self):
        # Only create the menu if the menu item index has been created.
        if hasattr(self, '_menu_items'):
            self._menu_items = {}
            menubar = NSMenu.alloc().initWithTitle('MainMenu')
            submenu = None
            for cmd in self.interface.commands:
                if cmd == toga.GROUP_BREAK:
                    menubar.setSubmenu(submenu, forItem=menuItem)
                    submenu = None
                elif cmd == toga.SECTION_BREAK:
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

                    # This line may appear redundant, but it triggers the logic
                    # to force the enabled status on the underlying widgets.
                    cmd.enabled = cmd.enabled
                    submenu.addItem(item)

            if submenu:
                menubar.setSubmenu(submenu, forItem=menuItem)

            # Set the menu for the app.
            self.native.mainMenu = menubar

    def main_loop(self):
        # Stimulate the build of the app
        self.create()

        self.loop.run_forever(lifecycle=CocoaLifecycle(self.native))

    def exit(self):
        self.native.terminate(None)

    def set_on_exit(self, value):
        pass

    def current_window(self):
        return self.native.keyWindow

    def enter_full_screen(self, windows):
        # If we're already in full screen mode, exit so that
        # we can re-assign windows to screens.
        if self.interface.is_full_screen:
            self.interface.exit_full_screen()

        opts = NSMutableDictionary.alloc().init()
        opts.setObject(NSNumber.numberWithBool(True), forKey="NSFullScreenModeAllScreens")

        for window, screen in zip(windows, NSScreen.screens):
            window.content._impl.native.enterFullScreenMode(screen, withOptions=opts)

    def exit_full_screen(self, windows):
        opts = NSMutableDictionary.alloc().init()
        opts.setObject(NSNumber.numberWithBool(True), forKey="NSFullScreenModeAllScreens")

        for window in windows:
            window.content._impl.native.exitFullScreenModeWithOptions(opts)

    def show_cursor(self):
        if not self._cursor_visible:
            NSCursor.unhide()

        self._cursor_visible = True

    def hide_cursor(self):
        if self._cursor_visible:
            NSCursor.hide()

        self._cursor_visible = False


class DocumentApp(App):
    def _create_app_commands(self):
        self.interface.commands.add(
            toga.Command(
                lambda _: self.select_file(),
                label='Open...',
                shortcut='o',
                group=toga.Group.FILE,
                section=0
            ),
        )

    def select_file(self, **kwargs):
        # FIXME This should be all we need; but for some reason, application types
        # aren't being registered correctly..
        # NSDocumentController.sharedDocumentController().openDocument_(None)

        # ...so we do this instead.
        panel = NSOpenPanel.openPanel()
        # print("Open documents of type", NSDocumentController.sharedDocumentController().defaultType)

        fileTypes = NSMutableArray.alloc().init()
        for filetype in self.interface.document_types:
            fileTypes.addObject(filetype)

        NSDocumentController.sharedDocumentController.runModalOpenPanel(panel, forTypes=fileTypes)

        # print("Untitled File opened?", panel.URLs)
        self.appDelegate.application_openFiles_(None, panel.URLs)

    def open_document(self, fileURL):
        """Open a new document in this app.

        Args:
            fileURL (str): The URL/path to the file to add as a document.
        """
        # Convert a cocoa fileURL to a file path.
        fileURL = fileURL.rstrip('/')
        path = unquote(urlparse(fileURL).path)
        extension = os.path.splitext(path)[1][1:]

        # Create the document instance
        DocType = self.interface.document_types[extension]
        document = DocType(path, app=self.interface)
        self.interface._documents.append(document)

        # Show the document.
        document.show()
