import asyncio
import io
import traceback
from pathlib import Path
from time import time

import pytest

import toga

TESTS_DIR = Path(__file__).parent.parent


@pytest.fixture
async def wait_for_dialog_to_close(main_window):
    """Wait for any asyncio task that is responsible for closing the dialog.

    An automatic fixture verifies tasks are not unintentionally left stranded after
    the test; so, wait specifically for the task that closes the dialog before leaving.
    """
    yield
    tasks = [
        t for t in main_window.app._running_tasks if t.get_name() == "close-dialog"
    ]
    task = tasks[0] if tasks else None
    deadline = time() + 1.5
    while task and not task.done():
        print("Waiting for dialog to close...")
        await asyncio.sleep(0.1)
        if time() > deadline:
            print("Gave up waiting for dialog to close...")
            break


async def test_info_dialog(main_window, main_window_probe, wait_for_dialog_to_close):
    """An info dialog can be displayed and acknowledged."""
    dialog = toga.InfoDialog("Info", "Some info")
    assert main_window_probe.is_modal_dialog(dialog)

    main_window_probe.setup_info_dialog_result(dialog)

    await main_window_probe.redraw("Display window modal info dialog")
    actual = await main_window.dialog(dialog)

    assert actual is None


@pytest.mark.parametrize("result", [False, True])
async def test_question_dialog(
    main_window,
    main_window_probe,
    result,
    wait_for_dialog_to_close,
):
    """A question dialog can be displayed and acknowledged."""
    dialog = toga.QuestionDialog("Question", "Some question")
    assert main_window_probe.is_modal_dialog(dialog)

    main_window_probe.setup_question_dialog_result(dialog, result)

    await main_window_probe.redraw(
        f"Display window modal question dialog; respond {'YES' if result else 'NO'}"
    )
    actual = await main_window.dialog(dialog)

    assert actual == result


@pytest.mark.parametrize("result", [False, True])
async def test_confirm_dialog(
    main_window,
    main_window_probe,
    result,
    wait_for_dialog_to_close,
):
    """A confirmation dialog can be displayed and acknowledged."""
    dialog = toga.ConfirmDialog("Confirm", "Some confirmation")
    assert main_window_probe.is_modal_dialog(dialog)

    main_window_probe.setup_confirm_dialog_result(dialog, result)

    await main_window_probe.redraw(
        f"Display window modal confirm dialog; respond {'OK' if result else 'CANCEL'}"
    )
    actual = await main_window.dialog(dialog)

    assert actual == result


async def test_error_dialog(main_window, main_window_probe, wait_for_dialog_to_close):
    """An error dialog can be displayed and acknowledged."""
    dialog = toga.ErrorDialog("Error", "Some error")
    assert main_window_probe.is_modal_dialog(dialog)

    main_window_probe.setup_error_dialog_result(dialog)

    await main_window_probe.redraw("Display window modal error dialog")
    actual = await main_window.dialog(dialog)

    assert actual is None


@pytest.mark.parametrize("result", [None, False, True])
async def test_stack_trace_dialog(
    main_window,
    main_window_probe,
    result,
    wait_for_dialog_to_close,
):
    """A confirmation dialog can be displayed and acknowledged."""
    stack = io.StringIO()
    traceback.print_stack(file=stack)

    dialog = toga.StackTraceDialog(
        "Stack Trace",
        "Some stack trace",
        stack.getvalue(),
        retry=result is not None,
    )
    assert main_window_probe.is_modal_dialog(dialog)

    main_window_probe.setup_stack_trace_dialog_result(dialog, result)

    await main_window_probe.redraw(
        "Display window modal stack track dialog; "
        + ("no retry" if result is None else f"with retry={'YES' if result else 'NO'}")
    )
    actual = await main_window.dialog(dialog)

    assert actual == result


@pytest.mark.parametrize(
    "filename, file_types, result",
    [
        ("/path/to/file.txt", None, Path("/path/to/file.txt")),
        ("/path/to/file.txt", None, None),
        ("/path/to/file.txt", ["txt", "doc"], Path("/path/to/file.txt")),
        ("/path/to/file.txt", ["txt", "doc"], None),
    ],
)
async def test_save_file_dialog(
    main_window,
    main_window_probe,
    filename,
    file_types,
    result,
    wait_for_dialog_to_close,
):
    """A file open dialog can be displayed and acknowledged."""
    dialog = toga.SaveFileDialog(
        "Save file",
        suggested_filename=filename,
        file_types=file_types,
    )
    assert main_window_probe.is_modal_dialog(dialog)

    main_window_probe.setup_save_file_dialog_result(dialog, result)

    await main_window_probe.redraw(
        "Display window modal save file dialog"
        f"{', with' if file_types else ', without'} file types; "
        f"select {'OK' if result else 'CANCEL'}"
    )
    actual = await main_window.dialog(dialog)

    # The directory where the file dialog is opened can't be 100% predicted
    # so we need to modify the check to only inspect the filename.
    if result is None:
        assert actual is None
    else:
        assert actual.name == result.name


