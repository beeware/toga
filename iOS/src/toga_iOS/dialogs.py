from abc import abstractmethod

from rubicon.objc import Block, objc_id

import toga
from toga_iOS.libs import (
    UIAlertAction,
    UIAlertActionStyle,
    UIAlertController,
    UIAlertControllerStyle,
)


class BaseDialog:
    def show(self, host_window, future):
        self.future = future

        if self.native:
            # Don't differentiate between app and window-modal dialogs.
            toga.App.app.current_window._impl.native.rootViewController.presentViewController(
                self.native,
                animated=False,
                completion=None,
            )
        else:
            # Dialog doesn't have an implementation. This can't be covered, as
            # the testbed shortcuts the test before showing the dialog.
            self.future.set_result(None)  # pragma: no cover


class AlertDialog(BaseDialog):
    def __init__(self, title, message):
        super().__init__()

        self.native = UIAlertController.alertControllerWithTitle(
            title, message=message, preferredStyle=UIAlertControllerStyle.Alert
        ).retain()

        self.populate_dialog()

    @abstractmethod
    def populate_dialog(self, native): ...

    def response(self, value):
        self.future.set_result(value)

    def null_response(self, action: objc_id) -> None:
        self.response(None)

    def true_response(self, action: objc_id) -> None:
        self.response(True)

    def false_response(self, action: objc_id) -> None:
        self.response(False)

    def add_null_response_button(self, label):
        self.native.addAction(
            UIAlertAction.actionWithTitle(
                label,
                style=UIAlertActionStyle.Default,
                handler=Block(self.null_response, None, objc_id),
            )
        )

    def add_true_response_button(self, label):
        self.native.addAction(
            UIAlertAction.actionWithTitle(
                label,
                style=UIAlertActionStyle.Default,
                handler=Block(self.true_response, None, objc_id),
            )
        )

    def add_false_response_button(self, label):
        self.native.addAction(
            UIAlertAction.actionWithTitle(
                label,
                style=UIAlertActionStyle.Cancel,
                handler=Block(self.false_response, None, objc_id),
            )
        )


class InfoDialog(AlertDialog):
    def populate_dialog(self):
        self.add_null_response_button("OK")


class QuestionDialog(AlertDialog):
    def populate_dialog(self):
        self.add_true_response_button("Yes")
        self.add_false_response_button("No")


class ConfirmDialog(AlertDialog):
    def populate_dialog(self):
        self.add_true_response_button("OK")
        self.add_false_response_button("Cancel")


class ErrorDialog(AlertDialog):
    def populate_dialog(self):
        self.add_null_response_button("OK")


class StackTraceDialog(BaseDialog):
    def __init__(self, title, message, **kwargs):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.StackTraceDialog()")
        self.native = None


class SaveFileDialog(BaseDialog):
    def __init__(
        self,
        title,
        filename,
        initial_directory,
        file_types=None,
    ):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.SaveFileDialog()")
        self.native = None


class OpenFileDialog(BaseDialog):
    def __init__(
        self,
        title,
        initial_directory,
        file_types,
        multiple_select,
    ):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.OpenFileDialog()")
        self.native = None


class SelectFolderDialog(BaseDialog):
    def __init__(
        self,
        title,
        initial_directory,
        multiple_select,
    ):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.SelectFolderDialog()")
        self.native = None
