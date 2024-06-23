import asyncio
from unittest.mock import Mock


class DialogsMixin:
    supports_multiple_select_folder = False

    def _setup_dialog_result(self, dialog, char, alt=False):
        cleanup = dialog._impl.cleanup

        def auto_cleanup(future):
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

            asyncio.ensure_future(_close_dialog())

            return cleanup(future)

        dialog._impl.cleanup = auto_cleanup

    def setup_info_dialog(self, dialog):
        self._setup_dialog("\n")

    def setup_question_dialog(self, dialog, result):
        self._setup_dialog("y" if result else "n")

    def setup_confirm_dialog(self, dialog, result):
        self._setup_dialog("\n" if result else "<esc>")

    def setup_error_dialog(self, dialog):
        self._setup_dialog("\n")

    def setup_stack_trace_dialog(self, dialog, result):
        self._setup_dialog(
            {None: "o", True: "r", False: "q"}[result],
            alt=True,
        )

    def setup_save_file_dialog(self, dialog, result):
        self._setup_dialog("\n" if result else "<esc>")

    def setup_open_file_dialog(self, dialog, result, multiple_select):
        if result is None:
            self._setup_dialog("<esc>")
        else:
            if multiple_select:
                # native.FileNames is read-only, so we have to mock the mechanism
                # returning the result
                dialog.native.FileName = str(result[0])  # Enable the OK button
                dialog.selected_paths = Mock(result=[str(path) for path in result])
            else:
                dialog.native.FileName = str(result)

            self._setup_dialog("\n")

    def setup_select_folder_dialog(self, dialog, result, multiple_select):
        if result is None:
            self._setup_dialog("<esc>")
        else:
            dialog.native.SelectedPath = str(result[-1] if multiple_select else result)
            self._setup_dialog("\n")

    def is_modal_dialog(self, dialog):
        return True
