import io
import traceback
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
async def main_window_probe(app, main_window):
    yield window_probe(app, main_window)


async def test_title(main_window, main_window_probe):
    """The title of a window can be changed"""
    original_title = main_window.title
    assert original_title == "Toga Testbed"
    await main_window_probe.redraw("Window title can be retrieved")

    try:
        main_window.title = "A Different Title"
        assert main_window.title == "A Different Title"
        await main_window_probe.redraw("Window title can be changed")
    finally:
        main_window.title = original_title
        assert main_window.title == "Toga Testbed"
        await main_window_probe.redraw("Window title can be reverted")


# Mobile platforms have different windowing characterics, so they have different tests.
if toga.platform.current_platform in {"iOS", "android"}:
    ####################################################################################
    # Mobile platform tests
    ####################################################################################

    async def test_visibility(main_window, main_window_probe):
        """Hide and close are no-ops on mobile"""
        assert main_window.visible

        main_window.hide()
        await main_window_probe.redraw("Window.hide is a no-op")
        assert main_window.visible

        main_window.close()
        await main_window_probe.redraw("Window.close is a no-op")
        assert main_window.visible

    async def test_secondary_window(app):
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
        await main_window_probe.redraw("Main window can't be moved")
        assert main_window.size == initial_size
        assert main_window.position == (0, 0)

        main_window.size = (200, 150)
        await main_window_probe.redraw("Main window cannot be resized")
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
            await main_window_probe.redraw("Main window content has been set")
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size

            # Alter the content width to exceed window width
            box1.style.width = 1000
            await main_window_probe.redraw("Content is too wide for the window")
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size

            assert (
                "**WARNING** Window content exceeds available space"
                in capsys.readouterr().out
            )

            # Resize content to fit
            box1.style.width = 100
            await main_window_probe.redraw("Content fits in window")
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size

            assert (
                "**WARNING** Window content exceeds available space"
                not in capsys.readouterr().out
            )

            # Alter the content width to exceed window height
            box1.style.height = 2000
            await main_window_probe.redraw("Content is too tall for the window")
            assert main_window.size == initial_size
            assert main_window_probe.content_size == content_size

            assert (
                "**WARNING** Window content exceeds available space"
                in capsys.readouterr().out
            )
        finally:
            main_window.content = orig_content

    async def test_full_screen(main_window, main_window_probe):
        """Window can be made full screen"""
        main_window.full_screen = True
        await main_window_probe.redraw("Full screen is a no-op")

        main_window.full_screen = False
        await main_window_probe.redraw("Full screen is a no-op")

