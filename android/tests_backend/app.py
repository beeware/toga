from pathlib import Path

from android import R
from org.beeware.android import MainActivity
from pytest import xfail

from toga import Group

from .probe import BaseProbe
from .window import WindowProbe


class AppProbe(BaseProbe):
    supports_key = False

    def __init__(self, app):
        super().__init__(app)
        self.native = self.app._impl.native
        self.main_window_probe = WindowProbe(self.app, app.main_window)
        assert isinstance(self.native, MainActivity)

    def get_app_context(self):
        return self.native.getApplicationContext()

    @property
    def config_path(self):
        return Path(self.get_app_context().getFilesDir().getPath()) / "config"

    @property
    def data_path(self):
        return Path(self.get_app_context().getFilesDir().getPath()) / "data"

    @property
    def cache_path(self):
        return Path(self.get_app_context().getCacheDir().getPath())

    @property
    def logs_path(self):
        return Path(self.get_app_context().getFilesDir().getPath()) / "log"

    def assert_app_icon(self, icon):
        xfail("Android apps don't have app icons at runtime")

    def _menu_item(self, path):
        menu = self.main_window_probe._native_menu()
        for i_path, label in enumerate(path):
            if i_path == 0 and label == Group.COMMANDS.text:
                continue

            for i_item in range(menu.size()):
                item = menu.getItem(i_item)
                assert not item.requestsActionButton()
                if item.getTitle() == label and not item.requiresActionButton():
                    break
            else:
                raise AssertionError(f"no item named {path[:i_path+1]}")

            if i_path < len(path) - 1:
                # Simulate opening the submenu.
                assert self.native.onOptionsItemSelected(item) is False
                menu = item.getSubMenu()
                assert menu is not None

        return item

    def _activate_menu_item(self, path):
        assert self.native.onOptionsItemSelected(self._menu_item(path))

    def activate_menu_exit(self):
        xfail("This backend doesn't have an exit command")

    def activate_menu_about(self):
        self._activate_menu_item(["About Toga Testbed"])

    async def close_about_dialog(self):
        await self.main_window_probe.close_info_dialog(None)

    def activate_menu_visit_homepage(self):
        xfail("This backend doesn't have a visit homepage command")

    def assert_menu_item(self, path, *, enabled=True):
        assert self._menu_item(path).isEnabled() == enabled

    def assert_menu_order(self, path, expected):
        item = self._menu_item(path)
        menu = item.getSubMenu()

        # Android doesn't include separators, so we need to exclude separators from the
        # length check, and add an offset when a separator is expected.
        separator_offset = 0
        assert menu.size() == len([item for item in expected if item != "---"])
        for i, title in enumerate(expected):
            if title == "---":
                separator_offset += 1
            else:
                assert menu.getItem(i - separator_offset).getTitle() == title

    def assert_system_menus(self):
        self.assert_menu_item(["About Toga Testbed"])

    def activate_menu_close_window(self):
        xfail("This backend doesn't have a window management menu")

    def activate_menu_close_all_windows(self):
        xfail("This backend doesn't have a window management menu")

    def activate_menu_minimize(self):
        xfail("This backend doesn't have a window management menu")

    def enter_background(self):
        xfail(
            "This is possible (https://stackoverflow.com/a/7071289), but there's no "
            "easy way to bring it to the foreground again"
        )

    def enter_foreground(self):
        xfail("See enter_background")

    def terminate(self):
        xfail("Can't simulate this action without killing the app")

    def rotate(self):
        self.native.findViewById(
            R.id.content
        ).getViewTreeObserver().dispatchOnGlobalLayout()
