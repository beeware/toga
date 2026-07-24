import asyncio
from pathlib import Path

import System.Windows.Forms as WinForms
from System.Drawing import (
    ContentAlignment,
    Font as WinFont,
    FontFamily,
)
from System.Windows.Forms import DialogResult, MessageBoxButtons, MessageBoxIcon

from toga.handlers import WeakrefCallable

from .libs.user32 import GetDpiForWindow

PLACEHOLDER_RESULT = object()


class BaseDialog:
    def show(self, host_window, future):
        self.future = future

        # Don't differentiate between app and window modal dialogs
        # Show the dialog using an inner loop.
        asyncio.get_event_loop().start_inner_loop(self._show)


class MessageDialog(BaseDialog):
    def __init__(
        self,
        title,
        message,
        buttons,
        icon,
        success_result=None,
    ):
        super().__init__()
        self.message = message
        self.title = title
        self.buttons = buttons
        self.icon = icon
        self.success_result = success_result

    def _show(self):
        return_value = WinForms.MessageBox.Show(
            self.message,
            self.title,
            self.buttons,
            self.icon,
        )
        if self.success_result:
            self.future.set_result(return_value == self.success_result)
        else:
            self.future.set_result(None)


class InfoDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title,
            message,
            MessageBoxButtons.OK,
            MessageBoxIcon.Information,
        )


class QuestionDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title,
            message,
            MessageBoxButtons.YesNo,
            MessageBoxIcon.Information,
            success_result=DialogResult.Yes,
        )


class ConfirmDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title,
            message,
            MessageBoxButtons.OKCancel,
            MessageBoxIcon.Warning,
            success_result=DialogResult.OK,
        )


class ErrorDialog(MessageDialog):
    def __init__(self, title, message=None):
        super().__init__(
            title,
            message,
            WinForms.MessageBoxButtons.OK,
            WinForms.MessageBoxIcon.Error,
        )


class StackTraceDialog(BaseDialog):
    def __init__(self, title, message, content, retry):
        super().__init__()

        font_size = 8.25
        message_font = WinFont(FontFamily.GenericSansSerif, font_size)
        monospace_font = WinFont(FontFamily.GenericMonospace, font_size)

        self.native = WinForms.Form()
        dpi_scale = GetDpiForWindow(int(self.native.Handle.ToString())) / 96

        self.native.MinimizeBox = False
        self.native.FormBorderStyle = self.native.FormBorderStyle.FixedSingle
        self.native.MaximizeBox = False
        self.native.FormClosed += WeakrefCallable(self.winforms_FormClosed)
        self.native.FormClosing += WeakrefCallable(self.winforms_FormClosing)
        self.native.Width = int(540 * dpi_scale)
        self.native.Height = int(320 * dpi_scale)
        self.native.Text = title
        self.title = title

        # The top-of-page introductory message
        textLabel = WinForms.Label()
        textLabel.Left = int(10 * dpi_scale)
        textLabel.Top = int(10 * dpi_scale)
        textLabel.Width = int(520 * dpi_scale)
        textLabel.Alignment = ContentAlignment.MiddleCenter
        textLabel.Text = message
        textLabel.Font = message_font
        self.native.Controls.Add(textLabel)

        # A scrolling text box for the stack trace.
        trace = WinForms.RichTextBox()
        trace.Left = int(10 * dpi_scale)
        trace.Top = int(35 * dpi_scale)
        trace.Width = int(504 * dpi_scale)
        trace.Height = int(205 * dpi_scale)
        trace.Multiline = True
        trace.ReadOnly = True
        trace.Font = monospace_font
        trace.Text = content
        self.result = PLACEHOLDER_RESULT

        self.native.Controls.Add(trace)

        # Add acceptance/close buttons
        if retry:
            retry_button = WinForms.Button()
            retry_button.Left = int(290 * dpi_scale)
            retry_button.Top = int(250 * dpi_scale)
            retry_button.Width = int(100 * dpi_scale)
            retry_button.Height = int(retry_button.PreferredSize.Height * dpi_scale)
            retry_button.Text = "&Retry"
            retry_button.Font = message_font
            retry_button.Click += WeakrefCallable(self.winforms_Click_retry)

            self.native.Controls.Add(retry_button)

            quit_button = WinForms.Button()
            quit_button.Left = int(400 * dpi_scale)
            quit_button.Top = int(250 * dpi_scale)
            quit_button.Width = int(100 * dpi_scale)
            quit_button.Height = int(quit_button.PreferredSize.Height * dpi_scale)
            quit_button.Text = "&Quit"
            quit_button.Font = message_font
            quit_button.Click += WeakrefCallable(self.winforms_Click_quit)

            self.native.Controls.Add(quit_button)
        else:
            accept_button = WinForms.Button()
            accept_button.Left = int(400 * dpi_scale)
            accept_button.Top = int(250 * dpi_scale)
            accept_button.Width = int(100 * dpi_scale)
            accept_button.Height = int(accept_button.PreferredSize.Height * dpi_scale)
            accept_button.Text = "&OK"
            accept_button.Font = message_font
            accept_button.Click += WeakrefCallable(self.winforms_Click_accept)

            self.native.Controls.Add(accept_button)

    def _show(self):
        self.native.ShowDialog()

    def winforms_FormClosed(self, sender, event):
        # Set the result of the future after exit to prevent it being set too early.
        self.future.set_result(self.result)

    def winforms_FormClosing(self, sender, event):
        # If the close button is pressed, the future won't be done.
        # We cancel this event to prevent the dialog from closing.
        # If a button is pressed, the future will be set, and a close
        # event will be triggered.
        if self.result == PLACEHOLDER_RESULT:
            event.Cancel = True  # pragma: no cover

    def winforms_Click_quit(self, sender, event):
        self.result = False
        self.native.Close()

    def winforms_Click_retry(self, sender, event):
        self.result = True
        self.native.Close()

    def winforms_Click_accept(self, sender, event):
        self.result = None
        self.native.Close()


