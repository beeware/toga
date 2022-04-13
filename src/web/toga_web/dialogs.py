class InfoDialog:
    def __init__(self, window, title, message, on_result=None):
        window.factory.not_implemented("Window.info_dialog()")


class QuestionDialog:
    def __init__(self, window, title, message, on_result=None):
        window.factory.not_implemented("Window.question_dialog()")


class ConfirmDialog:
    def __init__(self, window, title, message, on_result=None):
        window.factory.not_implemented("Window.confirm_dialog()")


class ErrorDialog:
    def __init__(self, window, title, message, on_result=None):
        window.factory.not_implemented("Window.error_dialog()")


class StackTraceDialog:
    def __init__(self, window, title, message, on_result=None, **kwargs):
        window.factory.not_implemented("Window.stack_trace_dialog()")


class SaveFileDialog:
    def __init__(
        self, window, title, filename, initial_directory, file_types=None, on_result=None
    ):
        window.factory.not_implemented("Window.save_file_dialog()")


class OpenFileDialog:
    def __init__(
        self, window, title, initial_directory, file_types, multiselect, on_result=None
    ):
        window.factory.not_implemented("Window.open_file_dialog()")


class SelectFolderDialog:
    def __init__(self, window, title, initial_directory, multiselect, on_result=None):
        window.factory.not_implemented("Window.select_folder_dialog()")
