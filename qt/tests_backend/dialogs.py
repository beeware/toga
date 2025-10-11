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
                            # On Qt, if a dialog is dismissed before it is fully
                            # realized, nothing will show or even flash.  Add
                            # an explicit redraw with a delay to have Qt realize
                            # the dialog before closing it, so the appearance
                            # of the dialog may be verified.
                            await self.redraw("Qt: Dialog display", delay=0.1)
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
        pytest.skip("Qt backend only implements info dialog so far")

    def setup_confirm_dialog_result(self, dialog, result):
        pytest.skip("Qt backend only implements info dialog so far")

    def setup_error_dialog_result(self, dialog):
        pytest.skip("Qt backend only implements info dialog so far")

    def setup_stack_trace_dialog_result(self, dialog, result):
        pytest.skip("Qt backend only implements info dialog so far")

    def setup_save_file_dialog_result(self, dialog, result):
        pytest.skip("Qt backend only implements info dialog so far")

    def setup_open_file_dialog_result(self, dialog, result, multiple_select):
        pytest.skip("Qt backend only implements info dialog so far")

    def setup_select_folder_dialog_result(self, dialog, result, multiple_select):
        pytest.skip("Qt backend only implements info dialog so far")

    def is_modal_dialog(self, dialog):
        if dialog._impl.native is not None:
            return dialog._impl.native.isModal()
        else:
            # The native dialog is created at execution time
            # to ensure a correct parent, so it is not feasible
            # to test the modality of the dialog before first
            # execution.
            return True
