import asyncio
import inspect
import os
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

from rubicon.objc.eventloop import CocoaLifecycle, EventLoopPolicy

import toga
from toga.command import Separator
from toga.handlers import NativeHandler

from .keys import cocoa_key
from .libs import (
    NSURL,
    SEL,
    NSAboutPanelOptionApplicationIcon,
    NSAboutPanelOptionApplicationName,
    NSAboutPanelOptionApplicationVersion,
    NSAboutPanelOptionVersion,
    NSApplication,
    NSApplicationActivationPolicyRegular,
    NSBeep,
    NSBundle,
    NSCursor,
    NSDocumentController,
    NSMenu,
    NSMenuItem,
    NSMutableArray,
    NSMutableDictionary,
    NSNumber,
    NSObject,
    NSOpenPanel,
    NSScreen,
    NSString,
    objc_method,
    objc_property,
)
from .window import Window


class MainWindow(Window):
    def cocoa_windowShouldClose(self):
        # Main Window close is a proxy for "Exit app".
        # Defer all handling to the app's on_exit handler.
        # As a result of calling that method, the app will either
        # exit, or the user will cancel the exit; in which case
        # the main window shouldn't close, either.
        self.interface.app.on_exit()
        return False


class AppDelegate(NSObject):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def applicationDidFinishLaunching_(self, notification):
        self.native.activateIgnoringOtherApps(True)

    @objc_method
    def applicationOpenUntitledFile_(self, sender) -> bool:  # pragma: no cover
        self.impl.select_file()
        return True

    @objc_method
    def addDocument_(self, document) -> None:  # pragma: no cover
        # print("Add Document", document)
        super().addDocument_(document)

    @objc_method
    def applicationShouldOpenUntitledFile_(self, sender) -> bool:  # pragma: no cover
        return True

    @objc_method
    def application_openFiles_(self, app, filenames) -> None:  # pragma: no cover
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
        cmd = self.impl._menu_items[sender]
        cmd.action()

    @objc_method
    def validateMenuItem_(self, sender) -> bool:
        cmd = self.impl._menu_items[sender]
        return cmd.enabled


