import asyncio
from pathlib import Path

import System.Windows.Forms as WinForms
from System.Drawing import (
    ContentAlignment,
    Font as WinFont,
    FontFamily,
)
from System.Windows.Forms import DialogResult, MessageBoxButtons, MessageBoxIcon

from .libs.user32 import DPI_AWARENESS_CONTEXT_UNAWARE, SetThreadDpiAwarenessContext
from .libs.wrapper import WeakrefCallable


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

        # This dialog uses a fixed layout, so we create it as DPI-unaware so it will be
        # scaled by the system. "When a window is created, its DPI awareness is defined
        # as the DPI awareness of the calling thread at that time."
        # (https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-improvements-for-desktop-applications).
        self.prev_dpi_context = None
        if SetThreadDpiAwarenessContext is not None:  # pragma: no branch
            self.prev_dpi_context = SetThreadDpiAwarenessContext(
                DPI_AWARENESS_CONTEXT_UNAWARE
            )
            if not self.prev_dpi_context:  # pragma: no cover
                print("WARNING: Failed to set DPI Awareness for StackTraceDialog")

        # Changing the DPI awareness causes confusion around font sizes, so set them
        # all explicitly.
        font_size = 8.25
        message_font = WinFont(FontFamily.GenericSansSerif, font_size)
        monospace_font = WinFont(FontFamily.GenericMonospace, font_size)

        self.native = WinForms.Form()
        self.native.MinimizeBox = False
        self.native.FormBorderStyle = self.native.FormBorderStyle.FixedSingle
        self.native.MaximizeBox = False
        self.native.FormClosing += WeakrefCallable(self.winforms_FormClosing)
        self.native.Width = 540
        self.native.Height = 320
        self.native.Text = title
        self.title = title

        # The top-of-page introductory message
        textLabel = WinForms.Label()
        textLabel.Left = 10
        textLabel.Top = 10
        textLabel.Width = 520
        textLabel.Alignment = ContentAlignment.MiddleCenter
        textLabel.Text = message
        textLabel.Font = message_font
        self.native.Controls.Add(textLabel)

        # A scrolling text box for the stack trace.
        trace = WinForms.RichTextBox()
        trace.Left = 10
        trace.Top = 35
        trace.Width = 504
        trace.Height = 205
        trace.Multiline = True
        trace.ReadOnly = True
        trace.Font = monospace_font
        trace.Text = content

        self.native.Controls.Add(trace)

        # Add acceptance/close buttons
        if retry:
            retry = WinForms.Button()
            retry.Left = 290
            retry.Top = 250
            retry.Width = 100
            retry.Text = "&Retry"
            retry.Font = message_font
            retry.Click += WeakrefCallable(self.winforms_Click_retry)

            self.native.Controls.Add(retry)

            quit = WinForms.Button()
            quit.Left = 400
            quit.Top = 250
            quit.Width = 100
            quit.Text = "&Quit"
            quit.Font = message_font
            quit.Click += WeakrefCallable(self.winforms_Click_quit)

            self.native.Controls.Add(quit)
        else:
            accept = WinForms.Button()
            accept.Left = 400
            accept.Top = 250
            accept.Width = 100
            accept.Text = "&OK"
            accept.Font = message_font
            accept.Click += WeakrefCallable(self.winforms_Click_accept)

            self.native.Controls.Add(accept)

    def _show(self):
        self.native.ShowDialog()

    def winforms_FormClosing(self, sender, event):
        # If the close button is pressed, the future won't be done.
        # We cancel this event to prevent the dialog from closing.
        # If a button is pressed, the future will be set, and a close
        # event will be triggered.
        if not self.future.done():
            event.Cancel = True  # pragma: no cover
        else:
            # Reverting the DPI awareness at the end of __init__ would cause the window
            # to be DPI-aware, presumably because the window isn't actually "created"
            # until we call ShowDialog.
            #
            # This cleanup doesn't make any difference to the dialogs example, because
            # "When the window procedure for a window is called [e.g. when clicking a
            # button], the thread is automatically switched to the DPI awareness context
            # that was in use when the window was created." However, other apps may do
            # things outside of the context of a window event.
            if self.prev_dpi_context:  # pragma: no branch
                SetThreadDpiAwarenessContext(self.prev_dpi_context)

    def winforms_Click_quit(self, sender, event):
        self.future.set_result(False)
        self.native.Close()

    def winforms_Click_retry(self, sender, event):
        self.future.set_result(True)
        self.native.Close()

    def winforms_Click_accept(self, sender, event):
        self.future.set_result(None)
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
