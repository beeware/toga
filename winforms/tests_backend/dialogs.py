import asyncio
from unittest.mock import Mock

from System import Array as WinArray, String as WinString


class DialogsMixin:
    supports_multiple_select_folder = False

    def _setup_dialog_result(self, dialog, char, alt=False):
        # Install an overridden show method that invokes the original,
        # but then closes the open dialog.
        orig_show = dialog._impl.show

        def automated_show(host_window, future):
            orig_show(host_window, future)

            async def _close_dialog():
                try:
                    # Give the inner event loop a chance to start. The MessageBox dialogs work with
                    # sleep(0), but the file dialogs require it to be positive for some reason.
                    await asyncio.sleep(0.001)

                    await self.type_character(char, alt=alt)

                except Exception as e:
                    # An error occurred closing the dialog; that means the dialog
                    # isn't what as expected, so record that in the future.
                    future.set_exception(e)

            asyncio.create_task(_close_dialog(), name="close-dialog")

        dialog._impl.show = automated_show

    def setup_info_dialog_result(self, dialog):
        self._setup_dialog_result(dialog, "\n")

    def setup_question_dialog_result(self, dialog, result):
        self._setup_dialog_result(dialog, "y" if result else "n")

    def setup_confirm_dialog_result(self, dialog, result):
        self._setup_dialog_result(dialog, "\n" if result else "<esc>")

    def setup_error_dialog_result(self, dialog):
        self._setup_dialog_result(dialog, "\n")

    def setup_stack_trace_dialog_result(self, dialog, result):
        self._setup_dialog_result(
            dialog,
            {None: "o", True: "r", False: "q"}[result],
            alt=True,
        )

    def setup_save_file_dialog_result(self, dialog, result):
        self._setup_dialog_result(dialog, "\n" if result else "<esc>")

    def setup_open_file_dialog_result(self, dialog, result, multiple_select):
        if result is None:
            self._setup_dialog_result(dialog, "<esc>")
        else:
            if multiple_select:
                # Since we are mocking selected_path(), it's never actually invoked
                # under test conditions. Call it just to confirm that it returns the
                # type we think it does.
                assert isinstance(
                    dialog._impl.selected_paths(),
                    type(WinArray.CreateInstance(WinString, 0)),
                )

                # native.FileNames is read-only, so we have to mock the mechanism
                # returning the result
                dialog._impl.native.FileName = str(result[0])  # Enable the OK button
                dialog._impl.selected_paths = Mock(
                    return_value=[str(path) for path in result]
                )
            else:
                dialog._impl.native.FileName = str(result)

            self._setup_dialog_result(dialog, "\n")

    def setup_select_folder_dialog_result(self, dialog, result, multiple_select):
        if result is None:
            self._setup_dialog_result(dialog, "<esc>")
        else:
            dialog._impl.native.SelectedPath = str(
                result[-1] if multiple_select else result
            )
            self._setup_dialog_result(dialog, "\n")

    def is_modal_dialog(self, dialog):
        return True