else:
    ####################################################################################
    # Desktop platform tests
    ####################################################################################

    async def test_secondary_window(app):
        """A secondary window can be created"""
        new_window = toga.Window()
        probe = window_probe(app, new_window)

        new_window.show()
        await probe.redraw("New window has been shown")

        assert new_window.app == app
        assert new_window in app.windows

        assert new_window.title == "Toga"
        assert new_window.size == (640, 480)
        assert new_window.position == (100, 100)
        assert probe.is_resizable
        assert probe.is_closable
        assert probe.is_minimizable

        new_window.close()
        await probe.redraw("New window has been closed")

        assert new_window not in app.windows

    async def test_secondary_window_with_args(app):
        """A secondary window can be created with a specific size and position."""
        on_close_handler = Mock(return_value=False)

        new_window = toga.Window(
            title="New Window",
            position=(200, 300),
            size=(300, 200),
            on_close=on_close_handler,
        )
        probe = window_probe(app, new_window)

        new_window.show()
        await probe.redraw("New window has been shown")

        assert new_window.app == app
        assert new_window in app.windows

        assert new_window.title == "New Window"
        assert new_window.size == (300, 200)
        assert new_window.position == (200, 300)

        probe.close()
        await probe.redraw("Attempt to close second window that is rejected")
        on_close_handler.assert_called_once_with(new_window)

        assert new_window in app.windows

        # Reset, and try again, this time allowing the
        on_close_handler.reset_mock()
        on_close_handler.return_value = True

        probe.close()
        await probe.redraw("Attempt to close second window that succeeds")
        on_close_handler.assert_called_once_with(new_window)

        assert new_window not in app.windows

    async def test_non_resizable(app):
        """A non-resizable window can be created"""
        new_window = toga.Window(
            title="Not Resizable", resizable=False, position=(150, 150)
        )

        new_window.show()

        probe = window_probe(app, new_window)
        await probe.redraw("Non resizable window has been shown")

        assert new_window.visible
        assert not probe.is_resizable

        # Clean up
        new_window.close()

    async def test_non_closable(app):
        """A non-closable window can be created"""
        new_window = toga.Window(
            title="Not Closeable", closable=False, position=(150, 150)
        )
        new_window.show()

        probe = window_probe(app, new_window)
        await probe.redraw("Non-closable window has been shown")

        assert new_window.visible
        assert not probe.is_closable

        # Do a UI close on the window
        probe.close()
        await probe.redraw("Close request was ignored")
        assert new_window.visible

        # Do an explicit close on the window
        new_window.close()
        await probe.redraw("Explicit close was honored")

        assert not new_window.visible

    async def test_non_minimizable(app):
        """A non-minimizable window can be created"""
        new_window = toga.Window(
            title="Not Minimizable", minimizable=False, position=(150, 150)
        )
        new_window.show()

        probe = window_probe(app, new_window)
        await probe.redraw("Non-minimizable window has been shown")
        assert new_window.visible
        assert not probe.is_minimizable

        probe.minimize()
        await probe.redraw("Minimize request has been ignored")
        assert not probe.is_minimized

        # Clean up
        new_window.close()

    async def test_visibility(app):
        """Visibility of a window can be controlled"""
        new_window = toga.Window(title="New Window", position=(200, 250))
        probe = window_probe(app, new_window)

        new_window.show()
        await probe.redraw("New window has been shown")

        assert new_window.app == app
        assert new_window in app.windows

        assert new_window.visible
        assert new_window.size == (640, 480)
        assert new_window.position == (200, 250)

        new_window.hide()
        await probe.redraw("New window has been hidden")

        assert not new_window.visible

        # Move and resie the window while offscreen
        new_window.size = (250, 200)
        new_window.position = (300, 150)

        new_window.show()
        await probe.redraw("New window has been made visible again")

        assert new_window.visible
        assert new_window.size == (250, 200)
        assert new_window.position == (300, 150)

        probe.minimize()
        # Delay is required to account for "genie" animations
        await probe.redraw("Window has been minimized", delay=0.5)

        assert probe.is_minimized

        probe.unminimize()
        # Delay is required to account for "genie" animations
        await probe.redraw("Window has been unminimized", delay=0.5)

        assert not probe.is_minimized

        probe.close()
        await probe.redraw("New window has been closed")

        assert new_window not in app.windows

    async def test_move_and_resize(app):
        """A window can be moved and resized."""
        new_window = toga.Window(title="New Window")
        probe = window_probe(app, new_window)
        new_window.show()
        await probe.redraw("New window has been shown")

        # Determine the extra width consumed by window chrome (e.g., title bars, borders etc)
        extra_width = new_window.size[0] - probe.content_size[0]
        extra_height = new_window.size[1] - probe.content_size[1]

        new_window.position = (150, 50)
        await probe.redraw("New window has been moved")
        assert new_window.position == (150, 50)

        new_window.size = (200, 150)
        await probe.redraw("New window has been resized")
        assert new_window.size == (200, 150)
        assert probe.content_size == (200 - extra_width, 150 - extra_height)

        box1 = toga.Box(style=Pack(background_color=REBECCAPURPLE, width=10, height=10))
        box2 = toga.Box(style=Pack(background_color=GOLDENROD, width=10, height=200))
        new_window.content = toga.Box(
            children=[box1, box2],
            style=Pack(direction=COLUMN, background_color=CORNFLOWERBLUE),
        )
        await probe.redraw("New window has had height adjusted due to content")
        assert new_window.size == (200 + extra_width, 210 + extra_height)
        assert probe.content_size == (200, 210)

        # Alter the content width to exceed window size
        box1.style.width = 250
        await probe.redraw("New window has had width adjusted due to content")
        assert new_window.size == (250 + extra_width, 210 + extra_height)
        assert probe.content_size == (250, 210)

        # Try to resize to a size less than the content size
        new_window.size = (200, 150)
        await probe.redraw("New window forced resize fails")
        assert new_window.size == (250 + extra_width, 210 + extra_height)
        assert probe.content_size == (250, 210)

        new_window.close()

    async def test_full_screen(app):
        """Window can be made full screen"""
        new_window = toga.Window(
            title="New Window", size=(400, 300), position=(150, 150)
        )
        new_window.content = toga.Box(style=Pack(background_color=CORNFLOWERBLUE))
        probe = window_probe(app, new_window)
        new_window.show()
        await probe.redraw("New window has been shown")
        assert not probe.is_full_screen
        initial_content_size = probe.content_size

        new_window.full_screen = True
        # A short delay to allow for genie animations
        await probe.redraw("New window is full screen", delay=1)
        assert probe.is_full_screen
        assert probe.content_size[0] > initial_content_size[0]
        assert probe.content_size[1] > initial_content_size[1]

        new_window.full_screen = True
        await probe.redraw("New window is still full screen")
        assert probe.is_full_screen
        assert probe.content_size[0] > initial_content_size[0]
        assert probe.content_size[1] > initial_content_size[1]

        new_window.full_screen = False
        # A short delay to allow for genie animations
        await probe.redraw("New window is not full screen", delay=1)
        assert not probe.is_full_screen
        assert probe.content_size == initial_content_size

        new_window.full_screen = False
        await probe.redraw("New window is still not full screen")
        assert not probe.is_full_screen
        assert probe.content_size == initial_content_size

        new_window.close()


