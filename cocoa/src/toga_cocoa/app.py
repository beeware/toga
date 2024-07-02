import asyncio
import sys
from pathlib import Path

from rubicon.objc import (
    SEL,
    NSMutableDictionary,
    NSObject,
    objc_method,
    objc_property,
)
from rubicon.objc.eventloop import CocoaLifecycle, EventLoopPolicy

import toga
from toga.command import Command, Group, Separator
from toga.handlers import NativeHandler, overridden, simple_handler
from toga.keys import Key

from .keys import cocoa_key
from .libs import (
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
    NSMenu,
    NSMenuItem,
    NSNumber,
    NSScreen,
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
        asyncio.create_task(self.interface._open())
        return True

    @objc_method
    def applicationShouldOpenUntitledFile_(self, sender) -> bool:
        return bool(self.interface.document_types)

    @objc_method
    def application_openFiles_(self, app, filenames) -> None:
        for filename in filenames:
            self.interface._open_initial_document(str(filename))

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
    # macOS has handling for command line arguments tied to document handling;
    # this also allows documents to be opened by dragging an icon onto the app.
    HANDLES_COMMAND_LINE = True

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self._cursor_visible = True

        asyncio.set_event_loop_policy(EventLoopPolicy())
        self.loop = asyncio.new_event_loop()

        self.native = NSApplication.sharedApplication

        # The app icon been set *before* the app instance is created. However, we only
        # need to set the icon on the app if it has been explicitly defined; the default
        # icon is... the default. We can't test this branch in the testbed.
        if self.interface.icon._impl.path:
            self.set_icon(self.interface.icon)  # pragma: no cover

        self.resource_path = Path(NSBundle.mainBundle.bundlePath).parent.parent

        self.appDelegate = AppDelegate.alloc().init()
        self.appDelegate.impl = self
        self.appDelegate.interface = self.interface
        self.appDelegate.native = self.native
        self.native.setDelegate(self.appDelegate)

        # Create the lookup table for menu items
        self._menu_groups = {}
        self._menu_items = {}

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
        self.interface.commands.add(
            # ---- App menu -----------------------------------
            # About should be the first menu item
            Command(
                simple_handler(self.interface.about),
                f"About {self.interface.formal_name}",
                group=Group.APP,
                id=Command.ABOUT,
                section=-1,
            ),
            # App-level window management commands should be in the second last section.
            Command(
                NativeHandler(SEL("hide:")),
                f"Hide {self.interface.formal_name}",
                shortcut=toga.Key.MOD_1 + "h",
                group=Group.APP,
                order=0,
                section=sys.maxsize - 1,
            ),
            Command(
                NativeHandler(SEL("hideOtherApplications:")),
                "Hide Others",
                shortcut=toga.Key.MOD_1 + toga.Key.MOD_2 + "h",
                group=Group.APP,
                order=1,
                section=sys.maxsize - 1,
            ),
            Command(
                NativeHandler(SEL("unhideAllApplications:")),
                "Show All",
                group=Group.APP,
                order=2,
                section=sys.maxsize - 1,
            ),
            # Quit should always be the last item, in a section on its own. Invoke
            # `_request_exit` rather than `exit`, because we want to trigger the "OK to
            # exit?" logic.
            Command(
                simple_handler(self.interface._request_exit),
                f"Quit {self.interface.formal_name}",
                shortcut=toga.Key.MOD_1 + "q",
                group=Group.APP,
                section=sys.maxsize,
                id=Command.EXIT,
            ),
            # ---- File menu ----------------------------------
            # This is a bit of an oddity. Apple HIG apps that don't have tabs as
            # part of their interface (so, Preview and Numbers, but not Safari)
            # have a "Close" item that becomes "Close All" when you press Option
            # (MOD_2). That behavior isn't something we're currently set up to
            # implement, so we live with a separate menu item for now.
            Command(
                self._menu_close_window,
                "Close",
                shortcut=toga.Key.MOD_1 + "w",
                group=Group.FILE,
                order=1,
                section=50,
            ),
            Command(
                self._menu_close_all_windows,
                "Close All",
                shortcut=toga.Key.MOD_2 + toga.Key.MOD_1 + "w",
                group=Group.FILE,
                order=2,
                section=50,
            ),
            # ---- Edit menu ----------------------------------
            Command(
                NativeHandler(SEL("undo:")),
                "Undo",
                shortcut=toga.Key.MOD_1 + "z",
                group=Group.EDIT,
                order=10,
            ),
            Command(
                NativeHandler(SEL("redo:")),
                "Redo",
                shortcut=toga.Key.SHIFT + toga.Key.MOD_1 + "z",
                group=Group.EDIT,
                order=20,
            ),
            Command(
                NativeHandler(SEL("cut:")),
                "Cut",
                shortcut=toga.Key.MOD_1 + "x",
                group=Group.EDIT,
                section=10,
                order=10,
            ),
            Command(
                NativeHandler(SEL("copy:")),
                "Copy",
                shortcut=toga.Key.MOD_1 + "c",
                group=Group.EDIT,
                section=10,
                order=20,
            ),
            Command(
                NativeHandler(SEL("paste:")),
                "Paste",
                shortcut=toga.Key.MOD_1 + "v",
                group=Group.EDIT,
                section=10,
                order=30,
            ),
            Command(
                NativeHandler(SEL("pasteAsPlainText:")),
                "Paste and Match Style",
                shortcut=toga.Key.MOD_2 + toga.Key.SHIFT + toga.Key.MOD_1 + "v",
                group=Group.EDIT,
                section=10,
                order=40,
            ),
            Command(
                NativeHandler(SEL("delete:")),
                "Delete",
                group=Group.EDIT,
                section=10,
                order=50,
            ),
            Command(
                NativeHandler(SEL("selectAll:")),
                "Select All",
                shortcut=toga.Key.MOD_1 + "a",
                group=Group.EDIT,
                section=10,
                order=60,
            ),
            # ---- Window menu ----------------------------------
            Command(
                self._menu_minimize,
                "Minimize",
                shortcut=toga.Key.MOD_1 + "m",
                group=Group.WINDOW,
            ),
            # ---- Help menu ----------------------------------
            Command(
                simple_handler(self.interface.visit_homepage),
                "Visit homepage",
                enabled=self.interface.home_page is not None,
                group=Group.HELP,
                id=Command.VISIT_HOMEPAGE,
            ),
        )

        # If the user has overridden preferences, provide a menu item.
        # Testbed doesn't have a preferences menu, so this can't be covered
        if overridden(self.interface.preferences):
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.preferences),
                    "Settings\u2026",
                    shortcut=toga.Key.MOD_1 + ",",
                    group=Group.APP,
                    section=20,
                    id=Command.PREFERENCES,
                ),
            )  # pragma: no cover

        # If the app has document types, or has overridden new(), provide a menu item.
        # Testbed always has document types, so this must be covered.
        if self.interface.document_types:  # pragma: no branch
            known_document_classes = set()
            for i, (extension, document_class) in enumerate(
                self.interface.document_types.items()
            ):
                if document_class not in known_document_classes:
                    self.interface.commands.add(
                        Command(
                            simple_handler(self.interface.new, document_class),
                            text=f"New {document_class.document_type}",
                            shortcut=(Key.MOD_1 + "n" if i == 0 else None),
                            group=Group.FILE,
                            section=0,
                            order=i,
                            id=Command.NEW.format(extension),
                        ),
                    )
                    known_document_classes.add(document_class)
        elif overridden(self.interface.new):  # pragma: no cover
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.new),
                    text="New",
                    shortcut=Key.MOD_1 + "n",
                    group=Group.FILE,
                    section=0,
                    order=0,
                    id=Command.NEW.format(None),
                )
            )

        # If the app has document types, or has overridden open(), provide a menu item.
        # Testbed always has document types, so this must be covered.
        if self.interface.document_types or overridden(
            self.interface.open
        ):  # pragma: no branch
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface._open),
                    text="Open\u2026",
                    shortcut=Key.MOD_1 + "o",
                    group=Group.FILE,
                    section=0,
                    order=10,
                    id=Command.OPEN,
                )
            )

        # If the app has document types, or has overridden save(), provide a menu item.
        # Testbed always has document types, so this must be covered.
        if self.interface.document_types or overridden(
            self.interface.save
        ):  # pragma: no branch
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.save),
                    text="Save",
                    shortcut=Key.MOD_1 + "s",
                    group=Group.FILE,
                    section=30,
                    order=10,
                    id=Command.SAVE,
                )
            )

        # If the app has document types, or has overridden save_as(), provide a menu
        # item. Testbed always has document types, so this must be covered.
        if self.interface.document_types or overridden(
            self.interface.save_as
        ):  # pragma: no branch
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.save_as),
                    text="Save As\u2026",
                    shortcut=Key.MOD_1 + "S",
                    group=Group.FILE,
                    section=30,
                    order=11,
                    id=Command.SAVE_AS,
                )
            )

        # If the app has document types, or has overridden save_all(), provide a menu
        # item. Testbed always has document types, so this must be covered.
        if self.interface.document_types or overridden(
            self.interface.save_all
        ):  # pragma: no branch
            self.interface.commands.add(
                Command(
                    simple_handler(self.interface.save_all),
                    text="Save All",
                    shortcut=Key.MOD_1 + Key.MOD_2 + "s",
                    group=Group.FILE,
                    section=30,
                    order=12,
                    id=Command.SAVE_ALL,
                )
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

                menu_item = parent_menu.addItemWithTitle(
                    group.text, action=None, keyEquivalent=""
                )
                submenu = NSMenu.alloc().initWithTitle(group.text)
                parent_menu.setSubmenu(submenu, forItem=menu_item)

            # Install the item in the group cache.
            self._menu_groups[group] = submenu
            return submenu

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

    ######################################################################
    # App lifecycle
    ######################################################################

    # We can't call this under test conditions, because it would kill the test harness
    def exit(self):  # pragma: no cover
        self.loop.stop()

    def main_loop(self):
        self.loop.run_forever(lifecycle=CocoaLifecycle(self.native))

    def set_icon(self, icon):
        # If the icon is a path, it's an explicit icon; otherwise its the default icon
        if icon._impl.path:
            self.native.setApplicationIconImage(icon._impl.native)
        else:
            self.native.setApplicationIconImage(None)

    def set_main_window(self, window):
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

    def open_document(self, fileURL):
        """No-op when the app is not a ``DocumentApp``."""

    def select_file(self, **kwargs):
        """No-op when the app is not a ``DocumentApp``."""

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
        return self.native.keyWindow

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
