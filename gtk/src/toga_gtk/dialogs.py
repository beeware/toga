from pathlib import Path

from .libs import GTK_VERSION, Gio, GLib, Gtk


class BaseDialog:
    def show(self, host_window, future):
        self.future = future
        self.native.set_transient_for(host_window._impl.native if host_window else None)
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.show()
        else:  # pragma: no-cover-if-gtk3
            self.native.present()


class MessageDialog(BaseDialog):
    def __init__(
        self,
        title,
        message_type,
        buttons,
        success_result=None,
        **kwargs,
    ):
        super().__init__()
        self.success_result = success_result
        if GTK_VERSION >= (4, 10, 0):  # pragma: no-cover-if-gtk3
            choices = {
                Gtk.ButtonsType.OK: [("OK", Gtk.ResponseType.OK)],
                Gtk.ButtonsType.CANCEL: [("Cancel", Gtk.ResponseType.CANCEL)],
                Gtk.ButtonsType.YES_NO: [
                    ("No", Gtk.ResponseType.NO),
                    ("Yes", Gtk.ResponseType.YES),
                ],
                Gtk.ButtonsType.OK_CANCEL: [
                    ("Cancel", Gtk.ResponseType.CANCEL),
                    ("OK", Gtk.ResponseType.OK),
                ],
            }[buttons]
            self.response_types = [response for _, response in choices]
            self.native = Gtk.AlertDialog(
                message=title,
                detail=kwargs["message"],
                modal=True,
                buttons=[label for label, _ in choices],
                cancel_button=0,
                default_button=len(choices) - 1,
            )
        else:
            self.native = Gtk.MessageDialog(
                message_type=message_type,
                buttons=buttons,
                text=title,
            )
            self.native.set_modal(True)
            self.build_dialog(**kwargs)
            self.native.connect("response", self.gtk_response)

    def show(self, host_window, future):
        if GTK_VERSION >= (4, 10, 0) and isinstance(
            self.native, Gtk.AlertDialog
        ):  # pragma: no-cover-if-gtk3
            self.future = future
            self.native.choose(
                host_window._impl.native if host_window else None,
                None,
                self.gtk_choose,
            )
        else:
            super().show(host_window, future)

    def gtk_choose(self, dialog, result):  # pragma: no-cover-if-gtk3
        try:
            response = self.response_types[dialog.choose_finish(result)]
        except GLib.Error as error:
            if error.matches(Gtk.DialogError.quark(), Gtk.DialogError.DISMISSED):
                response = Gtk.ResponseType.CANCEL
            else:
                self.future.set_exception(error)
                return
        self.resolve(response)

    def resolve(self, response):
        result = response == self.success_result if self.success_result else None
        self.future.set_result(result)

    def build_dialog(self, message):
        self.native.set_property("secondary-text", message)

    def gtk_response(self, dialog, response):
        self.resolve(response)
        self.native.destroy()


class InfoDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
        )


class QuestionDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            success_result=Gtk.ResponseType.YES,
        )


class ConfirmDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            success_result=Gtk.ResponseType.OK,
        )


class ErrorDialog(MessageDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CANCEL,
        )


