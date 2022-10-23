class InfoDialog:
    def __init__(self, window, title, message, on_result=None):
        window._impl._action(
            "info_dialog", title=title, message=message, on_result=on_result
        )


class QuestionDialog:
    def __init__(self, window, title, message, on_result=None):
        window._impl._action(
            "question_dialog", title=title, message=message, on_result=on_result
        )


class ConfirmDialog:
    def __init__(self, window, title, message, on_result=None):
        window._impl._action(
            "confirm_dialog", title=title, message=message, on_result=on_result
        )


class ErrorDialog:
    def __init__(self, window, title, message, on_result=None):
        window._impl._action(
            "error_dialog", title=title, message=message, on_result=on_result
        )


class StackTraceDialog:
    def __init__(self, window, title, message, on_result=None, **kwargs):
        window._impl._action(
            "stack_trace_dialog",
            title=title,
            message=message,
            on_result=on_result,
            **kwargs
        )


class SaveFileDialog:
    def __init__(
        self, window, title, filename, initial_directory, file_types=None, on_result=None
    ):
        window._impl._action(
            "save_file_dialog",
            title=title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=file_types,
            on_result=on_result,
        )


class OpenFileDialog:
    def __init__(
        self, window, title, initial_directory, file_types, multiselect, on_result=None
    ):
        window._impl._action(
            "open_file_dialog",
            title=title,
            initial_directory=initial_directory,
            file_types=file_types,
            multiselect=multiselect,
            on_result=on_result,
        )


class SelectFolderDialog:
    def __init__(self, window, title, initial_directory, multiselect, on_result=None):
        window._impl._action(
            "select_folder_dialog",
            title=title,
            initial_directory=initial_directory,
            multiselect=multiselect,
            on_result=on_result,
        )
