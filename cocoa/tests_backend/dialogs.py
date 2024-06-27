from unittest.mock import Mock

from rubicon.objc.collections import ObjCListInstance

from toga_cocoa.libs import (
    NSURL,
    NSAlertFirstButtonReturn,
    NSAlertSecondButtonReturn,
    NSModalResponseCancel,
    NSModalResponseOK,
    NSOpenPanel,
    NSSavePanel,
)


class DialogsMixin:
    supports_multiple_select_folder = True

    def setup_info_dialog_result(self, dialog):
        self._setup_alert_dialog_result(dialog, NSAlertFirstButtonReturn)

    def setup_question_dialog_result(self, dialog, result):
        if result:
            self._setup_alert_dialog_result(dialog, NSAlertFirstButtonReturn)
        else:
            self._setup_alert_dialog_result(dialog, NSAlertSecondButtonReturn)

    def setup_confirm_dialog_result(self, dialog, result):
        if result:
            self._setup_alert_dialog_result(dialog, NSAlertFirstButtonReturn)
        else:
            self._setup_alert_dialog_result(dialog, NSAlertSecondButtonReturn)

    def setup_error_dialog_result(self, dialog):
        self._setup_alert_dialog_result(dialog, NSAlertFirstButtonReturn)

    def setup_stack_trace_dialog_result(self, dialog, result):
        if result is None:
            self._setup_alert_dialog_result(dialog, NSAlertFirstButtonReturn)
        else:
            if result:
                self._setup_alert_dialog_result(dialog, NSAlertFirstButtonReturn)
            else:
                self._setup_alert_dialog_result(dialog, NSAlertSecondButtonReturn)

    def setup_save_file_dialog_result(self, dialog, result):
        assert isinstance(dialog._impl.native, NSSavePanel)

        if result:
            self._setup_file_dialog_result(dialog, result=NSModalResponseOK)
        else:
            self._setup_file_dialog_result(dialog, result=NSModalResponseCancel)

    def setup_open_file_dialog_result(self, dialog, result, multiple_select):
        assert isinstance(dialog._impl.native, NSOpenPanel)

        if result is not None:
            if multiple_select:
                # Since we are mocking selected_path(), it's never actually invoked
                # under test conditions. Call it just to confirm that it returns the
                # type we think it does.
                assert isinstance(dialog._impl.selected_paths(), ObjCListInstance)

                dialog._impl.selected_paths = Mock(
                    return_value=[
                        NSURL.alloc().initFileURLWithPath(str(path), isDirectory=False)
                        for path in result
                    ]
                )
            else:
                dialog._impl.selected_path = Mock(
                    return_value=NSURL.alloc().initFileURLWithPath(
                        str(result),
                        isDirectory=False,
                    )
                )

            self._setup_file_dialog_result(dialog, result=NSModalResponseOK)
        else:
            self._setup_file_dialog_result(dialog, result=NSModalResponseCancel)

    def setup_select_folder_dialog_result(self, dialog, result, multiple_select):
        assert isinstance(dialog._impl.native, NSOpenPanel)

        if result is not None:
            if multiple_select:
                # Since we are mocking selected_path(), it's never actually invoked
                # under test conditions. Call it just to confirm that it returns the
                # type we think it does.
                assert isinstance(dialog._impl.selected_paths(), ObjCListInstance)

                dialog._impl.selected_paths = Mock(
                    return_value=[
                        NSURL.alloc().initFileURLWithPath(str(path), isDirectory=True)
                        for path in result
                    ]
                )
            else:
                dialog._impl.selected_path = Mock(
                    return_value=NSURL.alloc().initFileURLWithPath(
                        str(result),
                        isDirectory=True,
                    )
                )

            self._setup_file_dialog_result(dialog, result=NSModalResponseOK)
        else:
            self._setup_file_dialog_result(dialog, result=NSModalResponseCancel)

    def is_modal_dialog(self, dialog):
        return True