########################################################################################
# Dialog tests
########################################################################################


async def test_info_dialog(main_window, main_window_probe):
    """An info dialog can be displayed and acknowledged."""
    on_result_handler = Mock()
    dialog_result = main_window.info_dialog(
        "Info", "Some info", on_result=on_result_handler
    )
    await main_window_probe.redraw("Info dialog displayed")
    await main_window_probe.close_info_dialog(dialog_result._impl)

    on_result_handler.assert_called_once_with(main_window, None)
    assert await dialog_result is None


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

    on_result_handler.assert_called_once_with(main_window, result)
    assert await dialog_result is result


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

    on_result_handler.assert_called_once_with(main_window, result)
    assert await dialog_result is result


async def test_error_dialog(main_window, main_window_probe):
    """An error dialog can be displayed and acknowledged."""
    on_result_handler = Mock()
    dialog_result = main_window.error_dialog(
        "Error", "Some error", on_result=on_result_handler
    )
    await main_window_probe.redraw("Error dialog displayed")
    await main_window_probe.close_error_dialog(dialog_result._impl)

    on_result_handler.assert_called_once_with(main_window, None)
    assert await dialog_result is None


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

    on_result_handler.assert_called_once_with(main_window, result)
    assert await dialog_result is result


@pytest.mark.parametrize(
    "filename, file_types, result",
    [
        ("/path/to/file.txt", None, Path("/path/to/file.txt")),
        ("/path/to/file.txt", None, None),
        ("/path/to/file.txt", [".txt", ".doc"], Path("/path/to/file.txt")),
        ("/path/to/file.txt", [".txt", ".doc"], None),
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

    if result:
        # The directory where the file dialog is opened can't be 100% predicted
        # so we need to modify the check to only inspect the filename.
        on_result_handler.call_count == 1
        assert on_result_handler.mock_calls[0].args[0] == main_window
        assert on_result_handler.mock_calls[0].args[1].name == Path(filename).name
        assert (await dialog_result).name == Path(filename).name
    else:
        on_result_handler.assert_called_once_with(main_window, None)
        assert await dialog_result is None


@pytest.mark.parametrize(
    "initial_directory, file_types, multiple_select, result",
    [
        # Successful single select
        (Path(__file__).parent, None, False, Path("/path/to/file1.txt")),
        # Cancelled single select
        (Path(__file__).parent, None, False, None),
        # Successful single select with no initial directory
        (None, None, False, Path("/path/to/file1.txt")),
        # Successful single select with file types
        (Path(__file__).parent, [".txt", ".doc"], False, Path("/path/to/file1.txt")),
        # Successful multiple selection
        (
            Path(__file__).parent,
            None,
            True,
            [Path("/path/to/file1.txt"), Path("/path/to/file2.txt")],
        ),
        # Successful multiple selection of no items
        (Path(__file__).parent, None, True, []),
        # Cancelled multiple selection
        (Path(__file__).parent, None, True, None),
        # Successful multiple selection with no initial directory
        (None, None, True, [Path("/path/to/file1.txt"), Path("/path/to/file2.txt")]),
        # Successful multiple selection with file types
        (
            Path(__file__).parent,
            [".txt", ".doc"],
            True,
            [Path("/path/to/file1.txt"), Path("/path/to/file2.txt")],
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
        dialog_result._impl,
        result,
        multiple_select=multiple_select,
    )

    if result is not None:
        on_result_handler.assert_called_once_with(main_window, result)
        assert await dialog_result == result
    else:
        print(dialog_result._impl, on_result_handler, on_result_handler.mock_calls)
        on_result_handler.assert_called_once_with(main_window, None)
        assert await dialog_result is None


@pytest.mark.parametrize(
    "initial_directory, multiple_select, result",
    [
        # Successful single select
        (Path(__file__).parent, False, Path("/path/to/dir1")),
        # Cancelled single select
        (Path(__file__).parent, False, None),
        # Successful single select with no initial directory
        (None, False, Path("/path/to/dir1")),
        # Successful multiple selection
        (Path(__file__).parent, True, [Path("/path/to/dir1"), Path("/path/to/dir2")]),
        # Successful multiple selection with no items
        (Path(__file__).parent, True, []),
        # Cancelled multiple selection
        (Path(__file__).parent, True, None),
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
        dialog_result._impl,
        result,
        multiple_select=multiple_select,
    )

    if result is not None:
        on_result_handler.assert_called_once_with(main_window, result)
        assert await dialog_result == result
    else:
        on_result_handler.assert_called_once_with(main_window, None)
        assert await dialog_result is None
