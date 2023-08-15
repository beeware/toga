from pathlib import Path

from rubicon.objc import ObjCClass, send_message
from rubicon.objc.runtime import objc_id

from toga_cocoa.libs import NSApplication

from .probe import BaseProbe

NSPanel = ObjCClass("NSPanel")


class AppProbe(BaseProbe):
    def __init__(self, app):
        super().__init__()
        self.app = app
        assert isinstance(self.app._impl.native, NSApplication)

    @property
    def config_path(self):
        return Path.home() / "Library" / "Preferences" / "org.beeware.toga.testbed"

    @property
    def data_path(self):
        return (
            Path.home() / "Library" / "Application Support" / "org.beeware.toga.testbed"
        )

    @property
    def cache_path(self):
        return Path.home() / "Library" / "Caches" / "org.beeware.toga.testbed"

    @property
    def logs_path(self):
        return Path.home() / "Library" / "Logs" / "org.beeware.toga.testbed"

    @property
    def is_cursor_visible(self):
        # There's no API level mechanism to detect cursor visibility;
        # fall back to the implementation's proxy variable.
        return self.app._impl._cursor_visible

    def is_full_screen(self, window):
        return window.content._impl.native.isInFullScreenMode()

    def content_size(self, window):
        return (
            window.content._impl.native.frame.size.width,
            window.content._impl.native.frame.size.height,
        )

    def _menu_item(self, path):
        main_menu = self.app._impl.native.mainMenu

        menu = main_menu
        orig_path = path.copy()
        try:
            while True:
                label, path = path[0], path[1:]
                item = menu.itemWithTitle(label)
                menu = item.submenu
        except IndexError:
            pass
        except AttributeError:
            raise AssertionError(f"Menu {' > '.join(orig_path)} not found")

        return item

    def _activate_menu_item(self, path):
        item = self._menu_item(path)
        send_message(
            self.app._impl.native.delegate,
            item.action,
            item,
            restype=None,
            argtypes=[objc_id],
        )

    def activate_menu_exit(self):
        self._activate_menu_item(["*", "Quit Toga Testbed"])

    def activate_menu_about(self):
        self._activate_menu_item(["*", "About Toga Testbed"])

    def close_about_dialog(self):
        about_dialog = self.app._impl.native.keyWindow
        if isinstance(about_dialog, NSPanel):
            about_dialog.close()

    def activate_menu_visit_homepage(self):
        self._activate_menu_item(["Help", "Visit homepage"])

    def assert_system_menus(self):
        self.assert_menu_item(["*", "About Toga Testbed"], enabled=True)
        self.assert_menu_item(["*", "Settings\u2026"], enabled=False)
        self.assert_menu_item(["*", "Hide Toga Testbed"], enabled=True)
        self.assert_menu_item(["*", "Hide Others"], enabled=True)
        self.assert_menu_item(["*", "Show All"], enabled=True)
        self.assert_menu_item(["*", "Quit Toga Testbed"], enabled=True)

        self.assert_menu_item(["File", "Close Window"], enabled=True)
        self.assert_menu_item(["File", "Close All Windows"], enabled=True)

        self.assert_menu_item(["Edit", "Undo"], enabled=True)
        self.assert_menu_item(["Edit", "Redo"], enabled=True)
        self.assert_menu_item(["Edit", "Cut"], enabled=True)
        self.assert_menu_item(["Edit", "Copy"], enabled=True)
        self.assert_menu_item(["Edit", "Paste"], enabled=True)
        self.assert_menu_item(["Edit", "Paste and Match Style"], enabled=True)
        self.assert_menu_item(["Edit", "Delete"], enabled=True)
        self.assert_menu_item(["Edit", "Select All"], enabled=True)

        self.assert_menu_item(["Window", "Minimize"], enabled=True)

        self.assert_menu_item(["Help", "Visit homepage"], enabled=True)

    def activate_menu_close_window(self):
        self._activate_menu_item(["File", "Close Window"])

    def activate_menu_close_all_windows(self):
        self._activate_menu_item(["File", "Close All Windows"])

    def activate_menu_minimize(self):
        self._activate_menu_item(["Window", "Minimize"])

    def assert_menu_item(self, path, enabled):
        item = self._menu_item(path)
        assert item.isEnabled() == enabled
