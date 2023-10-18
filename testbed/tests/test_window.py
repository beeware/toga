import gc
import io
import re
import traceback
import weakref
from asyncio import wait_for
from importlib import import_module
from pathlib import Path
from unittest.mock import Mock

import pytest

import toga
from toga.colors import CORNFLOWERBLUE, GOLDENROD, REBECCAPURPLE
from toga.style.pack import COLUMN, Pack


def window_probe(app, window):
    module = import_module("tests_backend.window")
    return getattr(module, "WindowProbe")(app, window)


@pytest.fixture
async def second_window(second_window_kwargs):
    yield toga.Window(**second_window_kwargs)


@pytest.fixture
async def second_window_probe(app, second_window):
    second_window.show()
    probe = window_probe(app, second_window)
    await probe.wait_for_window(f"Window ({second_window.title}) has been created")
    yield probe
    if second_window in app.windows:
        second_window.close()


@pytest.fixture
async def main_window_probe(app, main_window):
    yield window_probe(app, main_window)


async def test_title(main_window, main_window_probe):
    """The title of a window can be changed"""
    original_title = main_window.title
    assert original_title == "Toga Testbed"
    await main_window_probe.wait_for_window("Window title can be retrieved")

    try:
        main_window.title = "A Different Title"
        assert main_window.title == "A Different Title"
        await main_window_probe.wait_for_window("Window title can be changed")
    finally:
        main_window.title = original_title
        assert main_window.title == "Toga Testbed"
        await main_window_probe.wait_for_window("Window title can be reverted")


# Mobile platforms have different windowing characterics, so they have different tests.
if toga.platform.current_platform in {"iOS", "android"}:
    ####################################################################################
    # Mobile platform tests
    ####################################################################################

    async def test_visibility(main_window, main_window_probe):
        """Hide and close are no-ops on mobile"""
        assert main_window.visible

        main_window.hide()
        await main_window_probe.wait_for_window("Window.hide is a no-op")
        assert main_window.visible

        main_window.close()
        await main_window_probe.wait_for_window("Window.close is a no-op")
        assert main_window.visible

    async def test_secondary_window():
        """A secondary window cannot be created"""
        with pytest.raises(
            RuntimeError,
            match=r"Secondary windows cannot be created on mobile platforms",
        ):
            toga.Window()

    async def test_move_and_resize(main_window, main_window_probe, capsys):
        """Move and resize are no-ops on mobile."""
        initial_size = main_window.size
        content_size = main_window_probe.content_size
        assert initial_size[0] > 300
        assert initial_size[1] > 500

        assert main_window.position == (0, 0)

        main_window.position = (150, 50)
        await main_window_probe.wait_for_window("Main window can't be moved")
        assert main_window.size == initial_size
        assert main_window.position == (0, 0)

        main_window.size = (200, 150)
        await main_window_probe.wait_for_window("Main window cannot be resized")
        assert main_window.size == initial_size
        assert main_window.position == (0, 0)

        try:
            orig_content = main_window.content

            box1 = toga.Box(
                style=Pack(background_color=REBECCAPURPLE, width=10, height=10)
            )
            box2 = toga.Box(style=Pack(background_color=GOLDENROD, width=10, height=20))
            main_window.content = toga.Box(
                children=[box1, box2],
                style=Pack(direction=COLUMN, background_color=CORNFLOWERBLUE),
            )
            await main_window_probe.wait_for_window("Main window content has been set")
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size

            # Alter the content width to exceed window width
            box1.style.width = 1000
            await main_window_probe.wait_for_window(
                "Content is too wide for the window"
            )
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size

            space_warning = (
                r"Warning: Window content \([\d.]+, [\d.]+\) "
                r"exceeds available space \([\d.]+, [\d.]+\)"
            )
            assert re.search(space_warning, capsys.readouterr().out)

            # Resize content to fit
            box1.style.width = 100
            await main_window_probe.wait_for_window("Content fits in window")
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size
            assert not re.search(space_warning, capsys.readouterr().out)

            # Alter the content width to exceed window height
            box1.style.height = 2000
            await main_window_probe.wait_for_window(
                "Content is too tall for the window"
            )
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size
            assert re.search(space_warning, capsys.readouterr().out)

        finally:
            main_window.content = orig_content

    async def test_full_screen(main_window, main_window_probe):
        """Window can be made full screen"""
        main_window.full_screen = True
        await main_window_probe.wait_for_window("Full screen is a no-op")

        main_window.full_screen = False
        await main_window_probe.wait_for_window("Full screen is a no-op")

