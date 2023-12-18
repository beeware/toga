import asyncio
from abc import ABC
from pathlib import Path

import System.Windows.Forms as WinForms
from System.Drawing import (
    ContentAlignment,
    Font as WinFont,
    FontFamily,
    FontStyle,
    SystemFonts,
)
from System.Windows.Forms import DialogResult, MessageBoxButtons, MessageBoxIcon

from .libs.wrapper import WeakrefCallable


class BaseDialog(ABC):
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

    # See libs/proactor.py
    def start_inner_loop(self, callback, *args):
        asyncio.get_event_loop().start_inner_loop(callback, *args)

    def set_result(self, result):
        self.interface.set_result(result)


class MessageDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        message,
        buttons,
        icon,
        success_result=None,
    ):
        super().__init__(interface)

        def show():
            return_value = WinForms.MessageBox.Show(message, title, buttons, icon)
            if success_result:
                self.set_result(return_value == success_result)
            else:
                self.set_result(None)

        self.start_inner_loop(show)


class InfoDialog(MessageDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface,
            title,
            message,
            MessageBoxButtons.OK,
            MessageBoxIcon.Information,
        )


class QuestionDialog(MessageDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface,
            title,
            message,
            MessageBoxButtons.YesNo,
            MessageBoxIcon.Information,
            success_result=DialogResult.Yes,
        )


class ConfirmDialog(MessageDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface,
            title,
            message,
            MessageBoxButtons.OKCancel,
            MessageBoxIcon.Warning,
            success_result=DialogResult.OK,
        )


class ErrorDialog(MessageDialog):
    def __init__(self, interface, title, message=None):
        super().__init__(
            interface,
            title,
            message,
            WinForms.MessageBoxButtons.OK,
            WinForms.MessageBoxIcon.Error,
        )


class StackTraceDialog(BaseDialog):
    def __init__(self, interface, title, message, content, retry):
        super().__init__(interface)

        self.native = WinForms.Form()
        self.native.MinimizeBox = False
        self.native.FormBorderStyle = self.native.FormBorderStyle.FixedSingle
        self.native.MaximizeBox = False
        self.native.FormClosing += WeakrefCallable(self.winforms_FormClosing)
        self.native.Width = 540
        self.native.Height = 320
        self.native.Text = title

        # The top-of-page introductory message
        textLabel = WinForms.Label()
        textLabel.Left = 10
        textLabel.Top = 10
        textLabel.Width = 520
        textLabel.Alignment = ContentAlignment.MiddleCenter
        textLabel.Text = message

        self.native.Controls.Add(textLabel)

        # A scrolling text box for the stack trace.
        trace = WinForms.RichTextBox()
        trace.Left = 10
        trace.Top = 30
        trace.Width = 504
        trace.Height = 210
        trace.Multiline = True
        trace.ReadOnly = True
        trace.Font = WinFont(
            FontFamily.GenericMonospace,
            float(SystemFonts.DefaultFont.Size),
            FontStyle.Regular,
        )
        trace.Text = content

        self.native.Controls.Add(trace)

        # Add acceptance/close buttons
        if retry:
            retry = WinForms.Button()
            retry.Left = 290
            retry.Top = 250
            retry.Width = 100
            retry.Text = "&Retry"
            retry.Click += WeakrefCallable(self.winforms_Click_retry)

            self.native.Controls.Add(retry)

            quit = WinForms.Button()
            quit.Left = 400
            quit.Top = 250
            quit.Width = 100
            quit.Text = "&Quit"
            quit.Click += WeakrefCallable(self.winforms_Click_quit)

            self.native.Controls.Add(quit)
        else:
            accept = WinForms.Button()
            accept.Left = 400
            accept.Top = 250
            accept.Width = 100
            accept.Text = "&OK"
            accept.Click += WeakrefCallable(self.winforms_Click_accept)

            self.native.Controls.Add(accept)

        self.start_inner_loop(self.native.ShowDialog)

    def winforms_FormClosing(self, sender, event):
        # If the close button is pressed, there won't be a future yet.
        # We cancel this event to prevent the dialog from closing.
        # If a button is pressed, the future will be set, and a close
        # event will be triggered.
        try:
            self.interface.future.result()
        except asyncio.InvalidStateError:  # pragma: no cover
            event.Cancel = True

    def set_result(self, result):
        super().set_result(result)
        self.native.Close()

    def winforms_Click_quit(self, sender, event):
        self.set_result(False)

    def winforms_Click_retry(self, sender, event):
        self.set_result(True)

    def winforms_Click_accept(self, sender, event):
        self.set_result(None)


class FileDialog(BaseDialog):
    def __init__(
        self,
        native,
        interface,
        title,
        initial_directory,
        *,
        filename=None,
        file_types=None,
    ):
        super().__init__(interface)
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

        def show():
            response = native.ShowDialog()
            if response == DialogResult.OK:
                self.set_result(self._get_filenames())
            else:
                self.set_result(None)

        self.start_inner_loop(show)

    def _set_title(self, title):
        self.native.Title = title

    def _set_initial_directory(self, initial_directory):
        self.native.InitialDirectory = initial_directory


class SaveFileDialog(FileDialog):
    def __init__(self, interface, title, filename, initial_directory, file_types):
        super().__init__(
            WinForms.SaveFileDialog(),
            interface,
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
        interface,
        title,
        initial_directory,
        file_types,
        multiple_select,
    ):
        super().__init__(
            WinForms.OpenFileDialog(),
            interface,
            title,
            initial_directory,
            file_types=file_types,
        )
        if multiple_select:
            self.native.Multiselect = True

    def _get_filenames(self):
        if self.native.Multiselect:
            return [Path(filename) for filename in self.native.FileNames]
        else:
            return Path(self.native.FileName)


class SelectFolderDialog(FileDialog):
    def __init__(self, interface, title, initial_directory, multiple_select):
        super().__init__(
            WinForms.FolderBrowserDialog(),
            interface,
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
