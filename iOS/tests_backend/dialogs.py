import pytest

from toga_iOS.libs import NSDate, NSRunLoop


class DialogsMixin:
    @property
    def dialog_view_controller(self):
        return self.app.current_window._impl.native.rootViewController

    def _setup_alert_dialog(self, dialog, action_index):
        cleanup = dialog._impl.cleanup

        def auto_cleanup(future):
            # Inject a small pause without blocking the event loop
            NSRunLoop.currentRunLoop.runUntilDate(
                NSDate.dateWithTimeIntervalSinceNow(1.0 if self.app.run_slow else 0.2)
            )
            # Close the dialog and trigger the completion handler
            self.dialog_view_controller.dismissViewControllerAnimated(
                False, completion=None
            )
            dialog._impl.native.actions[action_index].handler(dialog._impl.native)

            return cleanup(future)

        dialog._impl.cleanup = auto_cleanup

    def setup_info_dialog_result(self, dialog):
        self._setup_alert_dialog(dialog, 0)

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
