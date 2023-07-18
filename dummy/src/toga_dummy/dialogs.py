class BaseDialog:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self


class InfoDialog(BaseDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(interface)
        interface.window._impl._action(
            "info_dialog", title=title, message=message, on_result=on_result
        )


class QuestionDialog(BaseDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(interface)
        interface.window._impl._action(
            "question_dialog", title=title, message=message, on_result=on_result
        )


class ConfirmDialog(BaseDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(interface)
        interface.window._impl._action(
            "confirm_dialog", title=title, message=message, on_result=on_result
        )


class ErrorDialog(BaseDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(interface)
        interface.window._impl._action(
            "error_dialog", title=title, message=message, on_result=on_result
        )


class StackTraceDialog(BaseDialog):
    def __init__(self, interface, title, message, on_result=None, **kwargs):
        super().__init__(interface)
        interface.window._impl._action(
            "stack_trace_dialog",
            title=title,
            message=message,
            on_result=on_result,
            **kwargs
        )


class SaveFileDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        filename,
        initial_directory,
        file_types=None,
        on_result=None,
    ):
        super().__init__(interface)
        interface.window._impl._action(
            "save_file_dialog",
            title=title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=file_types,
            on_result=on_result,
        )


class OpenFileDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        file_types,
        multiselect,
        on_result=None,
    ):
        super().__init__(interface)
        interface.window._impl._action(
            "open_file_dialog",
            title=title,
            initial_directory=initial_directory,
            file_types=file_types,
            multiselect=multiselect,
            on_result=on_result,
        )


class SelectFolderDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        multiselect,
        on_result=None,
    ):
        super().__init__(interface)
        interface.window._impl._action(
            "select_folder_dialog",
            title=title,
            initial_directory=initial_directory,
            multiselect=multiselect,
            on_result=on_result,
        )