class StackTraceDialog(MessageDialog):
    def __init__(self, title, **kwargs):
        if GTK_VERSION >= (4, 10, 0):  # pragma: no-cover-if-gtk3
            self.success_result = Gtk.ResponseType.OK if kwargs["retry"] else None
            self.native = Gtk.Window(title=title, modal=True)
            container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            for side in ("top", "bottom", "start", "end"):
                getattr(container, f"set_margin_{side}")(12)
            container.append(Gtk.Label(label=kwargs["message"], wrap=True, xalign=0))
            trace = Gtk.TextView(editable=False, cursor_visible=False, monospace=True)
            trace.get_buffer().set_text(kwargs["content"])
            trace.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
            scroll = Gtk.ScrolledWindow(child=trace)
            scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            scroll.set_size_request(500, 200)
            container.append(scroll)
            buttons = Gtk.Box(spacing=12, halign=Gtk.Align.END)
            self.response_buttons = {}
            choices = (
                [("Cancel", Gtk.ResponseType.CANCEL), ("Retry", Gtk.ResponseType.OK)]
                if kwargs["retry"]
                else [("OK", Gtk.ResponseType.OK)]
            )
            for label, response in choices:
                button = Gtk.Button(label=label)
                button.connect("clicked", self.gtk_response, response)
                buttons.append(button)
                self.response_buttons[response] = button
            container.append(buttons)
            self.native.set_child(container)
            self.native.set_default_widget(button)
            self.native.connect("close-request", self.gtk_close)
        else:
            super().__init__(
                title=title,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL
                if kwargs["retry"]
                else Gtk.ButtonsType.OK,
                success_result=Gtk.ResponseType.OK if kwargs["retry"] else None,
                **kwargs,
            )

    def gtk_close(self, window):  # pragma: no-cover-if-gtk3
        self.gtk_response(window, Gtk.ResponseType.CANCEL)
        return True

    def build_dialog(self, message, content, retry):
        container = self.native.get_message_area()

        self.native.set_property("secondary-text", message)

        # Create a scrolling readonly text area, in monospace font,
        # to contain the stack trace.
        buffer = Gtk.TextBuffer()
        buffer.set_text(content)

        trace = Gtk.TextView()
        trace.set_buffer(buffer)
        trace.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        trace.set_property("editable", False)
        trace.set_property("cursor-visible", False)

        trace.set_monospace(True)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_size_request(500, 200)
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            scroll.add(trace)
            container.pack_end(scroll, False, False, 0)
            container.show_all()
        else:  # pragma: no-cover-if-gtk3
            scroll.set_child(trace)
            container.append(scroll)

        # If this is a retry dialog, add a retry button (which maps to OK).
        if retry:
            self.native.add_button("Retry", Gtk.ResponseType.OK)


