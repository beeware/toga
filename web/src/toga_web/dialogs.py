from abc import ABC

from toga_web.libs import create_element


class BaseDialog(ABC):
    def __init__(self, interface):
        self.interface = interface
        self.interface.impl = self


class InfoDialog(BaseDialog):
    def __init__(self, interface, title, message):
        super().__init__(interface=interface)
        self.native = create_element(
            "sl-dialog",
            id="toga-info-dialog",
            label=title,
            children=[
                create_element("p", content=message),
            ]
            + self.create_buttons(),
        )

        # Add the dialog to the DOM.
        interface.window.app._impl.native.appendChild(self.native)

        self.native.show()

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

        self.interface.set_result(None)


class QuestionDialog(BaseDialog):
    def __init__(self, interface, title, message):
        super().__init__(interface=interface)

        interface.window.factory.not_implemented("Window.question_dialog()")

        self.interface.set_result(None)


class ConfirmDialog(BaseDialog):
    def __init__(self, interface, title, message):
        super().__init__(interface=interface)

        interface.window.factory.not_implemented("Window.confirm_dialog()")

        self.interface.set_result(None)


class ErrorDialog(BaseDialog):
    def __init__(self, interface, title, message):
        super().__init__(interface=interface)

        interface.window.factory.not_implemented("Window.error_dialog()")

        self.interface.set_result(None)


class StackTraceDialog(BaseDialog):
    def __init__(self, interface, title, message, **kwargs):
        super().__init__(interface=interface)

        interface.window.factory.not_implemented("Window.stack_trace_dialog()")

        self.interface.set_result(None)


class SaveFileDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        filename,
        initial_directory,
        file_types=None,
    ):
        super().__init__(interface=interface)

        interface.window.factory.not_implemented("Window.save_file_dialog()")

        self.interface.set_result(None)


class OpenFileDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        file_types,
        multiselect,
    ):
        super().__init__(interface=interface)

        interface.window.factory.not_implemented("Window.open_file_dialog()")

        self.interface.set_result(None)


class SelectFolderDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        multiselect,
    ):
        super().__init__(interface=interface)

        interface.window.factory.not_implemented("Window.select_folder_dialog()")

        self.interface.set_result(None)
