from pathlib import Path

import toga
from toga_dummy.utils import (
    assert_action_performed_with,
)


def test_info_dialog(window, app):
    """An info dialog can be shown."""
    # Prime the user's response
    window._impl.dialog_responses["InfoDialog"] = [None]

    dialog = toga.InfoDialog("Title", "Body")

    assert app._impl.loop.run_until_complete(window.dialog(dialog)) is None

    assert_action_performed_with(
        dialog,
        "create InfoDialog",
        title="Title",
        message="Body",
    )
    assert_action_performed_with(
        window,
        "show window InfoDialog",
    )


def test_question_dialog(window, app):
    """A question dialog can be shown."""
    # Prime the user's response
    window._impl.dialog_responses["QuestionDialog"] = [True]

    dialog = toga.QuestionDialog("Title", "Body")

    assert app._impl.loop.run_until_complete(window.dialog(dialog))

    assert_action_performed_with(
        dialog,
        "create QuestionDialog",
        title="Title",
        message="Body",
    )
    assert_action_performed_with(
        window,
        "show window QuestionDialog",
    )


def test_confirm_dialog(window, app):
    """A confirm dialog can be shown."""
    # Prime the user's response
    window._impl.dialog_responses["ConfirmDialog"] = [True]

    dialog = toga.ConfirmDialog("Title", "Body")

    assert app._impl.loop.run_until_complete(window.dialog(dialog))

    assert_action_performed_with(
        dialog,
        "create ConfirmDialog",
        title="Title",
        message="Body",
    )
    assert_action_performed_with(
        window,
        "show window ConfirmDialog",
    )


def test_error_dialog(window, app):
    """An error dialog can be shown."""
    # Prime the user's response
    window._impl.dialog_responses["ErrorDialog"] = [None]

    dialog = toga.ErrorDialog("Title", "Body")

    assert app._impl.loop.run_until_complete(window.dialog(dialog)) is None

    assert_action_performed_with(
        dialog,
        "create ErrorDialog",
        title="Title",
        message="Body",
    )
    assert_action_performed_with(
        window,
        "show window ErrorDialog",
    )


def test_stack_trace_dialog(window, app):
    """A stack trace dialog can be shown."""
    # Prime the user's response
    window._impl.dialog_responses["StackTraceDialog"] = [None]

    dialog = toga.StackTraceDialog("Title", "Body", "The error")

    assert app._impl.loop.run_until_complete(window.dialog(dialog)) is None

    assert_action_performed_with(
        dialog,
        "create StackTraceDialog",
        title="Title",
        message="Body",
        content="The error",
        retry=False,
    )
    assert_action_performed_with(
        window,
        "show window StackTraceDialog",
    )


def test_save_file_dialog(window, app):
    """A save file dialog can be shown."""
    # Prime the user's response
    saved_file = Path("/saved/path/filename.txt")
    window._impl.dialog_responses["SaveFileDialog"] = [saved_file]

    dialog = toga.SaveFileDialog("Title", Path("/path/to/initial_file.txt"))

    assert app._impl.loop.run_until_complete(window.dialog(dialog)) is saved_file

    assert_action_performed_with(
        dialog,
        "create SaveFileDialog",
        title="Title",
        filename="initial_file.txt",
        initial_directory=Path("/path/to"),
        file_types=None,
    )
    assert_action_performed_with(
        window,
        "show window SaveFileDialog",
    )


def test_save_file_dialog_default_directory(window, app):
    """If no path is provided, a save file dialog will use the default directory."""
    # Prime the user's response
    saved_file = Path("/saved/path/filename.txt")
    window._impl.dialog_responses["SaveFileDialog"] = [saved_file]

    dialog = toga.SaveFileDialog(
        "Title",
        "initial_file.txt",
        file_types=[".txt", ".pdf"],
    )

    assert app._impl.loop.run_until_complete(window.dialog(dialog)) is saved_file

    assert_action_performed_with(
        dialog,
        "create SaveFileDialog",
        title="Title",
        filename="initial_file.txt",
        initial_directory=None,
        file_types=[".txt", ".pdf"],
    )
    assert_action_performed_with(
        window,
        "show window SaveFileDialog",
    )


def test_open_file_dialog(window, app):
    """A open file dialog can be shown."""
    # Prime the user's response
    opened_file = Path("/opened/path/filename.txt")
    window._impl.dialog_responses["OpenFileDialog"] = [opened_file]

    dialog = toga.OpenFileDialog("Title", "/path/to/folder")

    assert app._impl.loop.run_until_complete(window.dialog(dialog)) is opened_file

    assert_action_performed_with(
        dialog,
        "create OpenFileDialog",
        title="Title",
        initial_directory=Path("/path/to/folder"),
        file_types=None,
        multiple_select=False,
    )
    assert_action_performed_with(
        window,
        "show window OpenFileDialog",
    )


def test_open_file_dialog_default_directory(window, app):
    """If no path is provided, a open file dialog will use the default directory."""
    # Prime the user's response
    opened_files = [
        Path("/opened/path/filename.txt"),
        Path("/opened/path/filename2.txt"),
    ]
    window._impl.dialog_responses["OpenFileDialog"] = [opened_files]

    dialog = toga.OpenFileDialog(
        "Title",
        file_types=[".txt", ".pdf"],
        multiple_select=True,
    )

    assert app._impl.loop.run_until_complete(window.dialog(dialog)) is opened_files

    assert_action_performed_with(
        dialog,
        "create OpenFileDialog",
        title="Title",
        initial_directory=None,
        file_types=[".txt", ".pdf"],
        multiple_select=True,
    )
    assert_action_performed_with(
        window,
        "show window OpenFileDialog",
    )


def test_select_folder_dialog(window, app):
    """A select folder dialog can be shown."""
    # Prime the user's response
    opened_folder = Path("/opened/path")
    window._impl.dialog_responses["SelectFolderDialog"] = [opened_folder]

    dialog = toga.SelectFolderDialog("Title", Path("/path/to/folder"))

    assert app._impl.loop.run_until_complete(window.dialog(dialog)) is opened_folder

    assert_action_performed_with(
        dialog,
        "create SelectFolderDialog",
        title="Title",
        initial_directory=Path("/path/to/folder"),
        multiple_select=False,
    )
    assert_action_performed_with(
        window,
        "show window SelectFolderDialog",
    )


def test_select_folder_dialog_default_directory(window, app):
    """If no path is provided, a select folder dialog will use the default directory."""
    # Prime the user's response
    opened_paths = [
        Path("/opened/path"),
        Path("/other/path"),
    ]
    window._impl.dialog_responses["SelectFolderDialog"] = [opened_paths]

    dialog = toga.SelectFolderDialog("Title", multiple_select=True)

    assert app._impl.loop.run_until_complete(window.dialog(dialog)) is opened_paths

    assert_action_performed_with(
        dialog,
        "create SelectFolderDialog",
        title="Title",
        initial_directory=None,
        multiple_select=True,
    )
    assert_action_performed_with(
        window,
        "show window SelectFolderDialog",
    )
