import asyncio
from pathlib import Path

from .libs import WinForms


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
    def __init__(self, window, title, message, on_result=None, **kwargs):
        super().__init__()
        window.factory.not_implemented("Window.stack_trace_dialog()")


class FileDialog(BaseDialog):
    def __init__(self, dialog, window, title, filename, folder, file_types, multiselect, on_result=None):
        super().__init__()
        self.on_result = on_result

        dialog.Title = title

        if filename is not None:
            dialog.FileName = str(filename)

        if folder is not None:
            dialog.InitialDirectory = str(folder)

        if file_types is not None:
            filters = [
                "{0} files (*.{0})|*.{0}".format(ext)
                for ext in file_types
            ] + [
                "All files (*.*)|*.*"
            ]

            if len(file_types) > 1:
                filters.insert(0, "All matching files ({0})|{0}".format(
                    ';'.join([
                        '*.{0}'.format(ext)
                        for ext in file_types
                    ])
                ))
            dialog.Filter = '|'.join(filters)

        if multiselect:
            dialog.Multiselect = True

        response = dialog.ShowDialog()

        if response == WinForms.DialogResult.OK:
            if multiselect:
                result = [Path(filename) for filename in dialog.FileNames]
            else:
                result = Path(dialog.FileName)
        else:
            result = None

        if self.on_result:
            self.on_result(self, result)

        self.future.set_result(result)


class SaveFileDialog(FileDialog):
    def __init__(self, window, title, suggested_filename, file_types=None, on_result=None):
        # Convert suggested filename to a path, and break it into
        # a filename,
        suggested_path = Path(suggested_filename)
        folder = suggested_path.parent
        if folder == Path('.'):
            folder = None
        filename = suggested_path.name

        super().__init__(
            dialog=WinForms.SaveFileDialog(),
            window=window,
            title=title,
            filename=filename,
            folder=folder,
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
            folder=initial_directory,
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
            folder=initial_directory,
            file_types=None,
            multiselect=multiselect,
            on_result=on_result,
        )
