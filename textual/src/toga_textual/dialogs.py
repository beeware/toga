from abc import ABC

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Label, Static


class TextualDialog(ModalScreen[bool]):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def compose(self) -> ComposeResult:
        self.native_title = Header(name=self.impl.title)
        self.impl.compose_content(self)
        self.native_buttons = self.impl.create_buttons()
        self.native_button_box = Horizontal(*self.native_buttons)
        self.native_dialog = Vertical(
            self.native_title,
            self.native_content,
            self.native_button_box,
            id="dialog",
        )
        yield self.native_dialog

    def on_mount(self) -> None:
        self.styles.align = ("center", "middle")

        self.native_dialog.styles.width = 50
        self.native_dialog.styles.border = ("solid", "darkgray")

        self.impl.mount_content(self)

        self.native_button_box.styles.align = ("center", "middle")
        for native_button in self.native_buttons:
            native_button.styles.margin = (0, 1, 0, 1)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "result-True":
            self.dismiss(True)
        elif event.button.id == "result-False":
            self.dismiss(False)
        else:
            self.dismiss(None)


class BaseDialog(ABC):
    def __init__(self, interface, title, message, on_result):
        self.interface = interface
        self.interface._impl = self
        self.on_result = on_result
        self.title = title
        self.message = message

        self.native = TextualDialog(self)
        self.interface.app._impl.native.push_screen(self.native, self.on_close)

    def compose_content(self, dialog):
        dialog.native_content = Label(self.message, id="message")

    def mount_content(self, dialog):
        dialog.native_content.styles.margin = 1
        dialog.native_content.styles.height = 5

        dialog.native_dialog.styles.height = 13

    def on_close(self, result: bool):
        self.on_result(self, result)
        self.interface.future.set_result(result)


class InfoDialog(BaseDialog):
    def create_buttons(self):
        return [
            Button("OK", variant="primary", id="result-None"),
        ]


class QuestionDialog(BaseDialog):
    def create_buttons(self):
        return [
            Button("Yes", variant="primary", id="result-True"),
            Button("No", variant="error", id="result-False"),
        ]


class ConfirmDialog(BaseDialog):
    def create_buttons(self):
        return [
            Button("Cancel", variant="error", id="result-False"),
            Button("OK", variant="primary", id="result-True"),
        ]


class ErrorDialog(BaseDialog):
    def create_buttons(self):
        return [
            Button("OK", variant="primary", id="result-None"),
        ]


class StackTraceDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        message,
        on_result=None,
        retry=False,
        content="",
    ):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            on_result=on_result,
        )
        self.retry = retry
        self.content = content

    def compose_content(self, dialog):
        dialog.native_label = Label(self.message, id="message")
        dialog.native_scroll = VerticalScroll(
            Static(self.content, id="content"),
        )
        dialog.native_content = Vertical(
            dialog.native_label,
            dialog.native_scroll,
        )

    def create_buttons(self):
        if self.retry:
            return [
                Button("Cancel", variant="error", id="result-False"),
                Button("Retry", variant="primary", id="result-True"),
            ]
        else:
            return [
                Button("OK", variant="primary", id="result-None"),
            ]

    def mount_content(self, dialog):
        dialog.native_content.styles.margin = 1
        dialog.native_content.styles.height = self.interface.window.size[1] - 18

        dialog.native_dialog.styles.width = "80%"
        dialog.native_dialog.styles.height = self.interface.window.size[1] - 10

        dialog.native_label.styles.margin = (0, 0, 1, 0)


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
        self.on_result = on_result

        interface.window.factory.not_implemented("Window.save_file_dialog()")

        self.on_result(self, None)
        self.interface.future.set_result(None)


class OpenFileDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        file_types,
        multiselect,
        on_result=None,
    ):
        super().__init__(interface=interface)
        self.on_result = on_result

        interface.window.factory.not_implemented("Window.open_file_dialog()")

        self.on_result(self, None)
        self.interface.future.set_result(None)


class SelectFolderDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        multiselect,
        on_result=None,
    ):
        super().__init__(interface=interface)
        self.on_result = on_result

        interface.window.factory.not_implemented("Window.select_folder_dialog()")

        self.on_result(self, None)
        self.interface.future.set_result(None)
