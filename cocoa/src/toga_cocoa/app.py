from __future__ import annotations

import asyncio
import inspect
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

from rubicon.objc import (
    SEL,
    NSObject,
    objc_method,
    objc_property,
)
from rubicon.objc.eventloop import CocoaLifecycle, EventLoopPolicy

import toga
from toga.app import overridden
from toga.command import Separator
from toga.handlers import DynamicHandler, NativeHandler

from .keys import cocoa_key
from .libs import (
    NSURL,
    NSAboutPanelOptionApplicationIcon,
    NSAboutPanelOptionApplicationName,
    NSAboutPanelOptionApplicationVersion,
    NSAboutPanelOptionVersion,
    NSApplication,
    NSApplicationActivationPolicyAccessory,
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
    NSOpenPanel,
    NSScreen,
    NSString,
)
from .screens import Screen as ScreenImpl


class AppDelegate(NSObject):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def applicationDidFinishLaunching_(self, notification):
        self.native.activateIgnoringOtherApps(True)

    @objc_method
    def applicationSupportsSecureRestorableState_(self, app) -> bool:
        return True

    @objc_method
    def applicationOpenUntitledFile_(self, sender) -> bool:
        if self.interface.document_types and self.interface.main_window is None:
            # We can't use the normal "file open" logic here, because there's no
            # current window to hang the dialog off.
            panel = NSOpenPanel.openPanel()
            fileTypes = NSMutableArray.alloc().init()
            for filetype in self.interface.document_types:
                fileTypes.addObject(filetype)

            NSDocumentController.sharedDocumentController.runModalOpenPanel(
                panel, forTypes=fileTypes
            )

            self.application(None, openFiles=panel.URLs)

            return True
        return False

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

            # Convert a Cocoa fileURL to a Python file path.
            path = Path(unquote(urlparse(str(fileURL.absoluteString)).path))

            # Try to open the file.
            try:
                self.interface.open(path)
            except ValueError as e:
                print(e)
            except FileNotFoundError:
                print("Document {filename} not found")

    @objc_method
    def selectMenuItem_(self, sender) -> None:
        cmd = self.impl._menu_items[sender]
        cmd.action()

    @objc_method
    def validateMenuItem_(self, sender) -> bool:
        cmd = self.impl._menu_items[sender]
        return cmd.enabled


