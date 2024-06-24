from abc import ABC

import toga
from toga_web.libs import create_element


class BaseDialog(ABC):
    def show(self, host_window, future):
        self.future = future

        if self.native:
            # Add the dialog to the DOM. Don't differentiate between app and window
            # modal dialogs.
            toga.App.app._impl.native.appendChild(self.native)

            self.native.show()
        else:
            # Dialog doesn't have an implementation
            self.future.set_result(None)


class InfoDialog(BaseDialog):
    def __init__(self, title, message):
        super().__init__()
        self.native = create_element(
            "sl-dialog",
            id="toga-info-dialog",
            label=title,
            children=[
                create_element("p", content=message),
            ]
            + self.create_buttons(),
        )

    def create_buttons(self):
        close_button = create_element(
            "sl-button", slot="footer", variant="primary", content="Ok"
        )
        # Handle the close of the dialog
        close_button.onclick = self.dialog_close

        return [close_button]

    def dialog_close(self, event):
        self.native.hide()
        self.native.parentElement.removeChild(self.native)

        self.future.set_result(None)


class QuestionDialog(BaseDialog):
    def __init__(self, title, message):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.QuestionDialog()")
        self.native = None


class ConfirmDialog(BaseDialog):
    def __init__(self, title, message):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.ConfirmDialog()")
        self.native = None


class ErrorDialog(BaseDialog):
    def __init__(self, title, message):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.ErrorDialog()")
        self.native = None


class StackTraceDialog(BaseDialog):
    def __init__(self, title, message, **kwargs):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.StackTraceDialog()")
        self.native = None


class SaveFileDialog(BaseDialog):
    def __init__(
        self,
        interface,
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
        interface,
        title,
        initial_directory,
        file_types,
        multiselect,
    ):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.OpenFileDialog()")
        self.native = None


class SelectFolderDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        multiselect,
    ):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.SelectFolderDialog()")
        self.native = None