class FileDialog(BaseDialog):
    def __init__(
        self,
        native,
        title,
        initial_directory,
        *,
        filename=None,
        file_types=None,
    ):
        super().__init__()
        self.title = title
        self.native = native

        self._set_title(title)
        if filename is not None:
            native.FileName = filename

        if initial_directory is not None:
            self._set_initial_directory(str(initial_directory))

        if file_types is not None:
            filters = [f"{ext} files (*.{ext})|*.{ext}" for ext in file_types] + [
                "All files (*.*)|*.*"
            ]

            if len(file_types) > 1:
                pattern = ";".join([f"*.{ext}" for ext in file_types])
                filters.insert(0, f"All matching files ({pattern})|{pattern}")

            native.Filter = "|".join(filters)

    def _show(self):
        response = self.native.ShowDialog()
        if response == DialogResult.OK:
            self.future.set_result(self._get_filenames())
        else:
            self.future.set_result(None)

    def _set_title(self, title):
        self.native.Title = title

    def _set_initial_directory(self, initial_directory):
        self.native.InitialDirectory = initial_directory


class SaveFileDialog(FileDialog):
    def __init__(self, title, filename, initial_directory, file_types):
        super().__init__(
            WinForms.SaveFileDialog(),
            title,
            initial_directory,
            filename=filename,
            file_types=file_types,
        )

    def _get_filenames(self):
        return Path(self.native.FileName)


class OpenFileDialog(FileDialog):
    def __init__(
        self,
        title,
        initial_directory,
        file_types,
        multiple_select,
    ):
        super().__init__(
            WinForms.OpenFileDialog(),
            title,
            initial_directory,
            file_types=file_types,
        )
        if multiple_select:
            self.native.Multiselect = True

    # Provided as a stub that can be mocked in test conditions
    def selected_paths(self):
        return self.native.FileNames

    def _get_filenames(self):
        if self.native.Multiselect:
            return [Path(filename) for filename in self.selected_paths()]
        else:
            return Path(self.native.FileName)


class SelectFolderDialog(FileDialog):
    def __init__(self, title, initial_directory, multiple_select):
        super().__init__(
            WinForms.FolderBrowserDialog(),
            title,
            initial_directory,
        )

        # The native dialog doesn't support multiple selection, so the only effect
        # this has is to change whether we return a list.
        self.multiple_select = multiple_select

    def _get_filenames(self):
        filename = Path(self.native.SelectedPath)
        return [filename] if self.multiple_select else filename

    def _set_title(self, title):
        self.native.Description = title

    def _set_initial_directory(self, initial_directory):
        self.native.SelectedPath = initial_directory
