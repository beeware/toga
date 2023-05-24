from abc import ABC
from pathlib import Path

from .libs import Gtk


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
        message_type,
        buttons,
        success_result=None,
        on_result=None,
    ):
        super().__init__(interface=interface)
        self.on_result = on_result

        self.native = Gtk.MessageDialog(
            transient_for=interface.window._impl.native,
            flags=0,
            message_type=message_type,
            buttons=buttons,
            text=title,
        )
        self.native.format_secondary_text(message)

        return_value = self.native.run()
        self.native.destroy()

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
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            on_result=on_result,
        )


class QuestionDialog(MessageDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            success_result=Gtk.ResponseType.YES,
            on_result=on_result,
        )


class ConfirmDialog(MessageDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            success_result=Gtk.ResponseType.OK,
            on_result=on_result,
        )


class ErrorDialog(MessageDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CANCEL,
            on_result=on_result,
        )


class StackTraceDialog(BaseDialog):
    def __init__(self, interface, title, message, on_result=None, **kwargs):
        super().__init__(interface=interface)
        interface.window.factory.not_implemented("Window.stack_trace_dialog()")


class FileDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        filename,
        initial_directory,
        file_types,
        multiselect,
        action,
        ok_icon,
        on_result=None,
    ):
        super().__init__(interface=interface)
        self.on_result = on_result

        self.native = Gtk.FileChooserDialog(
            transient_for=interface.window._impl.native,
            title=title,
            action=action,
        )
        self.native.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.native.add_button(ok_icon, Gtk.ResponseType.OK)

        if filename:
            self.native.set_current_name(filename)

        if initial_directory:
            self.native.set_current_folder(str(initial_directory))

        if file_types:
            for file_type in file_types:
                filter_filetype = Gtk.FileFilter()
                filter_filetype.set_name("." + file_type + " files")
                filter_filetype.add_pattern("*." + file_type)
                self.native.add_filter(filter_filetype)

        if multiselect:
            self.native.set_select_multiple(True)

        response = self.native.run()

        if response == Gtk.ResponseType.OK:
            if multiselect:
                result = [Path(filename) for filename in self.native.get_filenames()]
            else:
                result = Path(self.native.get_filename())
        else:
            result = None

        self.native.destroy()

        if self.on_result:
            self.on_result(self, result)

        self.interface.future.set_result(result)


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
            interface=interface,
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
        self,
        interface,
        title,
        initial_directory,
        file_types,
        multiselect,
        on_result=None,
    ):
        super().__init__(
            interface=interface,
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
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        multiselect,
        on_result=None,
    ):
        super().__init__(
            interface=interface,
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=None,
            multiselect=multiselect,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            ok_icon=Gtk.STOCK_OPEN,
            on_result=on_result,
        )
