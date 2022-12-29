import asyncio
from pathlib import Path

from .libs import Gtk


class BaseDialog:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.future = loop.create_future()

    def __eq__(self, other):
        raise RuntimeError(
            "Can't check dialog result directly; use await or an on_result handler"
        )

    def __bool__(self):
        raise RuntimeError(
            "Can't check dialog result directly; use await or an on_result handler"
        )

    def __await__(self):
        return self.future.__await__()


class MessageDialog(BaseDialog):
    def __init__(
        self,
        window,
        title,
        message,
        message_type,
        buttons,
        success_result=None,
        on_result=None,
    ):
        super().__init__()
        self.on_result = on_result

        dialog = Gtk.MessageDialog(
            transient_for=window._impl.native,
            flags=0,
            message_type=message_type,
            buttons=buttons,
            text=title,
        )
        dialog.format_secondary_text(message)

        return_value = dialog.run()
        dialog.destroy()

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
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            on_result=on_result,
        )


class QuestionDialog(MessageDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            success_result=Gtk.ResponseType.YES,
            on_result=on_result,
        )


class ConfirmDialog(MessageDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            success_result=Gtk.ResponseType.OK,
            on_result=on_result,
        )


class ErrorDialog(MessageDialog):
    def __init__(self, window, title, message, on_result=None):
        super().__init__(
            window=window,
            title=title,
            message=message,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CANCEL,
            on_result=on_result,
        )


class StackTraceDialog(BaseDialog):
    def __init__(self, window, title, message, on_result=None, **kwargs):
        super().__init__()
        window.factory.not_implemented("Window.stack_trace_dialog()")


class FileDialog(BaseDialog):
    def __init__(
        self,
        window,
        title,
        filename,
        initial_directory,
        file_types,
        multiselect,
        action,
        ok_icon,
        on_result=None,
    ):
        super().__init__()
        self.on_result = on_result

        dialog = Gtk.FileChooserDialog(
            transient_for=window._impl.native,
            title=title,
            action=action,
        )
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(ok_icon, Gtk.ResponseType.OK)

        if filename:
            dialog.set_current_name(filename)

        if initial_directory:
            dialog.set_current_folder(str(initial_directory))

        if file_types:
            for file_type in file_types:
                filter_filetype = Gtk.FileFilter()
                filter_filetype.set_name("." + file_type + " files")
                filter_filetype.add_pattern("*." + file_type)
                dialog.add_filter(filter_filetype)

        if multiselect:
            dialog.set_select_multiple(True)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            if multiselect:
                result = [Path(filename) for filename in dialog.get_filenames()]
            else:
                result = Path(dialog.get_filename())
        else:
            result = None

        dialog.destroy()

        if self.on_result:
            self.on_result(self, result)

        self.future.set_result(result)


class SaveFileDialog(FileDialog):
    def __init__(
        self,
        window,
        title,
        filename,
        initial_directory,
        file_types=None,
        on_result=None,
    ):
        super().__init__(
            window=window,
            title=title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=file_types,
            multiselect=False,
            action=Gtk.FileChooserAction.SAVE,
            ok_icon=Gtk.STOCK_SAVE,
            on_result=on_result,
        )


class OpenFileDialog(FileDialog):
    def __init__(
        self, window, title, initial_directory, file_types, multiselect, on_result=None
    ):
        super().__init__(
            window=window,
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=file_types,
            multiselect=multiselect,
            action=Gtk.FileChooserAction.OPEN,
            ok_icon=Gtk.STOCK_OPEN,
            on_result=on_result,
        )


class SelectFolderDialog(FileDialog):
    def __init__(self, window, title, initial_directory, multiselect, on_result=None):
        super().__init__(
            window=window,
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=None,
            multiselect=multiselect,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            ok_icon=Gtk.STOCK_OPEN,
            on_result=on_result,
        )
