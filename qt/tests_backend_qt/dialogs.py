import asyncio

import pytest
from PySide6.QtWidgets import QDialog


class DialogsMixin:
    supports_multiple_select_folder = True

    def _default_close_handler(self, dialog, qt_result):
        dialog._impl.native.done(qt_result)
        # Note: somehow at this point if I do QApplication.processEvents()
        # it'll hang forever however the signal we use is emitted immediately
        # anyways.

    def _setup_dialog_result(
        self, dialog, qt_result, close_handler=None, pre_close_test_method=None
    ):
        orig_exec = dialog._impl.show

        def automated_exec(host_window, future):
            orig_exec(host_window, future)

            async def _close_dialog():
                try:
                    if pre_close_test_method:
                        pre_close_test_method(dialog)
                finally:
                    try:
                        if close_handler:
                            close_handler(dialog, qt_result)
                        else:
                            # This is nessacary because without it the dialog would
                            # not display for some reason.
                            # Won't be an issue with public API if the dialog hasn't
                            # been shown successfully yet,
                            # no user could dismiss it and the call can't complete.
                            await self.redraw(
                                "Dialog Internal: Just before close", delay=0.1
                            )
                            self._default_close_handler(dialog, qt_result)
                    except Exception as e:
                        future.set_exception(e)

            asyncio.create_task(_close_dialog())

        dialog._impl.show = automated_exec

    def setup_info_dialog_result(self, dialog, pre_close_test_method=None):
        self._setup_dialog_result(
            dialog,
            QDialog.DialogCode.Accepted,
            pre_close_test_method=pre_close_test_method,
        )

    def setup_question_dialog_result(self, dialog, result):
        pytest.skip("no impl")

    def setup_confirm_dialog_result(self, dialog, result):
        pytest.skip("no impl")

    def setup_error_dialog_result(self, dialog):
        pytest.skip("no impl")

    def setup_stack_trace_dialog_result(self, dialog, result):
        pytest.skip("no impl")

    def setup_save_file_dialog_result(self, dialog, result):
        pytest.skip("no impl")

    def setup_open_file_dialog_result(self, dialog, result, multiple_select):
        pytest.skip("no impl")

    def setup_select_folder_dialog_result(self, dialog, result, multiple_select):
        pytest.skip("no impl")

    def is_modal_dialog(self, dialog):
        if dialog._impl.native is not None:
            return dialog._impl.native.isModal()
        else:
            # Can't really get this tested...
            # we need to create native when our parent window is known
            return True
