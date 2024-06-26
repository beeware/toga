from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock

from toga_gtk.libs import Gtk


class DialogsMixin:
    supports_multiple_select_folder = True

    def _wait_for_dialog(self, message=None):
        # A synchronous delay we can use when programmatically driving dialogs
        # Wait for 0.1s (1s when running slow) to allow for GUI actions.
        print("Waiting for dialog" if message is None else message)
        delay_end = datetime.now() + timedelta(seconds=1 if self.app.run_slow else 0.1)
        while datetime.now() < delay_end:
            Gtk.main_iteration_do(blocking=False)

    def _default_close_handler(self, dialog, gtk_result):
        self._wait_for_dialog("Wait for dialog to appear")
        dialog._impl.native.response(gtk_result)
        self._wait_for_dialog("Wait for dialog to disappear")

    def _setup_dialog_result(self, dialog, gtk_result, close_handler=None):
        # Install an overridden show method that invokes the original,
        # but then closes the open dialog.
        orig_show = dialog._impl.show

        def automated_show(host_window, future):
            orig_show(host_window, future)

            if close_handler:
                close_handler(dialog, gtk_result)
            else:
                self._default_close_handler(dialog, gtk_result)

        dialog._impl.show = automated_show

    def setup_info_dialog_result(self, dialog):
        self._setup_dialog_result(dialog, Gtk.ResponseType.OK)

    def setup_question_dialog_result(self, dialog, result):
        self._setup_dialog_result(
            dialog,
            Gtk.ResponseType.YES if result else Gtk.ResponseType.NO,
        )

    def setup_confirm_dialog_result(self, dialog, result):
        self._setup_dialog_result(
            dialog,
            Gtk.ResponseType.OK if result else Gtk.ResponseType.CANCEL,
        )

    def setup_error_dialog_result(self, dialog):
        self._setup_dialog_result(dialog, Gtk.ResponseType.CANCEL)

    def setup_stack_trace_dialog_result(self, dialog, result):
        if result is None:
            self._setup_dialog_result(dialog, Gtk.ResponseType.OK)
        else:
            self._setup_dialog_result(
                dialog,
                Gtk.ResponseType.OK if result else Gtk.ResponseType.CANCEL,
            )

    def setup_save_file_dialog_result(self, dialog, result):
        assert isinstance(dialog._impl.native, Gtk.FileChooserDialog)

        self._setup_dialog_result(
            dialog,
            Gtk.ResponseType.OK if result else Gtk.ResponseType.CANCEL,
        )

    def setup_open_file_dialog_result(self, dialog, result, multiple_select):
        assert isinstance(dialog._impl.native, Gtk.FileChooserDialog)

        # GTK's file dialog shows folders first; but if a folder is selected when the
        # "open" button is pressed, it opens that folder. To prevent this, if we're
        # expecting this dialog to return a result, ensure a file is selected. We don't
        # care which file it is, as we're mocking the return value of the dialog.
        def close_handler(dialog, gtk_result):
            # Set up mocked results
            if result is not None:
                if multiple_select:
                    if result:
                        # Since we are mocking selected_path(), it's never actually invoked
                        # under test conditions. Call it just to confirm that it returns the
                        # type we think it does.
                        assert isinstance(dialog._impl.selected_paths(), list)

                        dialog._impl.selected_paths = Mock(
                            return_value=[str(path) for path in result]
                        )
                else:
                    dialog._impl.selected_path = Mock(return_value=str(result))

            self._wait_for_dialog("Wait for dialog to appear")
            if result:
                dialog._impl.native.select_filename(__file__)
                self._wait_for_dialog("Wait for file to be selected")
                assert (
                    dialog._impl.native.get_filename() == __file__
                ), "Dialog didn't select dummy file"
            else:
                self._wait_for_dialog("Wait for dialog to be dismissed")

            dialog._impl.native.response(gtk_result)

        # If there's nothing selected, you can't press OK.
        if result is not None:
            self._setup_dialog_result(
                dialog,
                Gtk.ResponseType.OK if result else Gtk.ResponseType.CANCEL,
                close_handler=close_handler,
            )
        else:
            self._setup_dialog_result(
                dialog, Gtk.ResponseType.CANCEL, close_handler=close_handler
            )

    def setup_select_folder_dialog_result(self, dialog, result, multiple_select):
        assert isinstance(dialog._impl.native, Gtk.FileChooserDialog)

        def close_handler(dialog, gtk_result):
            if result is not None:
                if multiple_select:
                    if result:
                        # Since we are mocking selected_path(), it's never actually invoked
                        # under test conditions. Call it just to confirm that it returns the
                        # type we think it does.
                        assert isinstance(dialog._impl.selected_paths(), list)

                        dialog._impl.selected_paths = Mock(
                            return_value=[str(path) for path in result]
                        )
                else:
                    dialog._impl.selected_path = Mock(return_value=str(result))

            # GTK's file dialog might open on default location that doesn't have anything
            # that can be selected, which alters closing behavior. To provide consistent
            # test conditions, select an arbitrary folder that we know has subfolders. We
            # don't care which folder it is, as we're mocking the return value of the
            # dialog.
            self._wait_for_dialog("Wait for dialog to appear")
            if result:
                folder = str(Path(__file__).parent.parent)
                dialog._impl.native.set_current_folder(folder)

                self._wait_for_dialog("Wait for folder to be selected")
                # We don't know how long it will take for the GUI to update, so iterate
                # for a while until the change has been applied.
                assert (
                    dialog._impl.native.get_current_folder() == folder
                ), "Dialog didn't select dummy folder"
            else:
                self._wait_for_dialog("Wait for folder to be dismissed")

            dialog._impl.native.response(gtk_result)

        if result is not None:
            # If there's nothing selected, you can't press OK.
            self._setup_dialog_result(
                dialog,
                Gtk.ResponseType.OK if result else Gtk.ResponseType.CANCEL,
                close_handler=close_handler,
            )
        else:
            self._setup_dialog_result(
                dialog,
                Gtk.ResponseType.CANCEL,
                close_handler=close_handler,
            )

    def is_modal_dialog(self, dialog):
        return dialog._impl.native.get_modal()
