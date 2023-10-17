from abc import ABC, abstractmethod

from rubicon.objc import Block
from rubicon.objc.runtime import objc_id

from toga_iOS.libs import (
    UIAlertAction,
    UIAlertActionStyle,
    UIAlertController,
    UIAlertControllerStyle,
)


class BaseDialog(ABC):
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self


class AlertDialog(BaseDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(interface=interface)
        self.on_result = on_result

        self.native = UIAlertController.alertControllerWithTitle(
            title, message=message, preferredStyle=UIAlertControllerStyle.Alert
        )

        self.populate_dialog()

        interface.window._impl.native.rootViewController.presentViewController(
            self.native,
            animated=False,
            completion=None,
        )

    @abstractmethod
    def populate_dialog(self, native):
        ...

    def response(self, value):
        self.on_result(self, value)
        self.interface.future.set_result(value)

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
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(interface, title, message, on_result=on_result)

    def populate_dialog(self):
        self.add_null_response_button("OK")


class QuestionDialog(AlertDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(interface, title, message, on_result=on_result)

    def populate_dialog(self):
        self.add_true_response_button("Yes")
        self.add_false_response_button("No")


class ConfirmDialog(AlertDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(interface, title, message, on_result=on_result)

    def populate_dialog(self):
        self.add_true_response_button("OK")
        self.add_false_response_button("Cancel")


class ErrorDialog(AlertDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(interface, title, message, on_result=on_result)

    def populate_dialog(self):
        self.add_null_response_button("OK")


class StackTraceDialog(BaseDialog):
    def __init__(self, interface, title, message, on_result=None, **kwargs):
        super().__init__(interface=interface)
        interface.window.factory.not_implemented("Window.stack_trace_dialog()")


class SaveFileDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        filename,
        initial_directory,
        file_types=None,
        on_result=None,
    ):
        super().__init__(interface=interface)
        interface.window.factory.not_implemented("Window.save_file_dialog()")


class OpenFileDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        file_types,
        multiple_select,
        on_result=None,
    ):
        super().__init__(interface=interface)
        interface.window.factory.not_implemented("Window.open_file_dialog()")


class SelectFolderDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        multiple_select,
        on_result=None,
    ):
        super().__init__(interface=interface)
        interface.window.factory.not_implemented("Window.select_folder_dialog()")