class App:
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self._cursor_visible = True

        asyncio.set_event_loop_policy(EventLoopPolicy())
        self.loop = asyncio.new_event_loop()

        # Stimulate the build of the app
        self.create()

    def create(self):
        self.native = NSApplication.sharedApplication
        self.native.setActivationPolicy(NSApplicationActivationPolicyRegular)

        self.native.setApplicationIconImage_(self.interface.icon._impl.native)

        self.resource_path = os.path.dirname(
            os.path.dirname(NSBundle.mainBundle.bundlePath)
        )

        self.appDelegate = AppDelegate.alloc().init()
        self.appDelegate.impl = self
        self.appDelegate.interface = self.interface
        self.appDelegate.native = self.native
        self.native.setDelegate_(self.appDelegate)

        self._create_app_commands()

        # Call user code to populate the main window
        self.interface._startup()

        # Create the lookup table of menu items,
        # then force the creation of the menus.
        self._menu_groups = {}
        self._menu_items = {}
        self.create_menus()

    def _create_app_commands(self):
        formal_name = self.interface.formal_name
        self.interface.commands.add(
            # ---- App menu -----------------------------------
            toga.Command(
                self._menu_about,
                "About " + formal_name,
                group=toga.Group.APP,
            ),
            toga.Command(
                None,
                "Settings\u2026",
                shortcut=toga.Key.MOD_1 + ",",
                group=toga.Group.APP,
                section=20,
            ),
            toga.Command(
                NativeHandler(SEL("hide:")),
                "Hide " + formal_name,
                shortcut=toga.Key.MOD_1 + "h",
                group=toga.Group.APP,
                order=0,
                section=sys.maxsize - 1,
            ),
            toga.Command(
                NativeHandler(SEL("hideOtherApplications:")),
                "Hide Others",
                shortcut=toga.Key.MOD_1 + toga.Key.MOD_2 + "h",
                group=toga.Group.APP,
                order=1,
                section=sys.maxsize - 1,
            ),
            toga.Command(
                NativeHandler(SEL("unhideAllApplications:")),
                "Show All",
                group=toga.Group.APP,
                order=2,
                section=sys.maxsize - 1,
            ),
            # Quit should always be the last item, in a section on its own
            toga.Command(
                self._menu_quit,
                "Quit " + formal_name,
                shortcut=toga.Key.MOD_1 + "q",
                group=toga.Group.APP,
                section=sys.maxsize,
            ),
            # ---- File menu ----------------------------------
            # This is a bit of an oddity. Apple HIG apps that don't have tabs as
            # part of their interface (so, Preview and Numbers, but not Safari)
            # have a "Close" item that becomes "Close All" when you press Option
            # (MOD_2). That behavior isn't something we're currently set up to
            # implement, so we live with a separate menu item for now.
            toga.Command(
                self._menu_close_window,
                "Close",
                shortcut=toga.Key.MOD_1 + "w",
                group=toga.Group.FILE,
                order=1,
                section=50,
            ),
            toga.Command(
                self._menu_close_all_windows,
                "Close All",
                shortcut=toga.Key.MOD_2 + toga.Key.MOD_1 + "w",
                group=toga.Group.FILE,
                order=2,
                section=50,
            ),
            # ---- Edit menu ----------------------------------
            toga.Command(
                NativeHandler(SEL("undo:")),
                "Undo",
                shortcut=toga.Key.MOD_1 + "z",
                group=toga.Group.EDIT,
                order=10,
            ),
            toga.Command(
                NativeHandler(SEL("redo:")),
                "Redo",
                shortcut=toga.Key.SHIFT + toga.Key.MOD_1 + "z",
                group=toga.Group.EDIT,
                order=20,
            ),
            toga.Command(
                NativeHandler(SEL("cut:")),
                "Cut",
                shortcut=toga.Key.MOD_1 + "x",
                group=toga.Group.EDIT,
                section=10,
                order=10,
            ),
            toga.Command(
                NativeHandler(SEL("copy:")),
                "Copy",
                shortcut=toga.Key.MOD_1 + "c",
                group=toga.Group.EDIT,
                section=10,
                order=20,
            ),
            toga.Command(
                NativeHandler(SEL("paste:")),
                "Paste",
                shortcut=toga.Key.MOD_1 + "v",
                group=toga.Group.EDIT,
                section=10,
                order=30,
            ),
            toga.Command(
                NativeHandler(SEL("pasteAsPlainText:")),
                "Paste and Match Style",
                shortcut=toga.Key.MOD_2 + toga.Key.SHIFT + toga.Key.MOD_1 + "v",
                group=toga.Group.EDIT,
                section=10,
                order=40,
            ),
            toga.Command(
                NativeHandler(SEL("delete:")),
                "Delete",
                group=toga.Group.EDIT,
                section=10,
                order=50,
            ),
            toga.Command(
                NativeHandler(SEL("selectAll:")),
                "Select All",
                shortcut=toga.Key.MOD_1 + "a",
                group=toga.Group.EDIT,
                section=10,
                order=60,
            ),
            # ---- Window menu ----------------------------------
            toga.Command(
                self._menu_minimize,
                "Minimize",
                shortcut=toga.Key.MOD_1 + "m",
                group=toga.Group.WINDOW,
            ),
            # ---- Help menu ----------------------------------
            toga.Command(
                self._menu_visit_homepage,
                "Visit homepage",
                enabled=self.interface.home_page is not None,
                group=toga.Group.HELP,
            ),
        )

    def _menu_about(self, command, **kwargs):
        self.interface.about()

    def _menu_quit(self, command, **kwargs):
        self.interface.on_exit()

    def _menu_close_window(self, command, **kwargs):
        if self.interface.current_window:
            self.interface.current_window._impl.native.performClose(None)

    def _menu_close_all_windows(self, command, **kwargs):
        # Convert to a list to so that we're not altering a set while iterating
        for window in list(self.interface.windows):
            window._impl.native.performClose(None)

    def _menu_minimize(self, command, **kwargs):
        if self.interface.current_window:
            self.interface.current_window._impl.native.miniaturize(None)

    def _menu_visit_homepage(self, command, **kwargs):
        self.interface.visit_homepage()

    def create_menus(self):
        # Recreate the menu.
        # Remove any native references to the existing menu
        for menu_item, cmd in self._menu_items.items():
            cmd._impl.native.remove(menu_item)

        # Create a clean menubar instance.
        menubar = NSMenu.alloc().initWithTitle("MainMenu")
        submenu = None
        self._menu_groups = {}
        self._menu_items = {}

        for cmd in self.interface.commands:
            submenu = self._submenu(cmd.group, menubar)
            if isinstance(cmd, Separator):
                submenu.addItem(NSMenuItem.separatorItem())
            else:
                if cmd.shortcut:
                    key, modifier = cocoa_key(cmd.shortcut)
                else:
                    key = ""
                    modifier = None

                # Native handlers can be invoked directly as menu actions.
                # Standard wrapped menu items have a `_raw` attribute,
                # and are invoked using the selectMenuItem:
                if hasattr(cmd.action, "_raw"):
                    action = SEL("selectMenuItem:")
                else:
                    action = cmd.action

                item = NSMenuItem.alloc().initWithTitle(
                    cmd.text,
                    action=action,
                    keyEquivalent=key,
                )

                if modifier is not None:
                    item.keyEquivalentModifierMask = modifier

                # Explicit set the initial enabled/disabled state on the menu item
                item.setEnabled(cmd.enabled)

                # Associated the MenuItem with the command, so that future
                # changes to enabled etc are reflected.
                cmd._impl.native.add(item)

                self._menu_items[item] = cmd
                submenu.addItem(item)

        # Set the menu for the app.
        self.native.mainMenu = menubar

    def _submenu(self, group, menubar):
        """Obtain the submenu representing the command group.

        This will create the submenu if it doesn't exist. It will call itself
        recursively to build the full path to menus inside submenus, returning the
        "leaf" node in the submenu path. Once created, it caches the menu that has been
        created for future lookup.
        """
        try:
            return self._menu_groups[group]
        except KeyError:
            if group is None:
                submenu = menubar
            else:
                parent_menu = self._submenu(group.parent, menubar)

                menu_item = parent_menu.addItemWithTitle(
                    group.text, action=None, keyEquivalent=""
                )
                submenu = NSMenu.alloc().initWithTitle(group.text)
                parent_menu.setSubmenu(submenu, forItem=menu_item)

            # Install the item in the group cache.
            self._menu_groups[group] = submenu
            return submenu

    def main_loop(self):
        self.loop.run_forever(lifecycle=CocoaLifecycle(self.native))

    def set_main_window(self, window):
        pass

    def show_about_dialog(self):
        options = NSMutableDictionary.alloc().init()

        options[NSAboutPanelOptionApplicationIcon] = self.interface.icon._impl.native
        options[NSAboutPanelOptionApplicationName] = self.interface.formal_name

        if self.interface.version is None:
            options[NSAboutPanelOptionApplicationVersion] = "0.0"
        else:
            options[NSAboutPanelOptionApplicationVersion] = self.interface.version

        # The build number
        options[NSAboutPanelOptionVersion] = "1"

        if self.interface.author is None:
            options["Copyright"] = ""
        else:
            options["Copyright"] = f"Copyright © {self.interface.author}"

        self.native.orderFrontStandardAboutPanelWithOptions(options)

    def beep(self):
        NSBeep()

    # We can't call this under test conditions, because it would kill the test harness
    def exit(self):  # pragma: no cover
        self.loop.stop()

    def get_current_window(self):
        return self.native.keyWindow

    def set_current_window(self, window):
        window._impl.native.makeKeyAndOrderFront(window._impl.native)

    def enter_full_screen(self, windows):
        opts = NSMutableDictionary.alloc().init()
        opts.setObject(
            NSNumber.numberWithBool(True), forKey="NSFullScreenModeAllScreens"
        )

        for window, screen in zip(windows, NSScreen.screens):
            window.content._impl.native.enterFullScreenMode(screen, withOptions=opts)
            # Going full screen causes the window content to be re-homed
            # in a NSFullScreenWindow; teach the new parent window
            # about its Toga representations.
            window.content._impl.native.window._impl = window._impl
            window.content._impl.native.window.interface = window
            window.content.refresh()

    def exit_full_screen(self, windows):
        opts = NSMutableDictionary.alloc().init()
        opts.setObject(
            NSNumber.numberWithBool(True), forKey="NSFullScreenModeAllScreens"
        )

        for window in windows:
            window.content._impl.native.exitFullScreenModeWithOptions(opts)
            window.content.refresh()

    def show_cursor(self):
        if not self._cursor_visible:
            NSCursor.unhide()

        self._cursor_visible = True

    def hide_cursor(self):
        if self._cursor_visible:
            NSCursor.hide()

        self._cursor_visible = False

    def open_document(self, fileURL):
        """No-op when the app is not a ``DocumentApp``."""

    def select_file(self, **kwargs):
        """No-op when the app is not a ``DocumentApp``."""


class DocumentApp(App):  # pragma: no cover
    def _create_app_commands(self):
        super()._create_app_commands()
        self.interface.commands.add(
            toga.Command(
                self._menu_open_file,
                text="Open\u2026",
                shortcut=toga.Key.MOD_1 + "o",
                group=toga.Group.FILE,
                section=0,
            ),
        )

    def _menu_open_file(self, app, **kwargs):
        self.select_file()

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

        NSDocumentController.sharedDocumentController.runModalOpenPanel(
            panel, forTypes=fileTypes
        )

        # print("Untitled File opened?", panel.URLs)
        self.appDelegate.application_openFiles_(None, panel.URLs)

    def open_document(self, fileURL):
        # Convert a cocoa fileURL to a file path.
        fileURL = fileURL.rstrip("/")
        path = Path(unquote(urlparse(fileURL).path))

        # Create and show the document instance
        self.interface._open(path)
