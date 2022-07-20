import asyncio
from pathlib import Path

from .libs import WinFont, WinForms
from .libs.winforms import ContentAlignment, FontFamily, FontStyle, SystemFonts


class BaseDialog:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.future = loop.create_future()

    def __eq__(self, other):
        raise RuntimeError("Can't check dialog result directly; use await or an on_result handler")

    def __bool__(self):
        raise RuntimeError("Can't check dialog result directly; use await or an on_result handler")

    def __await__(self):
        return self.future.__await__()


class MessageDialog(BaseDialog):
    def __init__(self, window, title, message, buttons, icon, success_result=None, on_result=None):
        super().__init__()
        self.on_result = on_result

        return_value = WinForms.MessageBox.Show(message, title, buttons, icon)

        if success_result:
            result = return_value == success_result
        else:
            result = None

        # def completion_handler(self, return_value: bool) -> None:
        if self.on_result:
            self.on_result(self, result)

        self.future.set_result(result)


class InfoDialog(MessageDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            buttons=WinForms.MessageBoxButtons.OK,
            icon=WinForms.MessageBoxIcon.Information,
            on_result=on_result,
        )


class QuestionDialog(MessageDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            buttons=WinForms.MessageBoxButtons.YesNo,
            icon=WinForms.MessageBoxIcon.Information,
            success_result=WinForms.DialogResult.Yes,
            on_result=on_result,
        )


class ConfirmDialog(MessageDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            buttons=WinForms.MessageBoxButtons.OKCancel,
            icon=WinForms.MessageBoxIcon.Warning,
            success_result=WinForms.DialogResult.OK,
            on_result=on_result,
        )


class ErrorDialog(MessageDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            buttons=WinForms.MessageBoxButtons.OK,
            icon=WinForms.MessageBoxIcon.Error,
            on_result=on_result,
        )


class StackTraceDialog(BaseDialog):
    def __init__(self, window, title, message, content, retry, on_result=None, **kwargs):
        super().__init__()
        self.on_result = on_result

        self.dialog = WinForms.Form()
        self.dialog.MinimizeBox = False
        self.dialog.FormBorderStyle = self.dialog.FormBorderStyle.FixedSingle
        self.dialog.MaximizeBox = False
        self.dialog.FormClosing += self.winforms_FormClosing
        self.dialog.Width = 540
        self.dialog.Height = 320
        self.dialog.Text = title

        # The top-of-page introductory message
        textLabel = WinForms.Label()
        textLabel.Left = 10
        textLabel.Top = 10
        textLabel.Width = 520
        textLabel.Alignment = ContentAlignment.MiddleCenter
        textLabel.Text = message

        self.dialog.Controls.Add(textLabel)

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
            FontStyle.Regular
        )
        trace.Text = content

        self.dialog.Controls.Add(trace)

        # Add acceptance/close buttons
        if retry:
            retry = WinForms.Button()
            retry.Left = 290
            retry.Top = 250
            retry.Width = 100
            retry.Text = "Retry"
            retry.Click += self.winforms_Click_retry

            self.dialog.Controls.Add(retry)

            quit = WinForms.Button()
            quit.Left = 400
            quit.Top = 250
            quit.Width = 100
            quit.Text = "Quit"
            quit.Click += self.winforms_Click_quit

            self.dialog.Controls.Add(quit)
        else:
            accept = WinForms.Button()
            accept.Left = 400
            accept.Top = 250
            accept.Width = 100
            accept.Text = "Ok"
            accept.Click += self.winforms_Click_accept

            self.dialog.Controls.Add(accept)

        self.dialog.ShowDialog()

    def winforms_FormClosing(self, sender, event):
        # If the close button is pressed, there won't be a future yet.
        # We cancel this event to prevent the dialog from closing.
        # If a button is pressed, the future will be set, and a close
        # event will be triggered.
        try:
            self.future.result()
        except asyncio.InvalidStateError:
            event.Cancel = True

    def handle_result(self, result):
        if self.on_result:
            self.on_result(self, result)

        self.future.set_result(result)

        self.dialog.Close()

    def winforms_Click_quit(self, sender, event):
        self.handle_result(False)

    def winforms_Click_retry(self, sender, event):
        self.handle_result(True)

    def winforms_Click_accept(self, sender, event):
        self.handle_result(None)


class FileDialog(BaseDialog):
    def __init__(
        self,
        dialog,
        window,
        title,
        filename,
        initial_directory,
        file_types,
        multiselect,
        on_result=None,
    ):
        super().__init__()
        self.on_result = on_result

        dialog.Title = title

        if filename is not None:
            dialog.FileName = filename

        if initial_directory is not None:
            self._set_initial_directory(dialog, str(initial_directory))

        if file_types is not None:
            filters = [f"{ext} files (*.{ext})|*.{ext}" for ext in file_types] + ["All files (*.*)|*.*"]

            if len(file_types) > 1:
                pattern = ";".join([f"*.{ext}" for ext in file_types])
                filters.insert(0, f"All matching files ({pattern})|{pattern}")

            dialog.Filter = "|".join(filters)

        if multiselect:
            dialog.Multiselect = True

        response = dialog.ShowDialog()

        if response == WinForms.DialogResult.OK:
            result = self._get_filenames(dialog, multiselect)
        else:
            result = None

        if self.on_result:
            self.on_result(self, result)

        self.future.set_result(result)

    @classmethod
    def _get_filenames(cls, dialog, multiselect):
        if multiselect:
            return [Path(filename) for filename in dialog.FileNames]
        else:
            return Path(dialog.FileName)

    @classmethod
    def _set_initial_directory(cls, dialog, initial_directory):
        """Set the initial directory of the given dialog.

        On Windows, not all file/folder dialogs work the same way,
        so this method is overridden when a subclass needs to
        set the initial directory in some other fashion.

        Args:
            dialog (WinForms.CommonDialog): the dialog to set the
                initial directory on.
            initial_directory (str): the path of the initial directory.

        """
        dialog.InitialDirectory = initial_directory


class SaveFileDialog(FileDialog):
    def __init__(self, window, title, filename, initial_directory, file_types=None, on_result=None):
        super().__init__(
            dialog=WinForms.SaveFileDialog(),
            window=window,
            title=title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=file_types,
            multiselect=False,
            on_result=on_result,
        )


class OpenFileDialog(FileDialog):
    def __init__(self, window, title, initial_directory, file_types, multiselect, on_result=None):
        super().__init__(
            dialog=WinForms.OpenFileDialog(),
            window=window,
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=file_types,
            multiselect=multiselect,
            on_result=on_result,
        )


class SelectFolderDialog(FileDialog):
    def __init__(self, window, title, initial_directory, multiselect, on_result=None):
        super().__init__(
            dialog=WinForms.FolderBrowserDialog(),
            window=window,
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=None,
            multiselect=multiselect,
            on_result=on_result,
        )

    @classmethod
    def _get_filenames(cls, dialog, multiselect):
        filename = Path(dialog.SelectedPath)
        return [filename] if multiselect else filename

    @classmethod
    def _set_initial_directory(cls, dialog, initial_directory):
        dialog.SelectedPath = initial_directory
