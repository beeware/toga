import abc

from android import R
from android.app import AlertDialog
from android.content import DialogInterface, Intent
from java import dynamic_proxy

import toga

from .libs import utilfile


class OnClickListener(dynamic_proxy(DialogInterface.OnClickListener)):
    def __init__(self, fn=None, value=None):
        super().__init__()
        self._fn = fn
        self._value = value

    def onClick(self, _dialog, _which):
        self._fn(self._value)


class BaseDialog:
    def show(self, host_window, future):
        self.future = future

        if self.native:
            # Show the dialog. Don't differentiate between app and window modal dialogs.
            self.native.show()
        else:
            # Dialog doesn't have an implementation. This can't be covered, as
            # the testbed shortcuts the test before showing the dialog.
            self.future.set_result(None)  # pragma: no cover


class TextDialog(BaseDialog):
    def __init__(
        self,
        title,
        message,
        positive_text,
        negative_text=None,
        icon=None,
    ):
        super().__init__()

        self.native_builder = AlertDialog.Builder(
            toga.App.app.current_window._impl.app.native
        )
        self.native_builder.setCancelable(False)
        self.native_builder.setTitle(title)
        self.native_builder.setMessage(message)
        if icon is not None:
            self.native_builder.setIcon(icon)

        self.native_builder.setPositiveButton(
            positive_text,
            OnClickListener(
                self.completion_handler,
                True if (negative_text is not None) else None,
            ),
        )
        if negative_text is not None:
            self.native_builder.setNegativeButton(
                negative_text, OnClickListener(self.completion_handler, False)
            )
        self.native = self.native_builder.create()

    def completion_handler(self, return_value: bool) -> None:
        self.future.set_result(return_value)


class InfoDialog(TextDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            positive_text="OK",
        )


class QuestionDialog(TextDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            positive_text="Yes",
            negative_text="No",
        )


class ConfirmDialog(TextDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            positive_text="OK",
            negative_text="Cancel",
        )


class ErrorDialog(TextDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            positive_text="OK",
            icon=R.drawable.ic_dialog_alert,
        )


class StackTraceDialog(BaseDialog):
    def __init__(
        self,
        title,
        message,
        **kwargs,
    ):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.StackTraceDialog()")
        self.native = None


class HandlerFileDialog(abc.ABC):
    """An abstract class that handles file manager calls"""

    def __init__(self, parent):
        self.parent = parent
        self.app = toga.App.app._impl
        self.mActive = toga.App.app._impl.native

    @abc.abstractmethod
    def show(self):
        """Запуск менеджера"""
        pass


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


class HandlerOpenDialog(HandlerFileDialog):
    def show(self):
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType("*/*")
        self.app.start_activity(intent, on_complete=self.parent.handler)


class OpenFileDialog(BaseDialog):

    def __init__(
        self,
        title,
        initial_directory,
        file_types,
        multiple_select,
    ):
        self.native = HandlerOpenDialog(self)
        self.mActive = self.native.mActive

    def handler(self, code, indent):
        uri = indent.getData()
        content = self.mActive.getContentResolver()
        reader = utilfile.PathReader(content, uri)
        self.future.set_result(reader)


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