class FileDialog(BaseDialog):
    def __init__(
        self,
        title,
        filename,
        initial_directory,
        file_types,
        multiple_select,
        action,
        ok_icon,
    ):
        super().__init__()
        self.multiple_select = multiple_select
        self.operation = {
            Gtk.FileChooserAction.OPEN: "open",
            Gtk.FileChooserAction.SAVE: "save",
            Gtk.FileChooserAction.SELECT_FOLDER: "select_folder",
        }[action]
        if multiple_select:
            self.operation = (
                "open_multiple"
                if action == Gtk.FileChooserAction.OPEN
                else "select_multiple_folders"
            )
        self._selected_files = []

        if GTK_VERSION >= (4, 10, 0):  # pragma: no-cover-if-gtk3
            self.native = Gtk.FileDialog(title=title, modal=True, accept_label=ok_icon)
            if filename:
                self.native.set_initial_name(filename)
            if initial_directory:
                self.native.set_initial_folder(
                    Gio.File.new_for_path(str(initial_directory))
                )
        else:
            self.native = Gtk.FileChooserDialog(title=title, action=action)
            self.native.add_button("_Cancel", Gtk.ResponseType.CANCEL)
            self.native.add_button(ok_icon, Gtk.ResponseType.OK)
            self.native.set_modal(True)
            if filename:
                self.native.set_current_name(filename)
            if initial_directory:
                self.native.set_current_folder(
                    str(initial_directory)
                    if GTK_VERSION < (4, 0, 0)
                    else Gio.File.new_for_path(str(initial_directory))
                )
            self.native.set_select_multiple(multiple_select)
            self.native.connect("response", self.gtk_response)

        filters = []
        if file_types:
            if len(file_types) > 1:
                combined = Gtk.FileFilter()
                combined.set_name(" or ".join(f".{ft}" for ft in file_types) + " files")
                for file_type in file_types:
                    combined.add_pattern(f"*.{file_type}")
                filters.append(combined)
            for file_type in file_types:
                file_filter = Gtk.FileFilter()
                file_filter.set_name(f".{file_type} files")
                file_filter.add_pattern(f"*.{file_type}")
                filters.append(file_filter)
        if GTK_VERSION >= (4, 10, 0):  # pragma: no-cover-if-gtk3
            model = Gio.ListStore.new(Gtk.FileFilter)
            for file_filter in filters:
                model.append(file_filter)
            self.native.set_filters(model)
        else:
            for file_filter in filters:
                self.native.add_filter(file_filter)

    def show(self, host_window, future):
        self.future = future
        parent = host_window._impl.native if host_window else None
        if GTK_VERSION >= (4, 10, 0):  # pragma: no-cover-if-gtk3
            getattr(self.native, self.operation)(parent, None, self.gtk_file_response)
        else:
            self.native.set_transient_for(parent)
            self.native.show()

    def gtk_file_response(self, dialog, result):  # pragma: no-cover-if-gtk3
        try:
            files = getattr(dialog, f"{self.operation}_finish")(result)
        except GLib.Error as error:
            if error.matches(
                Gtk.DialogError.quark(), Gtk.DialogError.DISMISSED
            ) or error.matches(Gtk.DialogError.quark(), Gtk.DialogError.CANCELLED):
                self.gtk_response(dialog, Gtk.ResponseType.CANCEL)
            else:
                self.future.set_exception(error)
        else:
            self._selected_files = list(files) if self.multiple_select else [files]
            self.gtk_response(dialog, Gtk.ResponseType.OK)

    # Provided as a stub that can be mocked in test conditions
    def selected_path(self):
        if GTK_VERSION >= (4, 10, 0):  # pragma: no-cover-if-gtk3
            return self._selected_files[0].get_path()
        elif GTK_VERSION >= (4, 0, 0):  # pragma: no-cover-if-gtk3
            return self.native.get_file().get_path()
        return self.native.get_filename()

    # Provided as a stub that can be mocked in test conditions
    def selected_paths(self):
        if GTK_VERSION >= (4, 10, 0):  # pragma: no-cover-if-gtk3
            return [file.get_path() for file in self._selected_files]
        elif GTK_VERSION >= (4, 0, 0):  # pragma: no-cover-if-gtk3
            return [file.get_path() for file in self.native.get_files()]
        return self.native.get_filenames()

    def gtk_response(self, dialog, response):
        if response in (Gtk.ResponseType.OK, Gtk.ResponseType.ACCEPT):
            if self.multiple_select:
                result = [Path(filename) for filename in self.selected_paths()]
            else:
                result = Path(self.selected_path())
        else:
            result = None

        self.future.set_result(result)
        if GTK_VERSION < (4, 10, 0):  # pragma: no-cover-if-gtk4
            self.native.destroy()
        else:  # pragma: no-cover-if-gtk3
            # Gtk.FileDialog closes its chooser before invoking the callback.
            pass


class SaveFileDialog(FileDialog):
    def __init__(
        self,
        title,
        filename,
        initial_directory,
        file_types=None,
    ):
        save_icon = "_Save"
        super().__init__(
            title=title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=file_types,
            multiple_select=False,
            action=Gtk.FileChooserAction.SAVE,
            ok_icon=save_icon,
        )
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.set_do_overwrite_confirmation(True)
        else:  # pragma: no-cover-if-gtk3
            pass


class OpenFileDialog(FileDialog):
    def __init__(
        self,
        title,
        initial_directory,
        file_types,
        multiple_select,
    ):
        open_icon = "_OK"
        super().__init__(
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=file_types,
            multiple_select=multiple_select,
            action=Gtk.FileChooserAction.OPEN,
            ok_icon=open_icon,
        )


class SelectFolderDialog(FileDialog):
    def __init__(
        self,
        title,
        initial_directory,
        multiple_select,
    ):
        open_icon = "_Open"
        super().__init__(
            title=title,
            filename=None,
            initial_directory=initial_directory,
            file_types=None,
            multiple_select=multiple_select,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            ok_icon=open_icon,
        )
