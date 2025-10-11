from PySide6.QtWidgets import QMessageBox

import toga


class MessageDialog:
    def __init__(self, title, message, icon, buttons=QMessageBox.Ok):
        self.title, self.message, self.icon, self.buttons = (
            title,
            message,
            icon,
            buttons,
        )
        # Note: The parent of the dialog must be passed in at creation time.
        # Therefore, the native must be initially None.
        self.native = None

    def show(self, parent, future):
        self.future = future
        if parent is not None:
            self.native = QMessageBox(parent._impl.native)
        else:
            self.native = QMessageBox()
        self.native.setIcon(self.icon)
        self.native.setWindowTitle(self.title)
        self.native.setText(self.message)
        self.native.setStandardButtons(self.buttons)
        self.native.setModal(True)
        self.native.finished.connect(self.qt_response)
        self.native.show()

    def qt_response(self):
        self.future.set_result(None)


class InfoDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(title, message, icon=QMessageBox.Icon.Information)


class QuestionDialog:
    def __init__(self, *args, **kwargs):
        toga.App.app.factory.not_implemented("dialogs.QuestionDialog()")
        self.native = None


class ConfirmDialog:
    def __init__(self, *args, **kwargs):
        toga.App.app.factory.not_implemented("dialogs.ConfirmDialog()")
        self.native = None


class ErrorDialog:
    def __init__(self, *args, **kwargs):
        toga.App.app.factory.not_implemented("dialogs.ErrorDialog()")
        self.native = None


class StackTraceDialog:
    def __init__(self, *args, **kwargs):
        toga.App.app.factory.not_implemented("dialogs.StackTraceDialog()")
        self.native = None


class SaveFileDialog:
    def __init__(self, *args, **kwargs):
        toga.App.app.factory.not_implemented("dialogs.SaveFileDialog()")
        self.native = None


class OpenFileDialog:
    def __init__(self, *args, **kwargs):
        toga.App.app.factory.not_implemented("dialogs.OpenFileDialog()")
        self.native = None


class SelectFolderDialog:
    def __init__(self, *args, **kwargs):
        toga.App.app.factory.not_implemented("dialogs.SelectFolderDialog()")
        self.native = None
