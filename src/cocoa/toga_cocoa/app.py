import asyncio
import inspect
import os
import sys
from urllib.parse import unquote, urlparse

from rubicon.objc.eventloop import CocoaLifecycle, EventLoopPolicy

import toga
from toga.handlers import wrapped_handler, NativeHandler

from .keys import cocoa_key
from .libs import (
    SEL,
    NSMenu,
    NSMenuItem,
    NSURL,
    NSAboutPanelOptionApplicationIcon,
    NSAboutPanelOptionApplicationName,
    NSAboutPanelOptionApplicationVersion,
    NSApplication,
    NSApplicationActivationPolicyRegular,
    NSBundle,
    NSCursor,
    NSDocumentController,
    NSMutableArray,
    NSMutableDictionary,
    NSNumber,
    NSObject,
    NSOpenPanel,
    NSScreen,
    NSString,
    objc_method
)
from .window import Window


class MainWindow(Window):
    def cocoa_windowShouldClose(self):
        # Main Window close is a proxy for "Exit app".
        # Defer all handling to the app's exit method.
        # As a result of calling that method, the app will either
        # exit, or the user will cancel the exit; in which case
        # the main window shouldn't close, either.
        self.interface.app.exit()
        return False


class AppDelegate(NSObject):
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
            # If you start your Toga application as `python myapp.py` or
            # `myapp.py`, the name of the Python script is included as a
            # filename to be processed. Inspect the stack, and ignore any
            # "document" that matches the file doing the executing
            if filename == inspect.stack(-1)[-1].filename:
                continue

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

    @objc_method
    def validateMenuItem_(self, sender) -> bool:
        cmd = self.interface._impl._menu_items[sender]
        return cmd.enabled


