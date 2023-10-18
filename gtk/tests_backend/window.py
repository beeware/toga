import asyncio
from pathlib import Path
from unittest.mock import Mock

from toga_gtk.libs import Gdk, Gtk

from .probe import BaseProbe


class WindowProbe(BaseProbe):
    # GTK defers a lot of window behavior to the window manager, which means some features
    # either don't exist, or we can't guarantee they behave the way Toga would like.
    supports_closable = True
    supports_minimizable = False
    supports_multiple_select_folder = True
    supports_move_while_hidden = False
    supports_unminimize = False

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
        content_allocation = self.impl.container.get_allocation()
        return (content_allocation.width, content_allocation.height)

    @property
    def is_full_screen(self):
        return bool(self.native.get_window().get_state() & Gdk.WindowState.FULLSCREEN)

    @property
    def is_resizable(self):
        return self.native.get_resizable()

    @property
    def is_closable(self):
        return self.native.get_deletable()

    @property
    def is_minimized(self):
        return bool(self.native.get_window().get_state() & Gdk.WindowState.ICONIFIED)

    def minimize(self):
        self.native.iconify()

    def unminimize(self):
        self.native.deiconify()

    async def wait_for_dialog(self, dialog, message):
        # It can take a moment for the dialog to disappear and the response to be
        # handled. However, the delay can be variable; use the completion of the future
        # as a proxy for "the dialog is done", with a safety catch that will prevent an
        # indefinite wait.
        await self.redraw(message, delay=0.1)
        count = 0
        while dialog.native.get_visible() and count < 20:
            await asyncio.sleep(0.1)
            count += 1
        assert not dialog.native.get_visible(), "Dialog didn't close"

    async def close_info_dialog(self, dialog):
        dialog.native.response(Gtk.ResponseType.OK)
        await self.wait_for_dialog(dialog, "Info dialog dismissed")

    async def close_question_dialog(self, dialog, result):
        if result:
            dialog.native.response(Gtk.ResponseType.YES)
        else:
            dialog.native.response(Gtk.ResponseType.NO)

        await self.wait_for_dialog(
            dialog,
            f"Question dialog ({'YES' if result else 'NO'}) dismissed",
        )

    async def close_confirm_dialog(self, dialog, result):
        if result:
            dialog.native.response(Gtk.ResponseType.OK)
        else:
            dialog.native.response(Gtk.ResponseType.CANCEL)

        await self.wait_for_dialog(
            dialog,
            f"Question dialog ({'OK' if result else 'CANCEL'}) dismissed",
        )

    async def close_error_dialog(self, dialog):
        dialog.native.response(Gtk.ResponseType.CANCEL)
        await self.wait_for_dialog(dialog, "Error dialog dismissed")

    async def close_stack_trace_dialog(self, dialog, result):
        if result is None:
            dialog.native.response(Gtk.ResponseType.OK)
            await self.wait_for_dialog(dialog, "Stack trace dialog dismissed")
        else:
            if result:
                dialog.native.response(Gtk.ResponseType.OK)
            else:
                dialog.native.response(Gtk.ResponseType.CANCEL)

            await self.wait_for_dialog(
                dialog,
                f"Stack trace dialog ({'RETRY' if result else 'QUIT'}) dismissed",
            )

    async def close_save_file_dialog(self, dialog, result):
        assert isinstance(dialog.native, Gtk.FileChooserDialog)

        if result:
            dialog.native.response(Gtk.ResponseType.OK)
        else:
            dialog.native.response(Gtk.ResponseType.CANCEL)

        await self.wait_for_dialog(
            dialog,
            f"Save file dialog ({'SAVE' if result else 'CANCEL'}) dismissed",
        )

    async def close_open_file_dialog(self, dialog, result, multiple_select):
        assert isinstance(dialog.native, Gtk.FileChooserDialog)

        # GTK's file dialog shows folders first; but if a folder is selected when the
        # "open" button is pressed, it opens that folder. To prevent this, if we're
        # expecting this dialog to return a result, ensure a file is selected. We don't
        # care which file it is, as we're mocking the return value of the dialog.
        if result:
            dialog.native.select_filename(__file__)
            # We don't know how long it will take for the GUI to update, so iterate
            # for a while until the change has been applied.
            await self.redraw("Selected a single (arbitrary) file")
            count = 0
            while dialog.native.get_filename() != __file__ and count < 10:
                await asyncio.sleep(0.1)
                count += 1
            assert (
                dialog.native.get_filename() == __file__
            ), "Dialog didn't select dummy file"

        if result is not None:
            if multiple_select:
                if result:
                    # Since we are mocking selected_path(), it's never actually invoked
                    # under test conditions. Call it just to confirm that it returns the
                    # type we think it does.
                    assert isinstance(dialog.selected_paths(), list)

                    dialog.selected_paths = Mock(
                        return_value=[str(path) for path in result]
                    )
            else:
                dialog.selected_path = Mock(return_value=str(result))

            # If there's nothing selected, you can't press OK.
            if result:
                dialog.native.response(Gtk.ResponseType.OK)
            else:
                dialog.native.response(Gtk.ResponseType.CANCEL)
        else:
            dialog.native.response(Gtk.ResponseType.CANCEL)

        await self.wait_for_dialog(
            dialog,
            (
                f"Open {'multiselect ' if multiple_select else ''}file dialog "
                f"({'OPEN' if result else 'CANCEL'}) dismissed"
            ),
        )

    async def close_select_folder_dialog(self, dialog, result, multiple_select):
        assert isinstance(dialog.native, Gtk.FileChooserDialog)

        # GTK's file dialog might open on default location that doesn't have anything
        # that can be selected, which alters closing behavior. To provide consistent
        # test conditions, select an arbitrary folder that we know has subfolders. We
        # don't care which folder it is, as we're mocking the return value of the
        # dialog.
        if result:
            folder = str(Path(__file__).parent.parent)
            dialog.native.set_current_folder(folder)
            # We don't know how long it will take for the GUI to update, so iterate
            # for a while until the change has been applied.
            await self.redraw("Selected a single (arbitrary) folder")
            count = 0
            while dialog.native.get_current_folder() != folder and count < 10:
                await asyncio.sleep(0.1)
                count += 1
            assert (
                dialog.native.get_current_folder() == folder
            ), "Dialog didn't select dummy folder"

        if result is not None:
            if multiple_select:
                if result:
                    # Since we are mocking selected_path(), it's never actually invoked
                    # under test conditions. Call it just to confirm that it returns the
                    # type we think it does.
                    assert isinstance(dialog.selected_paths(), list)

                    dialog.selected_paths = Mock(
                        return_value=[str(path) for path in result]
                    )
            else:
                dialog.selected_path = Mock(return_value=str(result))

            # If there's nothing selected, you can't press OK.
            if result:
                dialog.native.response(Gtk.ResponseType.OK)
            else:
                dialog.native.response(Gtk.ResponseType.CANCEL)
        else:
            dialog.native.response(Gtk.ResponseType.CANCEL)

        await self.wait_for_dialog(
            dialog,
            (
                f"{'Multiselect' if multiple_select else ' Select'} folder dialog "
                f"({'OPEN' if result else 'CANCEL'}) dismissed"
            ),
        )

    def has_toolbar(self):
        return self.impl.native_toolbar.get_n_items() > 0

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
