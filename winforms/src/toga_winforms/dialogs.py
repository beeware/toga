import asyncio
from abc import ABC
from pathlib import Path

from .libs import WinFont, WinForms
from .libs.winforms import ContentAlignment, FontFamily, FontStyle, SystemFonts


class BaseDialog(ABC):
    def __init__(self, interface):
        self.interface = interface
        self.interface.impl = self


class MessageDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        message,
        buttons,
        icon,
        success_result=None,
        on_result=None,
    ):
        super().__init__(interface=interface)
        self.on_result = on_result

        return_value = WinForms.MessageBox.Show(message, title, buttons, icon)

        if success_result:
            result = return_value == success_result
        else:
            result = None

        # def completion_handler(self, return_value: bool) -> None:
        if self.on_result:
            self.on_result(self, result)

        self.interface.future.set_result(result)


class InfoDialog(MessageDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            buttons=WinForms.MessageBoxButtons.OK,
            icon=WinForms.MessageBoxIcon.Information,
            on_result=on_result,
        )


class QuestionDialog(MessageDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            buttons=WinForms.MessageBoxButtons.YesNo,
            icon=WinForms.MessageBoxIcon.Information,
            success_result=WinForms.DialogResult.Yes,
            on_result=on_result,
        )


class ConfirmDialog(MessageDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            buttons=WinForms.MessageBoxButtons.OKCancel,
            icon=WinForms.MessageBoxIcon.Warning,
            success_result=WinForms.DialogResult.OK,
            on_result=on_result,
        )


class ErrorDialog(MessageDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            buttons=WinForms.MessageBoxButtons.OK,
            icon=WinForms.MessageBoxIcon.Error,
            on_result=on_result,
        )


class StackTraceDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        message,
        content,
        retry,
        on_result=None,
        **kwargs,
    ):
        super().__init__(interface=interface)
        self.on_result = on_result

        self.native = WinForms.Form()
        self.native.MinimizeBox = False
        self.native.FormBorderStyle = self.native.FormBorderStyle.FixedSingle
        self.native.MaximizeBox = False
        self.native.FormClosing += self.winforms_FormClosing
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
            retry.Text = "Retry"
            retry.Click += self.winforms_Click_retry

            self.native.Controls.Add(retry)

            quit = WinForms.Button()
            quit.Left = 400
            quit.Top = 250
            quit.Width = 100
            quit.Text = "Quit"
            quit.Click += self.winforms_Click_quit

            self.native.Controls.Add(quit)
        else:
            accept = WinForms.Button()
            accept.Left = 400
            accept.Top = 250
            accept.Width = 100
            accept.Text = "Ok"
            accept.Click += self.winforms_Click_accept

            self.native.Controls.Add(accept)

        self.native.ShowDialog()

    def winforms_FormClosing(self, sender, event):
        # If the close button is pressed, there won't be a future yet.
        # We cancel this event to prevent the dialog from closing.
        # If a button is pressed, the future will be set, and a close
        # event will be triggered.
        try:
            self.interface.future.result()
        except asyncio.InvalidStateError:
            event.Cancel = True

    def handle_result(self, result):
        self.on_result(self, result)

        self.interface.future.set_result(result)

        self.native.Close()

    def winforms_Click_quit(self, sender, event):
        self.handle_result(False)

    def winforms_Click_retry(self, sender, event):
        self.handle_result(True)

    def winforms_Click_accept(self, sender, event):
        self.handle_result(None)


class FileDialog(BaseDialog):
    def __init__(
        self,
        native,
        interface,
        title,
        filename,
        initial_directory,
        file_types,
        multiselect,
        on_result=None,
    ):
        super().__init__(interface=interface)
        self.on_result = on_result

        native.Title = title

        if filename is not None:
            native.FileName = filename

        if initial_directory is not None:
            self._set_initial_directory(native, str(initial_directory))

        if file_types is not None:
            filters = [f"{ext} files (*.{ext})|*.{ext}" for ext in file_types] + [
                "All files (*.*)|*.*"
            ]

            if len(file_types) > 1:
                pattern = ";".join([f"*.{ext}" for ext in file_types])
                filters.insert(0, f"All matching files ({pattern})|{pattern}")

            native.Filter = "|".join(filters)

        if multiselect:
            native.Multiselect = True

        response = native.ShowDialog()

        if response == WinForms.DialogResult.OK:
            result = self._get_filenames(native, multiselect)
        else:
            result = None

        self.on_result(self, result)

        self.interface.future.set_result(result)

    @classmethod
    def _get_filenames(cls, native, multiselect):
        if multiselect:
            return [Path(filename) for filename in native.FileNames]
        else:
            return Path(native.FileName)

    @classmethod
    def _set_initial_directory(cls, native, initial_directory):
        """Set the initial directory of the given dialog.

        On Windows, not all file/folder dialogs work the same way,
        so this method is overridden when a subclass needs to
        set the initial directory in some other fashion.

        Args:
            native (WinForms.CommonDialog): the dialog to set the
                initial directory on.
            initial_directory (str): the path of the initial directory.
        """
        native.InitialDirectory = initial_directory


class SaveFileDialog(FileDialog):
    def __init__(
        self,
        interface,
        title,
        filename,
        initial_directory,
        file_types=None,
        on_result=None,
    ):
        super().__init__(
            native=WinForms.SaveFileDialog(),
            interface=interface,
            title=title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=file_types,
            multiselect=False,
            on_result=on_result,
        )


class OpenFileDialog(FileDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        file_types,
        multiselect,
        on_result=None,
    ):
        super().__init__(
            native=WinForms.OpenFileDialog(),
            interface=interface,
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=file_types,
            multiselect=multiselect,
            on_result=on_result,
        )


class SelectFolderDialog(FileDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        multiselect,
        on_result=None,
    ):
        super().__init__(
            native=WinForms.FolderBrowserDialog(),
            interface=interface,
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=None,
            multiselect=multiselect,
            on_result=on_result,
        )

    @classmethod
    def _get_filenames(cls, native, multiselect):
        filename = Path(native.SelectedPath)
        return [filename] if multiselect else filename

    @classmethod
    def _set_initial_directory(cls, native, initial_directory):
        native.SelectedPath = initial_directory
