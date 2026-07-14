import asyncio
from unittest.mock import Mock

from System import Array as WinArray, String as WinString

from toga_winforms import _use_dotnet_core
from toga_winforms.libs.user32 import GetFocus


class DialogsMixin:
    supports_multiple_select_folder = False

    async def _close_dialog(
        self,
        future,
        dialog,
        char,
        alt=False,
        char2=None,
        pre_close_test_method=None,
    ):
        # When a dialog is opened, it receives the input focus. An opening event can be
        # detected by a change in the input focus.
        focus = GetFocus()
        while focus == GetFocus():  # noqa ASYNC110
            await asyncio.sleep(0.01)

        # File dialogs require some extra time to be ready.
        await self.redraw("Dialog opened", delay=0.2)

        try:
            if pre_close_test_method:
                pre_close_test_method(dialog)
        finally:
            try:
                await self.type_character(char, alt=alt)
                if char2:
                    # If a second character press is needed, wait a moment
                    # for the effect of the first character to take effect.
                    await self.redraw("wait for char", delay=0.1)
                    await self.type_character(char2)
            except Exception as e:
                # An error occurred closing the dialog; that means the dialog
                # isn't what as expected, so record that in the future.
                future.set_exception(e)

    async def _open_dialog(
        self,
        host_window,
        future,
        dialog,
        char,
        alt,
        char2,
        pre_close_test_method,
    ):

        asyncio.create_task(
            self._close_dialog(
                future,
                dialog,
                char,
                alt,
                char2,
                pre_close_test_method,
            )
        )

        # A small delay to ensure that _close_dialog has started.
        await asyncio.sleep(0.1)

        dialog.orig_show(host_window, future)

    def _setup_dialog_result(
        self,
        dialog,
        char,
        alt=False,
        char2=None,
        pre_close_test_method=None,
    ):
        # Install an overridden show method that invokes the original,
        # but then closes the open dialog.
        dialog.orig_show = dialog._impl.show

        def automated_show(host_window, future):
            asyncio.create_task(
                self._open_dialog(
                    host_window,
                    future,
                    dialog,
                    char,
                    alt,
                    char2,
                    pre_close_test_method,
                )
            )

        dialog._impl.show = automated_show

    def setup_info_dialog_result(self, dialog, pre_close_test_method=None):
        self._setup_dialog_result(
            dialog, "\n", pre_close_test_method=pre_close_test_method
        )

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
            # Under .NET Core, selecting pressing Enter once
            # displays the contents of the selected folder.
            # A second enter is needed to select that folder.
            char2 = "\n" if _use_dotnet_core else None
            self._setup_dialog_result(dialog, "\n", char2=char2)

    def is_modal_dialog(self, dialog):
        return True