class App:
    # macOS apps persist when there are no windows open
    CLOSE_ON_LAST_WINDOW = False

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self._cursor_visible = True

        asyncio.set_event_loop_policy(EventLoopPolicy())
        self.loop = asyncio.new_event_loop()

        self.native = NSApplication.sharedApplication
        self.native.setApplicationIconImage(self.interface.icon._impl.native)

        self.resource_path = Path(NSBundle.mainBundle.bundlePath).parent.parent

        self.appDelegate = AppDelegate.alloc().init()
        self.appDelegate.impl = self
        self.appDelegate.interface = self.interface
        self.appDelegate.native = self.native
        self.native.delegate = self.appDelegate

        # Call user code to populate the main window
        self.interface._startup()

    ######################################################################
    # Commands and menus
    ######################################################################

    def _menu_close_all_windows(self, command, **kwargs):
        # Convert to a list to so that we're not altering a set while iterating
        for window in list(self.interface.windows):
            window._impl.native.performClose(None)

    def _menu_close_window(self, command, **kwargs):
        if self.interface.current_window:
            self.interface.current_window._impl.native.performClose(None)

    def _menu_minimize(self, command, **kwargs):
        if self.interface.current_window:
            self.interface.current_window._impl.native.miniaturize(None)

    def create_app_commands(self):
        # All macOS apps have some basic commands.
        self.interface.commands.add(
            # ---- App menu -----------------------------------
            toga.Command(
                self.interface._menu_about,
                f"About {self.interface.formal_name}",
                group=toga.Group.APP,
            ),
            # Quit should always be the last item, in a section on its own
            toga.Command(
                self.interface._menu_exit,
                f"Quit {self.interface.formal_name}",
                shortcut=toga.Key.MOD_1 + "q",
                group=toga.Group.APP,
                section=sys.maxsize,
            ),
            # ---- Help menu ----------------------------------
            toga.Command(
                self.interface._menu_visit_homepage,
                "Visit homepage",
                enabled=self.interface.home_page is not None,
                group=toga.Group.HELP,
            ),
        )

        # Register the Apple HIG commands for any app with a MainWindow,
        # or any Document-based app (i.e., app with no main window).
        if (
            isinstance(self.interface.main_window, toga.MainWindow)
            or self.interface.main_window is None
        ):
            self.interface.commands.add(
                toga.Command(
                    self.interface._menu_preferences,
                    "Settings\u2026",
                    shortcut=toga.Key.MOD_1 + ",",
                    group=toga.Group.APP,
                    section=20,
                    # For now, only enable preferences if the user defines an implementation
                    enabled=overridden(self.interface.preferences),
                ),
                toga.Command(
                    NativeHandler(SEL("hide:")),
                    "Hide " + self.interface.formal_name,
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
                # ---- File menu ----------------------------------
                # This is a bit of an oddity. Apple HIG apps that don't have tabs as
                # part of their interface (so, Preview and Numbers, but not Safari)
                # have a "Close" item that becomes "Close All" when you press Option
                # (MOD_2). That behavior isn't something we're currently set up to
                # implement, so we live with a separate menu item for now.
                toga.Command(
                    DynamicHandler(
                        self._menu_close_window,
                        enabled=lambda: self.interface.current_window is not None,
                    ),
                    "Close",
                    shortcut=toga.Key.MOD_1 + "w",
                    group=toga.Group.FILE,
                    order=1,
                    section=50,
                ),
                toga.Command(
                    DynamicHandler(
                        self._menu_close_all_windows,
                        enabled=lambda: self.interface.current_window is not None,
                    ),
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
                    enabled=lambda: self.interface.current_window is not None,
                ),
            )

        # Add a "New" menu item for each unique registered document type.
        if self.interface.document_types:
            for i, document_class in enumerate(
                sorted(set(self.interface.document_types.values()))
            ):
                self.interface.commands.add(
                    toga.Command(
                        self.interface._menu_new_document(document_class),
                        text=f"New {document_class.document_type}",
                        shortcut=(toga.Key.MOD_1 + "n" if i == 0 else None),
                        group=toga.Group.FILE,
                        section=0,
                    ),
                )

        # If there's a user-provided open() implementation, or there are registered
        # document types, add an Open menu item.
        if overridden(self.interface.open) or self.interface.document_types:
            self.interface.commands.add(
                toga.Command(
                    self.interface._menu_open_file,
                    text="Open\u2026",
                    shortcut=toga.Key.MOD_1 + "o",
                    group=toga.Group.FILE,
                    section=10,
                ),
            )

        # If there is a user-provided save() implementation, or there are registered
        # document types, add a Save menu item.
        if overridden(self.interface.save) or self.interface.document_types:
            self.interface.commands.add(
                toga.Command(
                    DynamicHandler(
                        self.interface._menu_save,
                        enabled=self.interface.can_save,
                    ),
                    text="Save",
                    shortcut=toga.Key.MOD_1 + "s",
                    group=toga.Group.FILE,
                    section=20,
                    order=10,
                ),
            )

        # If there is a user-provided save_as() implementation, or there are registered
        # document types, add a Save As menu item.
        if overridden(self.interface.save_as) or self.interface.document_types:
            self.interface.commands.add(
                toga.Command(
                    DynamicHandler(
                        self.interface._menu_save_as,
                        enabled=self.interface.can_save,
                    ),
                    text="Save As\u2026",
                    shortcut=toga.Key.MOD_1 + "S",
                    group=toga.Group.FILE,
                    section=20,
                    order=11,
                ),
            )

        # If there is a user-provided save_all() implementation, or there are registered
        # document types, add a Save All menu item.
        if overridden(self.interface.save_all) or self.interface.document_types:
            self.interface.commands.add(
                toga.Command(
                    DynamicHandler(
                        self.interface._menu_save_all,
                        enabled=self.interface.can_save_all,
                    ),
                    text="Save All",
                    shortcut=toga.Key.MOD_1 + toga.Key.MOD_2 + "s",
                    group=toga.Group.FILE,
                    section=20,
                    order=12,
                ),
            )

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

                submenu = NSMenu.alloc().initWithTitle(group.text)

                menu_item = parent_menu.addItemWithTitle(
                    group.text, action=None, keyEquivalent=""
                )
                parent_menu.setSubmenu(submenu, forItem=menu_item)

            # Install the item in the group cache.
            self._menu_groups[group] = submenu
            return submenu

    def create_menus(self):
        # Recreate the menu bar for the app.
        # Remove any native references to the existing menu
        for menu_item, cmd in self._menu_items.items():
            cmd._impl.native.remove(menu_item)

        # Create a clean menubar instance.
        menubar = NSMenu.alloc().initWithTitle("MainMenu")
        self._menu_groups = {}
        self._menu_items = {}

        submenu = None
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

    ######################################################################
    # App lifecycle
    ######################################################################

    # We can't call this under test conditions, because it would kill the test harness
    def exit(self):  # pragma: no cover
        self.loop.stop()

    def finalize(self):
        # Set up the lookup tables for menu items
        self._menu_groups = {}
        self._menu_items = {}

        # Add any platform-specific app commands. This is done during finalization to
        # ensure that the main_window has been assigned, which informs which app
        # commands are needed.
        self.create_app_commands()
        self.create_menus()

        # Cocoa *doesn't* invoke _create_initial_windows(); the NSApplication
        # interface handles arguments as part of the persistent app interface.

    def main_loop(self):
        self.loop.run_forever(lifecycle=CocoaLifecycle(self.native))

    def set_main_window(self, window):
        # If it's a background app, don't display the app icon.
        if window == toga.App.BACKGROUND:
            self.native.setActivationPolicy(NSApplicationActivationPolicyAccessory)
        else:
            self.native.setActivationPolicy(NSApplicationActivationPolicyRegular)

    ######################################################################
    # App resources
    ######################################################################

    def get_screens(self):
        return [ScreenImpl(native=screen) for screen in NSScreen.screens]

    ######################################################################
    # App capabilities
    ######################################################################

    def beep(self):
        NSBeep()

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

    ######################################################################
    # Cursor control
    ######################################################################

    def hide_cursor(self):
        if self._cursor_visible:
            NSCursor.hide()

        self._cursor_visible = False

    def show_cursor(self):
        if not self._cursor_visible:
            NSCursor.unhide()

        self._cursor_visible = True

    ######################################################################
    # Window control
    ######################################################################

    def get_current_window(self):
        window = self.native.keyWindow
        # When a menu is activated, the current window sometimes reports as being of
        # type NSMenuWindowManagerWindow. This is an internal type; we ignore it, and
        # assume there's no current window. Marked nocover because it's impossible to
        # replicate in test conditions.
        if not hasattr(window, "interface"):  # pragma: no cover
            return None
        return window

    def set_current_window(self, window):
        window._impl.native.makeKeyAndOrderFront(window._impl.native)

    ######################################################################
    # Full screen control
    ######################################################################

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
