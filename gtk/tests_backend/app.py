from pathlib import Path

import pytest

from toga_gtk.keys import gtk_accel, toga_key
from toga_gtk.libs import Gtk

from .probe import BaseProbe


class AppProbe(BaseProbe):
    supports_key = True
    supports_key_mod3 = True

    def __init__(self, app):
        super().__init__()
        self.app = app
        assert isinstance(self.app._impl.native, Gtk.Application)

    @property
    def config_path(self):
        return Path.home() / ".config/testbed"

    @property
    def data_path(self):
        return Path.home() / ".local/share/testbed"

    @property
    def cache_path(self):
        return Path.home() / ".cache/testbed"

    @property
    def logs_path(self):
        return Path.home() / ".local/state/testbed/log"

    @property
    def is_cursor_visible(self):
        pytest.skip("Cursor visibility not implemented on GTK")

    def is_full_screen(self, window):
        return window._impl.native.is_fullscreen()

    def content_size(self, window):
        content = window._impl.container
        return (content.get_width(), content.get_height())

    def _menu_item(self, path):
        main_menu = self.app._impl.native.get_menubar()
        menu = main_menu
        orig_path = path.copy()
        try:
            while True:
                label, path = path[0], path[1:]
                items = {}
                for index in range(menu.get_n_items()):
                    section = menu.get_item_link(index, "section")
                    if section:
                        for section_index in range(section.get_n_items()):
                            items[
                                section.get_item_attribute_value(
                                    section_index, "label"
                                ).get_string()
                            ] = (section, section_index)
                    else:
                        items[
                            menu.get_item_attribute_value(index, "label").get_string()
                        ] = (menu, index)

                if label == "*":
                    item = items[self.app.formal_name]
                else:
                    item = items[label]

                menu = item[0].get_item_link(item[1], "submenu")
        except IndexError:
            pass
        except AttributeError:
            raise AssertionError(f"Menu {' > '.join(orig_path)} not found")

        action_name = item[0].get_item_attribute_value(item[1], "action").get_string()
        cmd_id = action_name.split(".")[1]
        action = self.app._impl.native.lookup_action(cmd_id)
        return action

    def _activate_menu_item(self, path):
        item = self._menu_item(path)
        item.emit("activate", None)

    def activate_menu_exit(self):
        pytest.skip("Exit menu item doesn't implemented on GTK")

    def activate_menu_about(self):
        pytest.skip("Menu about item doesn't implemented on GTK")

    async def close_about_dialog(self):
        self.app._impl._close_about(self.app._impl.native_about_dialog)

    def activate_menu_visit_homepage(self):
        # Homepage is a link on the GTK about page.
        pytest.xfail("GTK doesn't have a visit homepage menu item")

    def assert_system_menus(self):
        pytest.skip("System menus doesn't implemented on GTK")

    def activate_menu_close_window(self):
        pytest.xfail("GTK doesn't have a window management menu items")

    def activate_menu_close_all_windows(self):
        pytest.xfail("GTK doesn't have a window management menu items")

    def activate_menu_minimize(self):
        pytest.xfail("GTK doesn't have a window management menu items")

    def assert_menu_item(self, path, enabled):
        pytest.skip("Menu item doesn't implemented on GTK")

    def keystroke(self, combination):
        accel = gtk_accel(combination)

        shortcut = Gtk.Shortcut.new()
        shortcut.set_trigger(Gtk.ShortcutTrigger.parse_string(accel))

        return toga_key(shortcut)
