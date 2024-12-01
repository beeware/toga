import toga

from .utils import LoggedObject


class BaseDialog(LoggedObject):
    def show(self, host_window, future):
        self.future = future

        try:
            if host_window:
                host_window._impl._action(f"show window {self.__class__.__name__}")
                result = host_window._impl.dialog_responses[
                    self.__class__.__name__
                ].pop(0)
            else:
                toga.App.app._impl._action(f"show app {self.__class__.__name__}")
                result = toga.App.app._impl.dialog_responses[
                    self.__class__.__name__
                ].pop(0)

        except KeyError:
            raise RuntimeError(
                f"Was not expecting responses for {self.__class__.__name__}"
            )
        except IndexError:
            raise RuntimeError(
                f"Ran out of prepared responses for {self.__class__.__name__}"
            )

        self.future.set_result(result)


class InfoDialog(BaseDialog):
    def __init__(self, title, message):
        self._action(
            "create InfoDialog",
            title=title,
            message=message,
        )


class QuestionDialog(BaseDialog):
    def __init__(self, title, message):
        self._action(
            "create QuestionDialog",
            title=title,
            message=message,
        )


class ConfirmDialog(BaseDialog):
    def __init__(self, title, message):
        self._action(
            "create ConfirmDialog",
            title=title,
            message=message,
        )


class ErrorDialog(BaseDialog):
    def __init__(self, title, message):
        self._action(
            "create ErrorDialog",
            title=title,
            message=message,
        )


class StackTraceDialog(BaseDialog):
    def __init__(self, title, message, content, retry):
        self._action(
            "create StackTraceDialog",
            title=title,
            message=message,
            content=content,
            retry=retry,
        )


class SaveFileDialog(BaseDialog):
    def __init__(
        self,
        title,
        filename,
        initial_directory,
        file_types=None,
    ):
        self._action(
            "create SaveFileDialog",
            title=title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=file_types,
        )


class OpenFileDialog(BaseDialog):
    def __init__(
        self,
        title,
        initial_directory,
        file_types,
        multiple_select,
    ):
        self._action(
            "create OpenFileDialog",
            title=title,
            initial_directory=initial_directory,
            file_types=file_types,
            multiple_select=multiple_select,
        )


class SelectFolderDialog(BaseDialog):
    def __init__(
        self,
        title,
        initial_directory,
        multiple_select,
    ):
        self._action(
            "create SelectFolderDialog",
            title=title,
            initial_directory=initial_directory,
            multiple_select=multiple_select,
        )