else:
    ####################################################################################
    # Desktop platform tests
    ####################################################################################

    @pytest.mark.parametrize("second_window_kwargs", [{}])
    async def test_secondary_window(app, second_window, second_window_probe):
        """A secondary window can be created"""
        assert second_window.app == app
        assert second_window in app.windows

        assert second_window.title == "Toga"
        assert second_window.size == (640, 480)
        assert second_window.position == (100, 100)
        assert second_window_probe.is_resizable
        if second_window_probe.supports_closable:
            assert second_window_probe.is_closable
        if second_window_probe.supports_minimizable:
            assert second_window_probe.is_minimizable

        second_window.close()
        await second_window_probe.wait_for_window("Secondary window has been closed")

        assert second_window not in app.windows

    @pytest.mark.parametrize(
        "second_window_kwargs",
        [dict(title="Secondary Window", position=(200, 300), size=(300, 200))],
    )
    async def test_secondary_window_with_args(app, second_window, second_window_probe):
        """A secondary window can be created with a specific size and position."""
        on_close_handler = Mock(return_value=False)
        second_window.on_close = on_close_handler

        second_window.show()
        await second_window_probe.wait_for_window("Secondary window has been shown")

        assert second_window.app == app
        assert second_window in app.windows

        assert second_window.title == "Secondary Window"
        assert second_window.size == (300, 200)
        assert second_window.position == (200, 300)

        second_window_probe.close()
        await second_window_probe.wait_for_window(
            "Attempt to close second window that is rejected"
        )
        on_close_handler.assert_called_once_with(second_window)

        assert second_window in app.windows

        # Reset, and try again, this time allowing the
        on_close_handler.reset_mock()
        on_close_handler.return_value = True

        second_window_probe.close()
        await second_window_probe.wait_for_window(
            "Attempt to close second window that succeeds"
        )
        on_close_handler.assert_called_once_with(second_window)

        assert second_window not in app.windows

    async def test_secondary_window_cleanup(app_probe):
        """Memory for windows is cleaned up when windows are deleted."""
        # Create and show a window with content. We can't use the second_window fixture
        # because the fixture will retain a reference, preventing garbage collection.
        second_window = toga.Window()
        second_window.content = toga.Box()
        second_window.show()
        await app_probe.redraw("Secondary Window has been created")

        # Retain a weak reference to the window to check garbage collection
        window_ref = weakref.ref(second_window)
        impl_ref = weakref.ref(second_window._impl)

        second_window.close()
        await app_probe.redraw("Secondary window has been closed")

        # Clear the local reference to the window (which should be the last reference),
        # and force a garbage collection pass. This should cause deletion of both the
        # interface and impl of the window.
        del second_window
        gc.collect()

        # Assert that the weak references are now dead.
        assert window_ref() is None
        assert impl_ref() is None

    @pytest.mark.parametrize(
        "second_window_kwargs",
        [dict(title="Not Resizable", resizable=False, position=(200, 150))],
    )
    async def test_non_resizable(second_window, second_window_probe):
        """A non-resizable window can be created"""
        assert second_window.visible
        assert not second_window_probe.is_resizable

    @pytest.mark.parametrize(
        "second_window_kwargs",
        [dict(title="Not Closeable", closable=False, position=(200, 150))],
    )
    async def test_non_closable(second_window, second_window_probe):
        """A non-closable window can be created. Backends that don't support this
        natively should implement it by making the close button do nothing."""
        assert second_window.visible

        on_close_handler = Mock(return_value=False)
        second_window.on_close = on_close_handler

        if second_window_probe.supports_closable:
            assert not second_window_probe.is_closable

        # Do a UI close on the window
        second_window_probe.close()
        await second_window_probe.wait_for_window("Close request was ignored")
        on_close_handler.assert_not_called()
        assert second_window.visible

        # Do an explicit close on the window
        second_window.close()
        await second_window_probe.wait_for_window("Explicit close was honored")
        on_close_handler.assert_not_called()
        assert not second_window.visible

    @pytest.mark.parametrize(
        "second_window_kwargs",
        [dict(title="Not Minimizable", minimizable=False, position=(200, 150))],
    )
    async def test_non_minimizable(second_window, second_window_probe):
        """A non-minimizable window can be created"""
        if not second_window_probe.supports_minimizable:
            pytest.xfail("This backend doesn't support disabling minimization")

        assert second_window.visible
        assert not second_window_probe.is_minimizable

        second_window_probe.minimize()
        await second_window_probe.wait_for_window("Minimize request has been ignored")
        assert not second_window_probe.is_minimized

    @pytest.mark.parametrize(
        "second_window_kwargs",
        [dict(title="Secondary Window", position=(200, 150))],
    )
    async def test_visibility(app, second_window, second_window_probe):
        """Visibility of a window can be controlled"""
        assert second_window.app == app
        assert second_window in app.windows

        assert second_window.visible
        assert second_window.size == (640, 480)
        assert second_window.position == (200, 150)

        # Move the window
        second_window.position = (250, 200)

        await second_window_probe.wait_for_window("Secondary window has been moved")
        assert second_window.size == (640, 480)
        assert second_window.position == (250, 200)

        # Resize the window
        second_window.size = (300, 250)

        await second_window_probe.wait_for_window(
            "Secondary window has been resized; position has not changed"
        )

        assert second_window.size == (300, 250)
        # We can't confirm position here, because it may have changed. macOS rescales
        # windows relative to the bottom-left corner, which means the position of the
        # window has changed relative to the Toga coordinate frame.

        second_window.hide()
        await second_window_probe.wait_for_window("Secondary window has been hidden")

        assert not second_window.visible

        # Move and resize the window while offscreen
        second_window.size = (250, 200)
        second_window.position = (300, 150)

        second_window.show()
        await second_window_probe.wait_for_window(
            "Secondary window has been made visible again; window has moved"
        )

        assert second_window.visible
        assert second_window.size == (250, 200)
        if second_window_probe.supports_move_while_hidden:
            assert second_window.position == (300, 150)

        second_window_probe.minimize()
        # Delay is required to account for "genie" animations
        await second_window_probe.wait_for_window(
            "Window has been minimized",
            minimize=True,
        )

        assert second_window_probe.is_minimized

        if second_window_probe.supports_unminimize:
            second_window_probe.unminimize()
            # Delay is required to account for "genie" animations
            await second_window_probe.wait_for_window(
                "Window has been unminimized",
                minimize=True,
            )

            assert not second_window_probe.is_minimized

        second_window_probe.close()
        await second_window_probe.wait_for_window("Secondary window has been closed")

        assert second_window not in app.windows

    @pytest.mark.parametrize(
        "second_window_kwargs",
        [dict(title="Secondary Window", position=(200, 150))],
    )
    async def test_move_and_resize(second_window, second_window_probe):
        """A window can be moved and resized."""

        # Determine the extra width consumed by window chrome (e.g., title bars, borders etc)
        extra_width = second_window.size[0] - second_window_probe.content_size[0]
        extra_height = second_window.size[1] - second_window_probe.content_size[1]

        second_window.position = (150, 50)
        await second_window_probe.wait_for_window("Secondary window has been moved")
        assert second_window.position == (150, 50)

        second_window.size = (200, 150)
        await second_window_probe.wait_for_window("Secondary window has been resized")
        assert second_window.size == (200, 150)
        assert second_window_probe.content_size == (
            200 - extra_width,
            150 - extra_height,
        )

        box1 = toga.Box(style=Pack(background_color=REBECCAPURPLE, width=10, height=10))
        box2 = toga.Box(style=Pack(background_color=GOLDENROD, width=10, height=200))
        second_window.content = toga.Box(
            children=[box1, box2],
            style=Pack(direction=COLUMN, background_color=CORNFLOWERBLUE),
        )
        await second_window_probe.wait_for_window(
            "Secondary window has had height adjusted due to content"
        )
        assert second_window.size == (200, 210 + extra_height)
        assert second_window_probe.content_size == (200 - extra_width, 210)

        # Alter the content width to exceed window size
        box1.style.width = 250
        await second_window_probe.wait_for_window(
            "Secondary window has had width adjusted due to content"
        )
        assert second_window.size == (250 + extra_width, 210 + extra_height)
        assert second_window_probe.content_size == (250, 210)

        # Try to resize to a size less than the content size
        second_window.size = (200, 150)
        await second_window_probe.wait_for_window(
            "Secondary window forced resize fails"
        )
        assert second_window.size == (250 + extra_width, 210 + extra_height)
        assert second_window_probe.content_size == (250, 210)

    @pytest.mark.parametrize(
        "second_window_kwargs",
        [dict(title="Secondary Window", position=(200, 150))],
    )
    async def test_full_screen(second_window, second_window_probe):
        """Window can be made full screen"""
        assert not second_window_probe.is_full_screen
        assert second_window_probe.is_resizable
        initial_content_size = second_window_probe.content_size

        second_window.full_screen = True
        # A longer delay to allow for genie animations
        await second_window_probe.wait_for_window(
            "Secondary window is full screen",
            full_screen=True,
        )
        assert second_window_probe.is_full_screen
        assert second_window_probe.content_size[0] > initial_content_size[0]
        assert second_window_probe.content_size[1] > initial_content_size[1]

        second_window.full_screen = True
        await second_window_probe.wait_for_window(
            "Secondary window is still full screen"
        )
        assert second_window_probe.is_full_screen
        assert second_window_probe.content_size[0] > initial_content_size[0]
        assert second_window_probe.content_size[1] > initial_content_size[1]

        second_window.full_screen = False
        # A longer delay to allow for genie animations
        await second_window_probe.wait_for_window(
            "Secondary window is not full screen",
            full_screen=True,
        )
        assert not second_window_probe.is_full_screen
        assert second_window_probe.is_resizable
        assert second_window_probe.content_size == initial_content_size

        second_window.full_screen = False
        await second_window_probe.wait_for_window(
            "Secondary window is still not full screen"
        )
        assert not second_window_probe.is_full_screen
        assert second_window_probe.content_size == initial_content_size


########################################################################################
# Dialog tests
########################################################################################


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
