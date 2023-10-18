from abc import ABC

from java import dynamic_proxy

from android import R
from android.app import AlertDialog
from android.content import DialogInterface


class OnClickListener(dynamic_proxy(DialogInterface.OnClickListener)):
    def __init__(self, fn=None, value=None):
        super().__init__()
        self._fn = fn
        self._value = value

    def onClick(self, _dialog, _which):
        self._fn(self._value)


class BaseDialog(ABC):
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self


class TextDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        message,
        positive_text,
        negative_text=None,
        icon=None,
        on_result=None,
    ):
        super().__init__(interface=interface)
        self.on_result = on_result

        self.native = AlertDialog.Builder(interface.window._impl.app.native)
        self.native.setCancelable(False)
        self.native.setTitle(title)
        self.native.setMessage(message)
        if icon is not None:
            self.native.setIcon(icon)

        self.native.setPositiveButton(
            positive_text,
            OnClickListener(
                self.completion_handler,
                True if (negative_text is not None) else None,
            ),
        )
        if negative_text is not None:
            self.native.setNegativeButton(
                negative_text, OnClickListener(self.completion_handler, False)
            )
        self.native.show()

    def completion_handler(self, return_value: bool) -> None:
        self.on_result(self, return_value)
        self.interface.future.set_result(return_value)


class InfoDialog(TextDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            positive_text="OK",
            on_result=on_result,
        )


class QuestionDialog(TextDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            positive_text="Yes",
            negative_text="No",
            on_result=on_result,
        )


class ConfirmDialog(TextDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            positive_text="OK",
            negative_text="Cancel",
            on_result=on_result,
        )


class ErrorDialog(TextDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            positive_text="OK",
            icon=R.drawable.ic_dialog_alert,
            on_result=on_result,
        )


class StackTraceDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        message,
        on_result=None,
        **kwargs,
    ):
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
