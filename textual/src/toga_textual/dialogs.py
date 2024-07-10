from pathlib import Path

from toga_textual.window import TitleBar

import toga
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, DirectoryTree, Input, Label, Static


class TextualDialog(ModalScreen[bool]):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def compose(self) -> ComposeResult:
        self.titlebar = TitleBar(self.impl.title)
        self.impl.compose_content(self)
        self.buttons = self.impl.create_buttons()
        self.button_box = Horizontal(*self.buttons)
        self.container = Vertical(
            self.titlebar,
            self.content,
            self.button_box,
            id="dialog",
        )
        yield self.container

    def on_mount(self) -> None:
        self.styles.align = ("center", "middle")

        self.container.styles.width = 50
        self.container.styles.border = ("solid", "darkgray")

        self.impl.style_content(self)

        self.button_box.styles.align = ("center", "middle")
        for button in self.buttons:
            button.styles.margin = (0, 1, 0, 1)

        self.buttons[-1].focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(self.impl.return_value(event.button.variant))

    def on_resize(self, event) -> None:
        self.impl.style_content(self)


class BaseDialog:
    def __init__(self, title, message):
        self.title = title
        self.message = message

        self.native = TextualDialog(self)

    def show(self, host_window, future):
        self.future = future

        # Add the screen for the dialog. Don't differentiate between app and window
        # modal dialogs - attack all of them to the app
        toga.App.app._impl.native.push_screen(self.native, self.on_close)

    def compose_content(self, dialog):
        dialog.content = Label(self.message, id="message")

    def style_content(self, dialog):
        dialog.content.styles.margin = 1
        dialog.content.styles.height = 5

        dialog.container.styles.height = 13

    def return_value(self, variant):
        return variant == "primary"

    def textual_close(self):
        self.native.dismiss(None)

    def on_close(self, result: bool):
        self.future.set_result(result)


class InfoDialog(BaseDialog):
    def create_buttons(self):
        return [
            Button("OK", variant="primary"),
        ]

    def return_value(self, variant):
        return None


class QuestionDialog(BaseDialog):
    def create_buttons(self):
        return [
            Button("Yes", variant="primary"),
            Button("No", variant="error"),
        ]


class ConfirmDialog(BaseDialog):
    def create_buttons(self):
        return [
            Button("Cancel", variant="error"),
            Button("OK", variant="primary"),
        ]


class ErrorDialog(BaseDialog):
    def create_buttons(self):
        return [
            Button("OK", variant="primary"),
        ]

    def return_value(self, variant):
        return None


class StackTraceDialog(BaseDialog):
    def __init__(
        self,
        title,
        message,
        retry=False,
        content="",
    ):
        super().__init__(title=title, message=message)

        self.retry = retry
        self.content = content

    def compose_content(self, dialog):
        dialog.label = Label(self.message, id="message")
        dialog.scroll = VerticalScroll(
            Static(self.content, id="content"),
        )
        dialog.content = Vertical(
            dialog.label,
            dialog.scroll,
        )

    def create_buttons(self):
        if self.retry:
            return [
                Button("Cancel", variant="error"),
                Button("Retry", variant="primary"),
            ]
        else:
            return [
                Button("OK", variant="primary"),
            ]

    def style_content(self, dialog):
        # Textual apps must have a current window, so we can style relative to that window.
        dialog.content.styles.margin = 1
        dialog.content.styles.height = toga.App.app.current_window.size[1] - 18

        dialog.container.styles.width = "80%"
        dialog.container.styles.height = toga.App.app.current_window.size[1] - 10

        dialog.label.styles.margin = (0, 0, 1, 0)

    def return_value(self, variant):
        if self.retry:
            return variant == "primary"
        else:
            return None


class ParentFolderButton(Button):
    DEFAULT_CSS = """
    ParentFolderButton {
        border: none;
        min-width: 4;
        height: 1;
        background: white 10%;
    }
    ParentFolderButton:hover {
        background: white 10%;
    }
    ParentFolderButton:focus {
        text-style: bold;
        color: white;
    }
    ParentFolderButton.-active {
        border: none;
    }
    """

    def __init__(self, dialog):
        super().__init__("..")
        self.dialog = dialog

    def on_button_pressed(self, event):
        self.dialog.native.directory_tree.path = (
            self.dialog.native.directory_tree.path.parent
        )
        event.stop()


class FilteredDirectoryTree(DirectoryTree):
    def __init__(self, dialog):
        super().__init__(dialog.initial_directory)
        self.dialog = dialog

    def filter_paths(self, paths):
        if self.dialog.filter_func:
            return [
                path
                for path in paths
                if (path.is_dir() or self.dialog.filter_func(path))
            ]
        else:
            return paths

    def on_tree_node_selected(self, event):
        self.dialog.on_select_file(event.node.data.path)


