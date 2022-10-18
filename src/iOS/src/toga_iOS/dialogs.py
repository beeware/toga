import asyncio

from rubicon.objc import Block
from rubicon.objc.runtime import objc_id

from toga_iOS.libs import (
    UIAlertAction,
    UIAlertActionStyle,
    UIAlertController,
    UIAlertControllerStyle,
)


class BaseDialog:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.future = loop.create_future()

    def __eq__(self, other):
        raise RuntimeError(
            "Can't check dialog result directly; use await or an on_result handler"
        )

    def __bool__(self):
        raise RuntimeError(
            "Can't check dialog result directly; use await or an on_result handler"
        )

    def __await__(self):
        return self.future.__await__()


class AlertDialog(BaseDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__()
        self.on_result = on_result

        self.dialog = UIAlertController.alertControllerWithTitle(
            title, message=message, preferredStyle=UIAlertControllerStyle.Alert
        )

        self.populate_dialog()

        window._impl.controller.presentViewController(
            self.dialog,
            animated=False,
            completion=None,
        )

    def populate_dialog(
        self,
        dialog,
    ):
        pass

    def response(self, value):
        if self.on_result:
            self.on_result(self, value)

        self.future.set_result(value)

    def null_response(self, action: objc_id) -> None:
        self.response(None)

    def true_response(self, action: objc_id) -> None:
        self.response(True)

    def false_response(self, action: objc_id) -> None:
        self.response(False)

    def add_null_response_button(self, label):
        self.dialog.addAction(
            UIAlertAction.actionWithTitle(
                label,
                style=UIAlertActionStyle.Default,
                handler=Block(self.null_response, None, objc_id),
            )
        )

    def add_true_response_button(self, label):
        self.dialog.addAction(
            UIAlertAction.actionWithTitle(
                label,
                style=UIAlertActionStyle.Default,
                handler=Block(self.true_response, None, objc_id),
            )
        )

    def add_false_response_button(self, label):
        self.dialog.addAction(
            UIAlertAction.actionWithTitle(
                label,
                style=UIAlertActionStyle.Cancel,
                handler=Block(self.false_response, None, objc_id),
            )
        )


class InfoDialog(AlertDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(window, title, message, on_result=on_result)

    def populate_dialog(self):
        self.add_null_response_button("OK")


class QuestionDialog(AlertDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(window, title, message, on_result=on_result)

    def populate_dialog(self):
        self.add_true_response_button("Yes")
        self.add_false_response_button("No")


class ConfirmDialog(AlertDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(window, title, message, on_result=on_result)

    def populate_dialog(self):
        self.add_true_response_button("OK")
        self.add_false_response_button("Cancel")


class ErrorDialog(AlertDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(window, title, message, on_result=on_result)

    def populate_dialog(self):
        self.add_null_response_button("OK")


class StackTraceDialog(BaseDialog):
    def __init__(self, window, title, message, on_result=None, **kwargs):
        super().__init__()
        window.factory.not_implemented("Window.stack_trace_dialog()")


class SaveFileDialog(BaseDialog):
    def __init__(
        self,
        window,
        title,
        filename,
        initial_directory,
        file_types=None,
        on_result=None,
    ):
        super().__init__()
        window.factory.not_implemented("Window.save_file_dialog()")


class OpenFileDialog(BaseDialog):
    def __init__(
        self, window, title, initial_directory, file_types, multiselect, on_result=None
    ):
        super().__init__()
        window.factory.not_implemented("Window.open_file_dialog()")


class SelectFolderDialog(BaseDialog):
    def __init__(self, window, title, initial_directory, multiselect, on_result=None):
        super().__init__()
        window.factory.not_implemented("Window.select_folder_dialog()")
