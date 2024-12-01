import pytest

from toga_iOS.libs import NSDate, NSRunLoop


class DialogsMixin:
    @property
    def dialog_view_controller(self):
        return self.app.current_window._impl.native.rootViewController

    def _setup_alert_dialog(self, dialog, action_index, pre_close_test_method=None):
        # Install an overridden show method that invokes the original,
        # but then closes the open dialog.
        orig_show = dialog._impl.show

        def automated_show(host_window, future):
            orig_show(host_window, future)

            # Inject a small pause without blocking the event loop
            NSRunLoop.currentRunLoop.runUntilDate(
                NSDate.dateWithTimeIntervalSinceNow(1.0 if self.app.run_slow else 0.2)
            )
            try:
                if pre_close_test_method:
                    pre_close_test_method(dialog)
            finally:
                try:
                    # Close the dialog and trigger the completion handler
                    self.dialog_view_controller.dismissViewControllerAnimated(
                        False, completion=None
                    )
                    dialog._impl.native.actions[action_index].handler(
                        dialog._impl.native
                    )
                except Exception as e:
                    # An error occurred closing the dialog; that means the dialog
                    # isn't what as expected, so record that in the future.
                    future.set_exception(e)

        dialog._impl.show = automated_show

    def setup_info_dialog_result(self, dialog, pre_close_test_method=None):
        self._setup_alert_dialog(dialog, 0, pre_close_test_method=pre_close_test_method)

    def setup_question_dialog_result(self, dialog, result):
        self._setup_alert_dialog(dialog, 0 if result else 1)

    def setup_confirm_dialog_result(self, dialog, result):
        self._setup_alert_dialog(dialog, 0 if result else 1)

    def setup_error_dialog_result(self, dialog):
        self._setup_alert_dialog(dialog, 0)

    def setup_stack_trace_dialog_result(self, dialog, result):
        pytest.skip("Stack Trace dialog not implemented on iOS")

    def setup_save_file_dialog_result(self, dialog, result):
        pytest.skip("Save File dialog not implemented on iOS")

    def setup_open_file_dialog_result(self, dialog, result, multiple_select):
        pytest.skip("Open File dialog not implemented on iOS")

    def setup_select_folder_dialog_result(self, dialog, result, multiple_select):
        pytest.skip("Select Folder dialog not implemented on iOS")

    def is_modal_dialog(self, dialog):
        return True