class SaveFileDialog(BaseDialog):
    def __init__(
        self,
        title,
        filename,
        initial_directory,
        file_types=None,
    ):
        super().__init__(title=title, message=None)

        self.initial_filename = filename
        self.initial_directory = initial_directory if initial_directory else Path.cwd()
        self.file_types = file_types
        if self.file_types:
            self.filter_func = lambda p: p.suffix[1:] in self.file_types
        else:
            self.filter_func = None

    def compose_content(self, dialog):
        dialog.directory_tree = FilteredDirectoryTree(self)
        dialog.parent_button = ParentFolderButton(self)
        dialog.scroll = VerticalScroll(dialog.directory_tree)
        dialog.filename_label = Label("Filename:")
        dialog.filename = Input(self.initial_filename)
        dialog.file_specifier = Horizontal(
            dialog.filename_label,
            dialog.filename,
        )
        dialog.content = Vertical(
            dialog.parent_button,
            dialog.scroll,
            dialog.file_specifier,
        )

    def create_buttons(self):
        return [
            Button("Cancel", variant="error"),
            Button("OK", variant="primary"),
        ]

    def style_content(self, dialog):
        # Textual apps must have a current window, so we can style relative to that window.
        dialog.content.styles.margin = 1
        dialog.content.styles.height = toga.App.app.current_window.size[1] - 18

        dialog.filename_label.styles.margin = (1, 0)
        dialog.scroll.styles.height = toga.App.app.current_window.size[1] - 22

        dialog.container.styles.width = "80%"
        dialog.container.styles.height = toga.App.app.current_window.size[1] - 10

    def on_select_file(self, path):
        if path.is_file():
            self.native.filename.value = path.name

    def return_value(self, variant):
        if variant == "primary":
            return (
                self.native.directory_tree.cursor_node.data.path.parent
                / self.native.filename.value
            )
        else:
            return None


class OpenFileDialog(BaseDialog):
    def __init__(
        self,
        title,
        initial_directory,
        file_types,
        multiple_select,
    ):
        super().__init__(title=title, message=None)

        self.initial_directory = initial_directory if initial_directory else Path.cwd()
        self.file_types = file_types
        if self.file_types:
            self.filter_func = lambda p: p.is_dir() or p.suffix[1:] in self.file_types
        else:
            self.filter_func = None

        self.multiple_select = multiple_select

    def compose_content(self, dialog):
        dialog.directory_tree = FilteredDirectoryTree(self)
        dialog.parent_button = ParentFolderButton(self)
        dialog.scroll = VerticalScroll(dialog.directory_tree)
        dialog.content = Vertical(
            dialog.parent_button,
            dialog.scroll,
        )

    def create_buttons(self):
        return [
            Button("Cancel", variant="error"),
            Button("OK", variant="primary", disabled=True),
        ]

    def style_content(self, dialog):
        # Textual apps must have a current window, so we can style relative to that window.
        dialog.content.styles.margin = 1
        dialog.content.styles.height = toga.App.app.current_window.size[1] - 18

        dialog.container.styles.width = "80%"
        dialog.container.styles.height = toga.App.app.current_window.size[1] - 10

    def on_select_file(self, path):
        ok_button = self.native.buttons[-1]
        if self.filter_func:
            ok_button.disabled = not self.filter_func(path)
        else:
            ok_button.disabled = not path.is_file()

    def return_value(self, variant):
        if variant == "primary":
            return self.native.directory_tree.cursor_node.data.path
        else:
            return None


class SelectFolderDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        multiple_select,
    ):
        super().__init__(
            interface=interface,
            title=title,
            message=None,
        )
        self.initial_directory = initial_directory if initial_directory else Path.cwd()
        self.filter_func = lambda path: path.is_dir()
        self.multiple_select = multiple_select

    def compose_content(self, dialog):
        dialog.directory_tree = FilteredDirectoryTree(self)
        dialog.parent_button = ParentFolderButton(self)
        dialog.scroll = VerticalScroll(dialog.directory_tree)
        dialog.content = Vertical(
            dialog.parent_button,
            dialog.scroll,
        )

    def create_buttons(self):
        return [
            Button("Cancel", variant="error"),
            Button("OK", variant="primary"),
        ]

    def style_content(self, dialog):
        # Textual apps must have a current window, so we can style relative to that window.
        dialog.content.styles.margin = 1
        dialog.content.styles.height = toga.App.app.current_window.size[1] - 19

        dialog.container.styles.width = "80%"
        dialog.container.styles.height = toga.App.app.current_window.size[1] - 10

    def on_select_file(self, path):
        ok_button = self.native.buttons[-1]
        if self.filter_func:
            ok_button.disabled = not self.filter_func(path)
        else:
            ok_button.disabled = not path.is_file()

    def return_value(self, variant):
        if variant == "primary":
            return self.native.directory_tree.cursor_node.data.path
        else:
            return None
