import asyncio
from pathlib import Path
from unittest.mock import Mock

from toga_gtk.libs import Gtk


class DialogsMixin:
    supports_multiple_select_folder = True

    def _setup_dialog_result(self, dialog, result, user_action=None):
        cleanup = dialog._impl.cleanup

        def auto_cleanup(future):
            async def _close_dialog():
                if user_action:
                    await user_action

                dialog.native.response(result)

                # It can take a moment for the dialog to disappear and the response to be
                # handled. However, the delay can be variable; use the completion of the future
                # as a proxy for "the dialog is done", with a safety catch that will prevent an
                # indefinite wait.
                try:
                    await self.redraw("Closing dialog", delay=0.1)
                    count = 0
                    while dialog.native.get_visible() and count < 20:
                        await asyncio.sleep(0.1)
                        count += 1
                    assert not dialog.native.get_visible(), "Dialog didn't close"

                except Exception as e:
                    # An error occurred closing the dialog; that means the dialog
                    # isn't what as expected, so record that in the future.
                    future.set_exception(e)

            asyncio.ensure_future(_close_dialog())

            return cleanup(future)

        dialog._impl.cleanup = auto_cleanup

    def setup_info_dialog_result(self, dialog):
        self._setup_dialog_result(Gtk.ResponseType.OK)

    def setup_question_dialog_result(self, dialog, result):
        self._setup_dialog_result(
            Gtk.ResponseType.YES if result else Gtk.ResponseType.NO
        )

    def setup_confirm_dialog_result(self, dialog, result):
        self._setup_dialog_result(
            Gtk.ResponseType.OK if result else Gtk.ResponseType.CANCEL
        )

    def setup_error_dialog_result(self, dialog):
        self._setup_dialog_result(Gtk.ResponseType.CANCEL)

    def setup_stack_trace_dialog_result(self, dialog, result):
        if result is None:
            self._setup_dialog_result(Gtk.ResponseType.OK)
        else:
            self._setup_dialog_result(
                Gtk.ResponseType.OK if result else Gtk.ResponseType.CANCEL
            )

    def setup_save_file_dialog_result(self, dialog, result):
        assert isinstance(dialog.native, Gtk.FileChooserDialog)

        self._setup_dialog_result(
            Gtk.ResponseType.OK if result else Gtk.ResponseType.CANCEL
        )

    def setup_open_file_dialog_result(self, dialog, result, multiple_select):
        assert isinstance(dialog.native, Gtk.FileChooserDialog)

        # GTK's file dialog shows folders first; but if a folder is selected when the
        # "open" button is pressed, it opens that folder. To prevent this, if we're
        # expecting this dialog to return a result, ensure a file is selected. We don't
        # care which file it is, as we're mocking the return value of the dialog.
        async def user_action():
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
        if result is not None:
            self._setup_dialog_result(
                Gtk.ResponseType.OK if result else Gtk.ResponseType.CANCEL,
                user_action=user_action(),
            )
        else:
            self._setup_dialog_result(
                Gtk.ResponseType.CANCEL,
                user_action=user_action(),
            )

    def setup_select_folder_dialog_result(self, dialog, result, multiple_select):
        assert isinstance(dialog.native, Gtk.FileChooserDialog)

        async def user_action():
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

        if result is not None:
            # If there's nothing selected, you can't press OK.
            self._setup_dialog_result(
                Gtk.ResponseType.OK if result else Gtk.ResponseType.CANCEL,
                user_action=user_action(),
            )
        else:
            self._setup_dialog_result(
                Gtk.ResponseType.CANCEL,
                user_action=user_action(),
            )

    def is_modal_dialog(self, dialog):
        return dialog._impl.native.get_modal()
