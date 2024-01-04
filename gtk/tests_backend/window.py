import asyncio
from pathlib import Path
from unittest.mock import Mock

import pytest

from toga_gtk.libs import Gdk, Gio, Gtk

from .probe import BaseProbe


class WindowProbe(BaseProbe):
    # GTK defers a lot of window behavior to the window manager, which means some features
    # either don't exist, or we can't guarantee they behave the way Toga would like.
    supports_closable = True
    supports_minimizable = False
    supports_multiple_select_folder = True
    supports_move_while_hidden = False
    supports_unminimize = False
    supports_positioning = False

    def __init__(self, app, window):
        super().__init__()
        self.app = app
        self.window = window
        self.impl = window._impl
        self.native = window._impl.native
        assert isinstance(self.native, Gtk.Window)

    async def wait_for_window(self, message, minimize=False, full_screen=False):
        await self.redraw(message, delay=0.5 if (full_screen or minimize) else 0.1)

    def close(self):
        if self.is_closable:
            self.native.close()

    @property
    def content_size(self):
        content = self.impl.container
        return (content.get_width(), content.get_height())

    @property
    def is_full_screen(self):
        return self.native.is_fullscreen()

    @property
    def is_resizable(self):
        return self.native.get_resizable()

    @property
    def is_closable(self):
        return self.native.get_deletable()

    @property
    def is_minimized(self):
        return bool(self.native.get_surface().get_state() & Gdk.ToplevelState.MINIMIZED)

    def minimize(self):
        self.native.minimize()

    def unminimize(self):
        self.native.present()

    def assert_as_image(self, screenshot_size, content_size):
        return self.assert_image_size(screenshot_size, content_size)

    async def wait_for_dialog(self, dialog, message):
        # It can take a moment for the dialog to disappear and the response to be
        # handled. However, the delay can be variable; use the completion of the future
        # as a proxy for "the dialog is done", with a safety catch that will prevent an
        # indefinite wait.
        await self.redraw(message, delay=0.1)
        count = 0
        while dialog.get_visible() and count < 20:
            await asyncio.sleep(0.1)
            count += 1
        assert not dialog.get_visible(), "Dialog didn't close"

    async def close_info_dialog(self, dialog):
        assert isinstance(dialog.native, Gtk.AlertDialog)

        dialog._dialog_window.response(0)
        await self.wait_for_dialog(dialog._dialog_window, "Info dialog dismissed")

    async def close_question_dialog(self, dialog, result):
        assert isinstance(dialog.native, Gtk.AlertDialog)

        if result:
            dialog._dialog_window.response(0)
        else:
            dialog._dialog_window.response(1)

        await self.wait_for_dialog(
            dialog._dialog_window,
            f"Question dialog ({'YES' if result else 'NO'}) dismissed",
        )

    async def close_confirm_dialog(self, dialog, result):
        assert isinstance(dialog.native, Gtk.AlertDialog)

        # get the dialog window
        if result:
            dialog._dialog_window.response(0)
        else:
            dialog._dialog_window.response(1)

        await self.wait_for_dialog(
            dialog._dialog_window,
            f"Question dialog ({'OK' if result else 'CANCEL'}) dismissed",
        )

    async def close_error_dialog(self, dialog):
        assert isinstance(dialog.native, Gtk.AlertDialog)

        dialog._dialog_window.response(0)
        await self.wait_for_dialog(dialog._dialog_window, "Error dialog dismissed")

    async def close_stack_trace_dialog(self, dialog, result):
        assert isinstance(dialog.native, Gtk.AlertDialog)

        if result is None:
            dialog._dialog_window.response(0)
            await self.wait_for_dialog(
                dialog._dialog_window, "Stack trace dialog dismissed"
            )
        else:
            if result:
                dialog._dialog_window.response(0)
            else:
                dialog._dialog_window.response(1)

            await self.wait_for_dialog(
                dialog._dialog_window,
                f"Stack trace dialog ({'RETRY' if result else 'QUIT'}) dismissed",
            )

    async def close_save_file_dialog(self, dialog, result):
        assert isinstance(dialog.native, Gtk.FileDialog)

        if result:
            dialog._dialog_window.response(Gtk.ResponseType.ACCEPT)
        else:
            dialog._dialog_window.response(Gtk.ResponseType.CANCEL)

        await self.wait_for_dialog(
            dialog._dialog_window,
            f"Save file dialog ({'SAVE' if result else 'CANCEL'}) dismissed",
        )

    async def close_open_file_dialog(self, dialog, result, multiple_select):
        assert isinstance(dialog.native, Gtk.FileDialog)

        # GTK's file dialog shows folders first; but if a folder is selected when the
        # "open" button is pressed, it opens that folder. To prevent this, if we're
        # expecting this dialog to return a result, ensure a file is selected. We don't
        # care which file it is, as we're mocking the return value of the dialog.
        if result is not None:
            gtk_file = Gio.File.new_for_path(__file__)
            dialog._dialog_window.set_file(gtk_file)

            # We don't know how long it will take for the GUI to update, so iterate
            # for a while until the change has been applied.
            await self.redraw("Selected a single (arbitrary) file")
            count = 0
            while dialog.selected_path() != __file__ and count < 10:
                await asyncio.sleep(0.1)
                count += 1

            assert dialog.selected_path() == __file__, "Dialog didn't select dummy file"

        if result is not None:
            if multiple_select:
                # Since we are mocking selected_paths(), it's never actually invoked
                # under test conditions. Call it just to confirm that it returns the
                # type we think it does.
                assert isinstance(dialog.selected_paths(), list)

                dialog.selected_paths = Mock(
                    return_value=[str(path) for path in result]
                )
            else:
                dialog.selected_path = Mock(return_value=str(result))

            # If there's nothing selected, you can't press Open.
            dialog._dialog_window.response(Gtk.ResponseType.ACCEPT)
        else:
            dialog._dialog_window.response(Gtk.ResponseType.CANCEL)

        await self.wait_for_dialog(
            dialog._dialog_window,
            (
                f"Open {'multiselect ' if multiple_select else ''}file dialog "
                f"({'OPEN' if result else 'CANCEL'}) dismissed"
            ),
        )

    async def close_select_folder_dialog(self, dialog, result, multiple_select):
        assert isinstance(dialog.native, Gtk.FileDialog)

        # GTK's file dialog might open on default location that doesn't have anything
        # that can be selected, which alters closing behavior. To provide consistent
        # test conditions, select an arbitrary folder that we know has subfolders. We
        # don't care which folder it is, as we're mocking the return value of the
        # dialog.
        if result is not None:
            folder = str(Path(__file__).parent.parent)
            dialog._dialog_window.set_current_folder(Gio.File.new_for_path(folder))

            # We don't know how long it will take for the GUI to update, so iterate
            # for a while until the change has been applied.
            await self.redraw("Selected a single (arbitrary) folder")
            count = 0
            while dialog.selected_path() != folder and count < 10:
                await asyncio.sleep(0.1)
                count += 1

            assert dialog.selected_path() == folder, "Dialog didn't select dummy folder"

        if result is not None:
            if multiple_select:
                # Since we are mocking selected_paths(), it's never actually invoked
                # under test conditions. Call it just to confirm that it returns the
                # type we think it does.
                assert isinstance(dialog.selected_paths(), list)

                dialog.selected_paths = Mock(
                    return_value=[str(path) for path in result]
                )
            else:
                dialog.selected_path = Mock(return_value=str(result))

            # If there's nothing selected, you can't press Select.
            dialog._dialog_window.response(Gtk.ResponseType.ACCEPT)
        else:
            dialog._dialog_window.response(Gtk.ResponseType.CANCEL)

        await self.wait_for_dialog(
            dialog._dialog_window,
            (
                f"{'Multiselect' if multiple_select else ' Select'} folder dialog "
                f"({'OPEN' if result else 'CANCEL'}) dismissed"
            ),
        )

    def has_toolbar(self):
        pytest.skip("Toolbar doesn't implemented on GTK")

    def assert_is_toolbar_separator(self, index, section=False):
        item = self.impl.native_toolbar.get_nth_item(index)
        assert isinstance(item, Gtk.SeparatorToolItem)
        assert item.get_draw() == (not section)

    def assert_toolbar_item(self, index, label, tooltip, has_icon, enabled):
        item = self.impl.native_toolbar.get_nth_item(index)
        assert item.get_label() == label
        # FIXME: get_tooltip_text() doesn't work. The tooltip can be set, but the
        # API to return the value just doesn't work. If it is ever fixed, this
        # is the test for it:
        # assert (None if item.get_tooltip_text() is None else item.get_tooltip_text()) == tooltip
        assert (item.get_icon_widget() is not None) == has_icon
        assert item.get_sensitive() == enabled

    def press_toolbar_button(self, index):
        item = self.impl.native_toolbar.get_nth_item(index)
        item.emit("clicked")
