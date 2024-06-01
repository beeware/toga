from abc import ABC
from pathlib import Path

from .libs import Gtk


class BaseDialog(ABC):
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self


class MessageDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        message_type,
        buttons,
        success_result=None,
        **kwargs,
    ):
        super().__init__(interface=interface)
        self.success_result = success_result

        self.native = Gtk.MessageDialog(
            transient_for=interface.window._impl.native,
            flags=0,
            message_type=message_type,
            buttons=buttons,
            text=title,
        )
        self.native.set_modal(True)
        self.build_dialog(**kwargs)

        self.native.connect("response", self.gtk_response)
        self.native.show()

    def build_dialog(self, message):
        self.native.format_secondary_text(message)

    def gtk_response(self, dialog, response):
        if self.success_result:
            result = response == self.success_result
        else:
            result = None

        self.interface.set_result(result)

        self.native.destroy()


class InfoDialog(MessageDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
        )


class QuestionDialog(MessageDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            success_result=Gtk.ResponseType.YES,
        )


class ConfirmDialog(MessageDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            success_result=Gtk.ResponseType.OK,
        )


class ErrorDialog(MessageDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CANCEL,
        )


class StackTraceDialog(MessageDialog):
    def __init__(self, interface, title, **kwargs):
        super().__init__(
            interface=interface,
            title=title,
            message_type=Gtk.MessageType.ERROR,
            buttons=(
                Gtk.ButtonsType.CANCEL if kwargs.get("retry") else Gtk.ButtonsType.OK
            ),
            success_result=Gtk.ResponseType.OK if kwargs.get("retry") else None,
            **kwargs,
        )

    def build_dialog(self, message, content, retry):
        container = self.native.get_message_area()

        self.native.format_secondary_text(message)

        # Create a scrolling readonly text area, in monospace font, to contain the stack trace.
        buffer = Gtk.TextBuffer()
        buffer.set_text(content)

        trace = Gtk.TextView()
        trace.set_buffer(buffer)
        trace.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        trace.set_property("editable", False)
        trace.set_property("cursor-visible", False)

        trace.get_style_context().add_class("toga")
        trace.get_style_context().add_class("stacktrace")
        trace.get_style_context().add_class("dialog")

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(b".toga.stacktrace {font-family: monospace;}")

        trace.get_style_context().add_provider(
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_size_request(500, 200)
        scroll.add(trace)

        container.pack_end(scroll, False, False, 0)

        container.show_all()

        # If this is a retry dialog, add a retry button (which maps to OK).
        if retry:
            self.native.add_button("Retry", Gtk.ResponseType.OK)


class FileDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        filename,
        initial_directory,
        file_types,
        multiple_select,
        action,
        ok_icon,
    ):
        super().__init__(interface=interface)

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

        self.multiple_select = multiple_select
        if self.multiple_select:
            self.native.set_select_multiple(True)

        self.native.connect("response", self.gtk_response)
        self.native.show()

    # Provided as a stub that can be mocked in test conditions
    def selected_path(self):
        return self.native.get_filename()

    # Provided as a stub that can be mocked in test conditions
    def selected_paths(self):
        return self.native.get_filenames()

    def gtk_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            if self.multiple_select:
                result = [Path(filename) for filename in self.selected_paths()]
            else:
                result = Path(self.selected_path())
        else:
            result = None

        self.interface.set_result(result)

        self.native.destroy()


class SaveFileDialog(FileDialog):
    def __init__(
        self,
        interface,
        title,
        filename,
        initial_directory,
        file_types=None,
    ):
        super().__init__(
            interface=interface,
            title=title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=file_types,
            multiple_select=False,
            action=Gtk.FileChooserAction.SAVE,
            ok_icon=Gtk.STOCK_SAVE,
        )


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
            interface=interface,
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=file_types,
            multiple_select=multiple_select,
            action=Gtk.FileChooserAction.OPEN,
            ok_icon=Gtk.STOCK_OPEN,
        )


class SelectFolderDialog(FileDialog):
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
            filename=None,
            initial_directory=initial_directory,
            file_types=None,
            multiple_select=multiple_select,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            ok_icon=Gtk.STOCK_OPEN,
        )
