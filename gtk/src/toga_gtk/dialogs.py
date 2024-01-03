from abc import ABC
from pathlib import Path

from .libs import Gio, GLib, Gtk


class BaseDialog(ABC):
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self


class MessageDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        message,
        buttons,
        success_result=None,
        **kwargs,
    ):
        super().__init__(interface=interface)
        self.success_result = success_result

        self.native = Gtk.AlertDialog()
        self.native.set_modal(True)

        self.native.set_message(title)
        self.native.set_detail(message)
        self.native.set_buttons(buttons)
        self.native.set_default_button(0)
        self.native.set_cancel_button(-1)

        self.native.choose(
            self.interface.window._impl.native, None, self.on_choose, None
        )

        # NOTE: This is a workaround solution to get the dialog underline window
        self._dialog_window = self.interface.window._impl.native.list_toplevels()[0]
        self._buttons = buttons

        self.build_dialog(**kwargs)

    def build_dialog(self, **kwargs):
        pass

    def on_choose(self, dialog, result, *user_data):
        button_idx = self.native.choose_finish(result)

        if self.success_result is not None:
            result = button_idx == self.success_result
        else:
            result = None

        self.interface.set_result(result)


class InfoDialog(MessageDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            buttons=["Ok"],
        )


class QuestionDialog(MessageDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            buttons=["Yes", "No"],
            success_result=0,
        )


class ConfirmDialog(MessageDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            buttons=["Ok", "Cancel"],
            success_result=0,
        )


class ErrorDialog(MessageDialog):
    def __init__(self, interface, title, message):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            buttons=["Cancel"],
        )


class StackTraceDialog(MessageDialog):
    def __init__(self, interface, title, message, **kwargs):
        super().__init__(
            interface=interface,
            title=title,
            message=message,
            buttons=["Retry", "Cancel"] if kwargs.get("retry") else ["Ok"],
            success_result=0 if kwargs.get("retry") else None,
            **kwargs,
        )

    def build_dialog(self, content, **kwargs):
        container = self._dialog_window.get_message_area()

        # Create a scrolling readonly text area, in monospace font, to contain the stack trace.
        buffer = Gtk.TextBuffer()
        buffer.set_text(content)

        trace = Gtk.TextView()
        trace.set_buffer(buffer)
        trace.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        trace.set_property("editable", False)
        trace.set_property("cursor-visible", False)
        trace.set_property("monospace", True)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_width(500)
        scroll.set_min_content_height(200)
        scroll.set_overlay_scrolling(True)
        scroll.set_valign(Gtk.Align.FILL)
        scroll.set_vexpand(False)
        scroll.set_child(trace)

        container.append(scroll)
        container.set_visible(True)

        # NOTE: This is a workaround solution to recenter the dialog window position
        self._dialog_window.set_visible(False)
        self._dialog_window.set_visible(True)


class FileDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        filename,
        initial_directory,
        file_types,
        multiple_select,
    ):
        super().__init__(interface=interface)

        self.native = Gtk.FileDialog.new()
        self.native.set_modal(True)
        self.native.set_title(title)

        if filename:
            self.native.set_initial_name(filename)

        if initial_directory:
            init_dir = Gio.File.new_for_path(str(initial_directory))
            self.native.set_initial_folder(init_dir)

        if file_types:
            filter_list = Gio.ListStore.new(Gtk.FileFilter)
            for file_type in file_types:
                filter_filetype = Gtk.FileFilter()
                filter_filetype.set_name("." + file_type + " files")
                filter_filetype.add_pattern("*." + file_type)
                filter_list.append(filter_filetype)

            self.native.set_filters(filter_list)

        self.multiple_select = multiple_select

        self.build_file_dialog()

    def build_file_dialog(self):
        pass

    # Provided as a stub that can be mocked in test conditions
    def selected_path(self):
        return self.native.get_initial_name()

    # Provided as a stub that can be mocked in test conditions
    def selected_paths(self):
        return self.native.get_filenames()


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
        )

    def build_file_dialog(self, **kwargs):
        self.native.set_accept_label("Save")
        self.native.save(self.interface.window._impl.native, None, self.on_save, None)

    def on_save(self, dialog, result, *user_data):
        try:
            response = self.native.save_finish(result)
        except GLib.GError:
            response = None

        if response is not None:
            result = Path(response.get_path())
        else:
            result = None

        self.interface.set_result(result)


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
        )

    def build_file_dialog(self, **kwargs):
        self.native.set_accept_label("Open")

        if self.multiple_select:
            self.native.open_multiple(
                self.interface.window._impl.native, None, self.on_open, None
            )
        else:
            self.native.open(
                self.interface.window._impl.native, None, self.on_open, None
            )

    def on_open(self, dialog, result, *user_data):
        try:
            if self.multiple_select:
                response = self.native.open_multiple_finish(result)
            else:
                response = self.native.open_finish(result)
        except GLib.GError:
            response = None

        if response is not None:
            if self.multiple_select:
                filenames = [
                    response.get_item(pos) for pos in range(response.get_n_items())
                ]
                result = [Path(filename.get_path()) for filename in filenames]
            else:
                result = Path(response.get_path())
        else:
            result = None

        self.interface.set_result(result)


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
        )

    def build_file_dialog(self, **kwargs):
        self.native.set_accept_label("Select")

        if self.multiple_select:
            self.native.select_multiple_folders(
                self.interface.window._impl.native, None, self.on_select, None
            )
        else:
            self.native.select_folder(
                self.interface.window._impl.native, None, self.on_select, None
            )

    def on_select(self, dialog, result, *user_data):
        try:
            if self.multiple_select:
                response = self.native.select_multiple_folders_finish(result)
            else:
                response = self.native.select_folder_finish(result)
        except GLib.GError:
            response = None

        if response is not None:
            if self.multiple_select:
                filenames = [
                    response.get_item(pos) for pos in range(response.get_n_items())
                ]
                result = [Path(filename.get_path()) for filename in filenames]
            else:
                result = Path(response.get_path())
        else:
            result = None

        self.interface.set_result(result)