@pytest.mark.parametrize(
    "initial_directory, file_types, multiple_select, result",
    [
        # Successful single select
        (TESTS_DIR, None, False, TESTS_DIR / "data.py"),
        # Cancelled single select
        (TESTS_DIR, None, False, None),
        # Successful single select with no initial directory
        (None, None, False, TESTS_DIR / "data.py"),
        # Successful single select with file types
        (TESTS_DIR, ["py"], False, TESTS_DIR / "data.py"),
        # Successful multiple selection
        (
            TESTS_DIR,
            None,
            True,
            [TESTS_DIR / "conftest.py", TESTS_DIR / "data.py"],
        ),
        # Successful multiple selection of one item
        (TESTS_DIR, None, True, [TESTS_DIR / "data.py"]),
        # Cancelled multiple selection
        (TESTS_DIR, None, True, None),
        # Successful multiple selection with no initial directory
        (None, None, True, [TESTS_DIR / "conftest.py", TESTS_DIR / "data.py"]),
        # Successful multiple selection with file types
        (
            TESTS_DIR,
            ["txt", "py"],
            True,
            [TESTS_DIR / "conftest.py", TESTS_DIR / "data.py"],
        ),
    ],
)
async def test_open_file_dialog(
    main_window,
    main_window_probe,
    initial_directory,
    file_types,
    multiple_select,
    result,
    wait_for_dialog_to_close,
):
    """A file open dialog can be displayed and acknowledged."""
    dialog = toga.OpenFileDialog(
        "Open file",
        initial_directory=initial_directory,
        file_types=file_types,
        multiple_select=multiple_select,
    )
    assert main_window_probe.is_modal_dialog(dialog)

    main_window_probe.setup_open_file_dialog_result(dialog, result, multiple_select)

    await main_window_probe.redraw(
        "Display window modal"
        f"{' multiple selection' if multiple_select else ''}"
        " open file dialog"
        f"{'' if initial_directory else ', no initial directory'}"
        f"{', with' if file_types else ', no'} file types; "
        f"select {'OK' if result else 'CANCEL'}"
    )
    actual = await main_window.dialog(dialog)

    assert actual == result


@pytest.mark.parametrize(
    "initial_directory, multiple_select, result",
    [
        # Successful single select
        (TESTS_DIR, False, TESTS_DIR / "widgets"),
        # Cancelled single select
        (TESTS_DIR, False, None),
        # Successful single select with no initial directory
        (None, False, TESTS_DIR / "widgets"),
        # Successful multiple selection
        (TESTS_DIR, True, [TESTS_DIR, TESTS_DIR / "widgets"]),
        # Successful multiple selection with one item
        (TESTS_DIR, True, [TESTS_DIR / "widgets"]),
        # Cancelled multiple selection
        (TESTS_DIR, True, None),
    ],
)
async def test_select_folder_dialog(
    main_window,
    main_window_probe,
    initial_directory,
    multiple_select,
    result,
    wait_for_dialog_to_close,
):
    """A folder selection dialog can be displayed and acknowledged."""
    dialog = toga.SelectFolderDialog(
        "Select folder",
        initial_directory=initial_directory,
        multiple_select=multiple_select,
    )
    assert main_window_probe.is_modal_dialog(dialog)

    main_window_probe.setup_select_folder_dialog_result(dialog, result, multiple_select)
    await main_window_probe.redraw(
        "Display window modal"
        f"{' multiple selection' if multiple_select else ''}"
        " select folder dialog"
        f"{'' if initial_directory else ', no initial directory'}"
        f"; select {'OK' if result else 'CANCEL'}"
    )

    actual = await main_window.dialog(dialog)

    if (
        isinstance(result, list)
        and not main_window_probe.supports_multiple_select_folder
    ):
        result = result[-1:]
    assert actual == result
