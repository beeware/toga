import os
from pathlib import Path

import PIL.Image
import pytest

import toga
from toga_gtk.keys import gtk_accel, toga_key
from toga_gtk.libs import IS_WAYLAND, Gdk, Gtk

from .dialogs import DialogsMixin
from .probe import BaseProbe


class AppProbe(BaseProbe, DialogsMixin):
    supports_key = True
    supports_key_mod3 = True
    # Gtk 3.24.41 ships with Ubuntu 24.04 where present() works on Wayland
    supports_current_window_assignment = not (
        IS_WAYLAND and BaseProbe.GTK_VERSION < (3, 24, 41)
    )

    def __init__(self, app):
        super().__init__()
        self.app = app
        assert isinstance(self.app._impl.native, Gtk.Application)
        assert IS_WAYLAND is (os.environ.get("WAYLAND_DISPLAY", "") != "")

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
        return bool(
            window._impl.native.get_window().get_state() & Gdk.WindowState.FULLSCREEN
        )

    def content_size(self, window):
        content_allocation = window._impl.container.get_allocation()
        return (content_allocation.width, content_allocation.height)

    def assert_app_icon(self, icon):
        for window in self.app.windows:
            # We have no real way to check we've got the right icon; use pixel peeping as a
            # guess. Construct a PIL image from the current icon.
            img = toga.Image(window._impl.native.get_icon()).as_format(PIL.Image.Image)

            if icon:
                # The explicit alt icon has blue background, with green at a point 1/3 into
                # the image
                assert img.getpixel((5, 5)) == (211, 230, 245)
                mid_color = img.getpixel((img.size[0] // 3, img.size[1] // 3))
                assert mid_color == (0, 204, 9)
            else:
                # The default icon is transparent background, and brown in the center.
                assert img.getpixel((5, 5))[3] == 0
                mid_color = img.getpixel((img.size[0] // 2, img.size[1] // 2))
                assert mid_color == (149, 119, 73, 255)

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

        action = item[0].get_item_attribute_value(item[1], "action")
        if action:
            action_name = (
                item[0].get_item_attribute_value(item[1], "action").get_string()
            )
            cmd_id = action_name.split(".")[1]
            action = self.app._impl.native.lookup_action(cmd_id)
        return item, action

    def _activate_menu_item(self, path):
        _, action = self._menu_item(path)
        action.emit("activate", None)

    def activate_menu_exit(self):
        self._activate_menu_item(["*", "Quit"])

    def activate_menu_about(self):
        self._activate_menu_item(["Help", "About Toga Testbed"])

    async def close_about_dialog(self):
        self.app._impl._close_about(self.app._impl.native_about_dialog)

    def activate_menu_visit_homepage(self):
        # Homepage is a link on the GTK about page.
        pytest.xfail("GTK doesn't have a visit homepage menu item")

    def assert_system_menus(self):
        self.assert_menu_item(["*", "Preferences"], enabled=False)
        self.assert_menu_item(["*", "Quit"], enabled=True)

        self.assert_menu_item(["File", "New Example Document"], enabled=True)
        self.assert_menu_item(["File", "New Read-only Document"], enabled=True)
        self.assert_menu_item(["File", "Open..."], enabled=True)
        self.assert_menu_item(["File", "Save"], enabled=True)
        self.assert_menu_item(["File", "Save As..."], enabled=True)
        self.assert_menu_item(["File", "Save All"], enabled=True)

        self.assert_menu_item(["Help", "Visit homepage"], enabled=True)
        self.assert_menu_item(["Help", "About Toga Testbed"], enabled=True)

    def activate_menu_close_window(self):
        pytest.xfail("GTK doesn't have a window management menu items")

    def activate_menu_close_all_windows(self):
        pytest.xfail("GTK doesn't have a window management menu items")

    def activate_menu_minimize(self):
        pytest.xfail("GTK doesn't have a window management menu items")

    def assert_menu_item(self, path, enabled):
        _, action = self._menu_item(path)
        assert action.get_enabled() == enabled

    def assert_menu_order(self, path, expected):
        item, action = self._menu_item(path)
        menu = item[0].get_item_link(item[1], "submenu")

        # Loop over the sections
        actual = []
        for index in range(menu.get_n_items()):
            section = menu.get_item_link(index, "section")
            if section:
                if actual:
                    actual.append("---")

                for section_index in range(section.get_n_items()):
                    actual.append(
                        section.get_item_attribute_value(
                            section_index, "label"
                        ).get_string()
                    )
            else:
                actual.append(
                    section.get_item_attribute_value(index, "label").get_string()
                )

        assert actual == expected

    def keystroke(self, combination):
        accel = gtk_accel(combination)
        state = 0

        if "<Primary>" in accel:
            state |= Gdk.ModifierType.CONTROL_MASK
            accel = accel.replace("<Primary>", "")
        if "<Alt>" in accel:
            state |= Gdk.ModifierType.META_MASK
            accel = accel.replace("<Alt>", "")
        if "<Hyper>" in accel:
            state |= Gdk.ModifierType.HYPER_MASK
            accel = accel.replace("<Hyper>", "")
        if "<Shift>" in accel:
            state |= Gdk.ModifierType.SHIFT_MASK
            accel = accel.replace("<Shift>", "")

        keyval = getattr(
            Gdk,
            f"KEY_{accel}",
            {
                "!": Gdk.KEY_exclam,
                "<home>": Gdk.KEY_Home,
                "F5": Gdk.KEY_F5,
            }.get(accel, None),
        )

        event = Gdk.Event.new(Gdk.EventType.KEY_PRESS)
        event.keyval = keyval
        event.length = 1
        event.is_modifier = state != 0
        event.state = state

        return toga_key(event)

    async def restore_standard_app(self):
        # No special handling needed to restore standard app.
        await self.redraw("Restore to standard app")

    async def open_initial_document(self, monkeypatch, document_path):
        pytest.xfail("GTK doesn't require initial document support")

    def open_document_by_drag(self, document_path):
        pytest.xfail("GTK doesn't support opening documents by drag")

    def has_status_icon(self, status_icon):
        return status_icon._impl.native is not None

    def status_menu_items(self, status_icon):
        menu = status_icon._impl.native.get_primary_menu()
        if menu:
            return [
                {
                    "": "---",
                    "About Toga Testbed": "**ABOUT**",
                    "Quit": "**EXIT**",
                }.get(child.get_label(), child.get_label())
                for child in menu.get_children()
            ]
        else:
            # It's a button status item
            return None

    def activate_status_icon_button(self, item_id):
        self.app.status_icons[item_id]._impl.native.emit("activate", 0, 0)

    def activate_status_menu_item(self, item_id, title):
        menu = self.app.status_icons[item_id]._impl.native.get_primary_menu()
        item = {child.get_label(): child for child in menu.get_children()}[title]

        item.emit("activate")
