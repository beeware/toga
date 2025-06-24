from pathlib import Path

import toga
from toga_dummy.utils import (
    assert_action_performed_with,
)


def test_info_dialog(app):
    """An info dialog can be shown."""
    # Prime the user's response
    app._impl.dialog_responses["InfoDialog"] = [None]

    dialog = toga.InfoDialog("Title", "Body")

    assert app._impl.loop.run_until_complete(app.dialog(dialog)) is None

    assert_action_performed_with(
        dialog,
        "create InfoDialog",
        title="Title",
        message="Body",
    )
    assert_action_performed_with(
        app,
        "show app InfoDialog",
    )


def test_question_dialog(app):
    """A question dialog can be shown."""
    # Prime the user's response
    app._impl.dialog_responses["QuestionDialog"] = [True]

    dialog = toga.QuestionDialog("Title", "Body")

    assert app._impl.loop.run_until_complete(app.dialog(dialog))

    assert_action_performed_with(
        dialog,
        "create QuestionDialog",
        title="Title",
        message="Body",
    )
    assert_action_performed_with(
        app,
        "show app QuestionDialog",
    )


def test_confirm_dialog(app):
    """A confirm dialog can be shown."""
    # Prime the user's response
    app._impl.dialog_responses["ConfirmDialog"] = [True]

    dialog = toga.ConfirmDialog("Title", "Body")

    assert app._impl.loop.run_until_complete(app.dialog(dialog))

    assert_action_performed_with(
        dialog,
        "create ConfirmDialog",
        title="Title",
        message="Body",
    )
    assert_action_performed_with(
        app,
        "show app ConfirmDialog",
    )


def test_error_dialog(app):
    """An error dialog can be shown."""
    # Prime the user's response
    app._impl.dialog_responses["ErrorDialog"] = [None]

    dialog = toga.ErrorDialog("Title", "Body")

    assert app._impl.loop.run_until_complete(app.dialog(dialog)) is None

    assert_action_performed_with(
        dialog,
        "create ErrorDialog",
        title="Title",
        message="Body",
    )
    assert_action_performed_with(
        app,
        "show app ErrorDialog",
    )


def test_stack_trace_dialog(app):
    """A stack trace dialog can be shown."""
    # Prime the user's response
    app._impl.dialog_responses["StackTraceDialog"] = [None]

    dialog = toga.StackTraceDialog("Title", "Body", "The error")

    assert app._impl.loop.run_until_complete(app.dialog(dialog)) is None

    assert_action_performed_with(
        dialog,
        "create StackTraceDialog",
        title="Title",
        message="Body",
        content="The error",
        retry=False,
    )
    assert_action_performed_with(
        app,
        "show app StackTraceDialog",
    )


def test_save_file_dialog(app):
    """A save file dialog can be shown."""
    # Prime the user's response
    saved_file = Path("/saved/path/filename.txt")
    app._impl.dialog_responses["SaveFileDialog"] = [saved_file]

    dialog = toga.SaveFileDialog("Title", Path("/path/to/initial_file.txt"))

    assert app._impl.loop.run_until_complete(app.dialog(dialog)) is saved_file

    assert_action_performed_with(
        dialog,
        "create SaveFileDialog",
        title="Title",
        filename="initial_file.txt",
        initial_directory=Path("/path/to"),
        file_types=None,
    )
    assert_action_performed_with(
        app,
        "show app SaveFileDialog",
    )


def test_save_file_dialog_default_directory(app):
    """If no path is provided, a save file dialog will use the default directory."""
    # Prime the user's response
    saved_file = Path("/saved/path/filename.txt")
    app._impl.dialog_responses["SaveFileDialog"] = [saved_file]

    dialog = toga.SaveFileDialog(
        "Title",
        "initial_file.txt",
        file_types=[".txt", ".pdf"],
    )

    assert app._impl.loop.run_until_complete(app.dialog(dialog)) is saved_file

    assert_action_performed_with(
        dialog,
        "create SaveFileDialog",
        title="Title",
        filename="initial_file.txt",
        initial_directory=None,
        file_types=[".txt", ".pdf"],
    )
    assert_action_performed_with(
        app,
        "show app SaveFileDialog",
    )


def test_open_file_dialog(app):
    """A open file dialog can be shown."""
    # Prime the user's response
    opened_file = Path("/opened/path/filename.txt")
    app._impl.dialog_responses["OpenFileDialog"] = [opened_file]

    dialog = toga.OpenFileDialog("Title", "/path/to/folder")

    assert app._impl.loop.run_until_complete(app.dialog(dialog)) is opened_file

    assert_action_performed_with(
        dialog,
        "create OpenFileDialog",
        title="Title",
        initial_directory=Path("/path/to/folder"),
        file_types=None,
        multiple_select=False,
    )
    assert_action_performed_with(
        app,
        "show app OpenFileDialog",
    )


def test_open_file_dialog_default_directory(app):
    """If no path is provided, a open file dialog will use the default directory."""
    # Prime the user's response
    opened_files = [
        Path("/opened/path/filename.txt"),
        Path("/opened/path/filename2.txt"),
    ]
    app._impl.dialog_responses["OpenFileDialog"] = [opened_files]

    dialog = toga.OpenFileDialog(
        "Title",
        file_types=[".txt", ".pdf"],
        multiple_select=True,
    )

    assert app._impl.loop.run_until_complete(app.dialog(dialog)) is opened_files

    assert_action_performed_with(
        dialog,
        "create OpenFileDialog",
        title="Title",
        initial_directory=None,
        file_types=[".txt", ".pdf"],
        multiple_select=True,
    )
    assert_action_performed_with(
        app,
        "show app OpenFileDialog",
    )


def test_select_folder_dialog(app):
    """A select folder dialog can be shown."""
    # Prime the user's response
    opened_folder = Path("/opened/path")
    app._impl.dialog_responses["SelectFolderDialog"] = [opened_folder]

    dialog = toga.SelectFolderDialog("Title", Path("/path/to/folder"))

    assert app._impl.loop.run_until_complete(app.dialog(dialog)) is opened_folder

    assert_action_performed_with(
        dialog,
        "create SelectFolderDialog",
        title="Title",
        initial_directory=Path("/path/to/folder"),
        multiple_select=False,
    )
    assert_action_performed_with(
        app,
        "show app SelectFolderDialog",
    )


def test_select_folder_dialog_default_directory(app):
    """If no path is provided, a select folder dialog will use the default directory."""
    # Prime the user's response
    opened_paths = [
        Path("/opened/path"),
        Path("/other/path"),
    ]
    app._impl.dialog_responses["SelectFolderDialog"] = [opened_paths]

    dialog = toga.SelectFolderDialog("Title", multiple_select=True)

    assert app._impl.loop.run_until_complete(app.dialog(dialog)) is opened_paths

    assert_action_performed_with(
        dialog,
        "create SelectFolderDialog",
        title="Title",
        initial_directory=None,
        multiple_select=True,
    )
    assert_action_performed_with(
        app,
        "show app SelectFolderDialog",
    )
