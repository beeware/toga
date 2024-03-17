import io
import traceback
from asyncio import wait_for
from importlib import import_module
from pathlib import Path
from unittest.mock import Mock

import pytest


def window_probe(app, window):
    module = import_module("tests_backend.window")
    return module.WindowProbe(app, window)


TESTS_DIR = Path(__file__).parent


async def assert_dialog_result(window, dialog, on_result, expected):
    actual = await wait_for(dialog, timeout=1)
    if callable(expected):
        assert expected(actual)
    else:
        assert actual == expected

    on_result.assert_called_once_with(window, actual)


async def test_info_dialog(main_window, main_window_probe):
    """An info dialog can be displayed and acknowledged."""
    on_result_handler = Mock()
    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog_result = main_window.info_dialog(
            "Info", "Some info", on_result=on_result_handler
        )
    await main_window_probe.redraw("Info dialog displayed")
    await main_window_probe.close_info_dialog(dialog_result._impl)
    await assert_dialog_result(main_window, dialog_result, on_result_handler, None)


@pytest.mark.parametrize("result", [False, True])
async def test_question_dialog(main_window, main_window_probe, result):
    """An question dialog can be displayed and acknowledged."""
    on_result_handler = Mock()
    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog_result = main_window.question_dialog(
            "Question",
            "Some question",
            on_result=on_result_handler,
        )
    await main_window_probe.redraw("Question dialog displayed")
    await main_window_probe.close_question_dialog(dialog_result._impl, result)
    await assert_dialog_result(main_window, dialog_result, on_result_handler, result)


@pytest.mark.parametrize("result", [False, True])
async def test_confirm_dialog(main_window, main_window_probe, result):
    """A confirmation dialog can be displayed and acknowledged."""
    on_result_handler = Mock()
    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog_result = main_window.confirm_dialog(
            "Confirm",
            "Some confirmation",
            on_result=on_result_handler,
        )
    await main_window_probe.redraw("Confirmation dialog displayed")
    await main_window_probe.close_confirm_dialog(dialog_result._impl, result)
    await assert_dialog_result(main_window, dialog_result, on_result_handler, result)


async def test_error_dialog(main_window, main_window_probe):
    """An error dialog can be displayed and acknowledged."""
    on_result_handler = Mock()
    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog_result = main_window.error_dialog(
            "Error", "Some error", on_result=on_result_handler
        )
    await main_window_probe.redraw("Error dialog displayed")
    await main_window_probe.close_error_dialog(dialog_result._impl)
    await assert_dialog_result(main_window, dialog_result, on_result_handler, None)


@pytest.mark.parametrize("result", [None, False, True])
async def test_stack_trace_dialog(main_window, main_window_probe, result):
    """A confirmation dialog can be displayed and acknowledged."""
    on_result_handler = Mock()
    stack = io.StringIO()
    traceback.print_stack(file=stack)
    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog_result = main_window.stack_trace_dialog(
            "Stack Trace",
            "Some stack trace",
            stack.getvalue(),
            retry=result is not None,
            on_result=on_result_handler,
        )
    await main_window_probe.redraw(
        f"Stack trace dialog (with{'out' if result is None else ''} retry) displayed"
    )
    await main_window_probe.close_stack_trace_dialog(dialog_result._impl, result)
    await assert_dialog_result(main_window, dialog_result, on_result_handler, result)


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
):
    """A file open dialog can be displayed and acknowledged."""
    on_result_handler = Mock()
    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog_result = main_window.save_file_dialog(
            "Save file",
            suggested_filename=filename,
            file_types=file_types,
            on_result=on_result_handler,
        )
    await main_window_probe.redraw("Save File dialog displayed")
    await main_window_probe.close_save_file_dialog(dialog_result._impl, result)

    # The directory where the file dialog is opened can't be 100% predicted
    # so we need to modify the check to only inspect the filename.
    await assert_dialog_result(
        main_window,
        dialog_result,
        on_result_handler,
        None if result is None else (lambda actual: actual.name == result.name),
    )


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
        (TESTS_DIR, ["txt"], False, TESTS_DIR / "data.py"),
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
            ["txt", "doc"],
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
):
    """A file open dialog can be displayed and acknowledged."""
    on_result_handler = Mock()
    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog_result = main_window.open_file_dialog(
            "Open file",
            initial_directory=initial_directory,
            file_types=file_types,
            multiple_select=multiple_select,
            on_result=on_result_handler,
        )
    await main_window_probe.redraw("Open File dialog displayed")
    await main_window_probe.close_open_file_dialog(
        dialog_result._impl, result, multiple_select
    )
    await assert_dialog_result(main_window, dialog_result, on_result_handler, result)


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
):
    """A folder selection dialog can be displayed and acknowledged."""
    on_result_handler = Mock()
    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog_result = main_window.select_folder_dialog(
            "Select folder",
            initial_directory=initial_directory,
            multiple_select=multiple_select,
            on_result=on_result_handler,
        )
    await main_window_probe.redraw("Select Folder dialog displayed")
    await main_window_probe.close_select_folder_dialog(
        dialog_result._impl, result, multiple_select
    )

    if (
        isinstance(result, list)
        and not main_window_probe.supports_multiple_select_folder
    ):
        result = result[-1:]
    await assert_dialog_result(main_window, dialog_result, on_result_handler, result)