class App:
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self._cursor_visible = True

        policy = EventLoopPolicy()
        asyncio.set_event_loop_policy(policy)
        self.loop = policy.get_event_loop()

    def create(self):
        self.native = NSApplication.sharedApplication
        self.native.setActivationPolicy(NSApplicationActivationPolicyRegular)

        icon = self.interface.icon.bind(self.interface.factory)
        self.native.setApplicationIconImage_(icon.native)

        self.resource_path = os.path.dirname(os.path.dirname(NSBundle.mainBundle.bundlePath))

        self.appDelegate = AppDelegate.alloc().init()
        self.appDelegate.impl = self
        self.appDelegate.interface = self.interface
        self.appDelegate.native = self.native
        self.native.setDelegate_(self.appDelegate)

        formal_name = self.interface.formal_name

        self.interface.commands.add(

            # ---- App menu -----------------------------------
            toga.Command(
                lambda _: self.interface.about(),
                'About ' + formal_name,
                group=toga.Group.APP
            ),
            toga.Command(
                None,
                'Preferences',
                shortcut=toga.Key.MOD_1 + ',',
                group=toga.Group.APP,
                section=20,
            ),
            toga.Command(
                NativeHandler(SEL('hide:')),
                'Hide ' + formal_name,
                shortcut=toga.Key.MOD_1 + 'h',
                group=toga.Group.APP,
                order=0,
                section=sys.maxsize - 1,
            ),
            toga.Command(
                NativeHandler(SEL('hideOtherApplications:')),
                'Hide Others',
                shortcut=toga.Key.MOD_1 + toga.Key.MOD_2 + 'h',
                group=toga.Group.APP,
                order=1,
                section=sys.maxsize - 1,
            ),
            toga.Command(
                NativeHandler(SEL('unhideAllApplications:')),
                'Show All',
                group=toga.Group.APP,
                order=2,
                section=sys.maxsize - 1,
            ),
            # Quit should always be the last item, in a section on its own
            toga.Command(
                lambda _: self.interface.exit(),
                'Quit ' + formal_name,
                shortcut=toga.Key.MOD_1 + 'q',
                group=toga.Group.APP,
                section=sys.maxsize
            ),

            # ---- Edit menu ----------------------------------
            toga.Command(
                NativeHandler(SEL('undo:')),
                'Undo',
                shortcut=toga.Key.MOD_1 + 'z',
                group=toga.Group.EDIT,
                order=10,
            ),
            toga.Command(
                NativeHandler(SEL('redo:')),
                'Redo',
                shortcut=toga.Key.SHIFT + toga.Key.MOD_1 + 'z',
                group=toga.Group.EDIT,
                order=20,
            ),

            toga.Command(
                NativeHandler(SEL('cut:')),
                'Cut',
                shortcut=toga.Key.MOD_1 + 'x',
                group=toga.Group.EDIT,
                section=10,
                order=10,
            ),
            toga.Command(
                NativeHandler(SEL('copy:')),
                'Copy',
                shortcut=toga.Key.MOD_1 + 'c',
                group=toga.Group.EDIT,
                section=10,
                order=20,
            ),
            toga.Command(
                NativeHandler(SEL('paste:')),
                'Paste',
                shortcut=toga.Key.MOD_1 + 'v',
                group=toga.Group.EDIT,
                section=10,
                order=30,
            ),
            toga.Command(
                NativeHandler(SEL('pasteAsPlainText:')),
                'Paste and Match Style',
                shortcut=toga.Key.MOD_2 + toga.Key.SHIFT + toga.Key.MOD_1 + 'v',
                group=toga.Group.EDIT,
                section=10,
                order=40,
            ),
            toga.Command(
                NativeHandler(SEL('delete:')),
                'Delete',
                group=toga.Group.EDIT,
                section=10,
                order=50,
            ),
            toga.Command(
                NativeHandler(SEL('selectAll:')),
                'Select All',
                shortcut=toga.Key.MOD_1 + 'a',
                group=toga.Group.EDIT,
                section=10,
                order=60,
            ),

            # ---- Help menu ----------------------------------
            toga.Command(
                lambda _: self.interface.visit_homepage(),
                'Visit homepage',
                enabled=self.interface.home_page is not None,
                group=toga.Group.HELP
            )
        )
        self._create_app_commands()

        # Call user code to populate the main window
        self.interface.startup()

        # Create the lookup table of menu items,
        # then force the creation of the menus.
        self.create_menus()

    def _create_app_commands(self):
        # No extra commands
        pass

    def create_menus(self):
        # Recreate the menu
        self._menu_items = {}
        self._menu_groups = {}
        menubar = NSMenu.alloc().initWithTitle('MainMenu')
        submenu = None
        for cmd in self.interface.commands:
            if cmd == toga.GROUP_BREAK:
                submenu = None
            elif cmd == toga.SECTION_BREAK:
                submenu.addItem_(NSMenuItem.separatorItem())
            else:
                submenu = self._submenu(cmd.group, menubar)

                if cmd.shortcut:
                    key, modifier = cocoa_key(cmd.shortcut)
                else:
                    key = ''
                    modifier = None

                # Native handlers can be invoked directly as menu actions.
                # Standard wrapped menu items have a `_raw` attribute,
                # and are invoked using the selectMenuItem:
                if hasattr(cmd.action, '_raw'):
                    action = SEL('selectMenuItem:')
                else:
                    action = cmd.action

                item = NSMenuItem.alloc().initWithTitle(
                    cmd.label,
                    action=action,
                    keyEquivalent=key,
                )
                if modifier is not None:
                    item.keyEquivalentModifierMask = modifier

                self._menu_items[item] = cmd
                submenu.addItem(item)

        # Set the menu for the app.
        self.native.mainMenu = menubar

    def _submenu(self, group, menubar):
        """
        Obtain the submenu representing the command group.

        This will create the submenu if it doesn't exist. It will call itself
        recursively to build the full path to menus inside submenus, returning
        the "leaf" node in the submenu path. Once created, it caches the menu
        that has been created for future lookup.
        """
        try:
            return self._menu_groups[group]
        except KeyError:
            if group is None:
                submenu = menubar
            else:
                parent_menu = self._submenu(group.parent, menubar)

                menu_item = parent_menu.addItemWithTitle(
                    group.label, action=None, keyEquivalent=''
                )
                submenu = NSMenu.alloc().initWithTitle(group.label)
                parent_menu.setSubmenu(submenu, forItem=menu_item)

            # Install the item in the group cache.
            self._menu_groups[group] = submenu
            return submenu

    def main_loop(self):
        # Stimulate the build of the app
        self.create()

        self.loop.run_forever(lifecycle=CocoaLifecycle(self.native))

    def set_main_window(self, window):
        pass

    def show_about_dialog(self):
        options = NSMutableDictionary.alloc().init()

        options[NSAboutPanelOptionApplicationIcon] = self.interface.icon.bind(self.interface.factory).native

        if self.interface.name is not None:
            options[NSAboutPanelOptionApplicationName] = self.interface.name

        if self.interface.version is not None:
            options[NSAboutPanelOptionApplicationVersion] = self.interface.version

        # The build number
        # if self.interface.version is not None:
        #     options[NSAboutPanelOptionVersion] = "the build"

        if self.interface.author is not None:
            options["Copyright"] = "Copyright © {author}".format(
                author=self.interface.author
            )

        self.native.orderFrontStandardAboutPanelWithOptions(options)

    def exit(self):
        self.native.terminate(self.native)

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
            # Going full screen causes the window content to be re-homed
            # in a NSFullScreenWindow; teach the new parent window
            # about it's Toga representations.
            window.content._impl.native.window._impl = window._impl
            window.content._impl.native.window.interface = window

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

    def add_background_task(self, handler):
        self.loop.call_soon(wrapped_handler(self, handler), self)

    def open_document(self, fileURL):
        """No-op when the app is not a ``DocumentApp``."""

    def select_file(self, **kwargs):
        """No-op when the app is not a ``DocumentApp``."""


class DocumentApp(App):
    def _create_app_commands(self):
        self.interface.commands.add(
            toga.Command(
                lambda _: self.select_file(),
                label='Open...',
                shortcut=toga.Key.MOD_1 + 'o',
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
