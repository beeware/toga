from pathlib import Path
from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)


@pytest.fixture
def window(app):
    return toga.Window()


def test_window_created(app):
    "A Window can be created with minimal arguments"
    window = toga.Window()

    assert window.app == app
    assert window.content is None

    assert window._impl.interface == window
    assert_action_performed(window, "create Window")

    # We can't know what the ID is, but it must be a string.
    assert isinstance(window.id, str)
    assert window.title == "Toga"
    assert window.position == (100, 100)
    assert window.size == (640, 480)
    assert window.resizable
    assert window.closable
    assert window.minimizable
    assert len(window.toolbar) == 0
    assert window.on_close._raw is None


def test_window_created_explicit(app):
    "Explicit arguments at construction are stored"
    on_close_handler = Mock()

    window = toga.Window(
        id="my-window",
        title="My Window",
        position=(10, 20),
        size=(200, 300),
        resizable=False,
        closable=False,
        minimizable=False,
        on_close=on_close_handler,
    )

    assert window.app == app
    assert window.content is None

    assert window._impl.interface == window
    assert_action_performed(window, "create Window")

    assert window.id == "my-window"
    assert window.title == "My Window"
    assert window.position == (10, 20)
    assert window.size == (200, 300)
    assert not window.resizable
    assert not window.closable
    assert not window.minimizable
    assert len(window.toolbar) == 0
    assert window.on_close._raw == on_close_handler


def test_window_created_without_app():
    "A window cannot be created without an active app"
    toga.App.app = None
    with pytest.raises(
        RuntimeError, match="Cannot create a Window before creating an App"
    ):
        toga.Window()


def test_set_app(window, app):
    """A window's app cannot be reassigned"""
    assert window.app == app

    app2 = toga.App("Test App 2", "org.beeware.toga.test-app-2")
    with pytest.raises(ValueError, match=r"Window is already associated with an App"):
        window.app = app2


def test_set_app_with_content(window, app):
    """If a window has content, the content is assigned to the app"""
    assert window.app == app

    content = toga.Box()
    assert content.app is None

    window.content = content
    assert content.app == app


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Text", "New Text"),
        ("", "Toga"),
        (None, "Toga"),
        (12345, "12345"),
        ("Contains\nnewline", "Contains"),
    ],
)
def test_title(window, value, expected):
    """The title of the window can be changed"""
    window.title = value
    assert window.title == expected


def test_toolbar_implicit_add(window, app):
    """Adding an item to to a toolbar implicitly adds it to the app."""
    cmd1 = toga.Command(None, "Command 1")
    cmd2 = toga.Command(None, "Command 2")

    toolbar = window.toolbar
    assert list(toolbar) == []
    assert list(app.commands) == []

    # Adding a command to the toolbar automatically adds it to the app
    toolbar.add(cmd1)
    assert list(toolbar) == [cmd1]
    assert list(app.commands) == [cmd1]

    # But not vice versa
    app.commands.add(cmd2)
    assert list(toolbar) == [cmd1]
    assert list(app.commands) == [cmd1, cmd2]

    # Adding a command to both places does not cause a duplicate
    app.commands.add(cmd1)
    assert list(toolbar) == [cmd1]
    assert list(app.commands) == [cmd1, cmd2]


def test_change_content(window, app):
    """The content of a window can be changed"""
    assert window.content is None
    assert window.app == app

    # Set the content of the window
    content1 = toga.Box()
    window.content = content1

    # The content has been assigned and refreshed
    assert content1.app == app
    assert content1.window == window
    assert_action_performed_with(window, "set content", widget=content1._impl)
    assert_action_performed(content1, "refresh")

    # Set the content of the window to something new
    content2 = toga.Box()
    window.content = content2

    # The content has been assigned and refreshed
    assert content2.app == app
    assert content2.window == window
    assert_action_performed_with(window, "set content", widget=content2._impl)
    assert_action_performed(content2, "refresh")

    # The original content has been removed
    assert content1.window is None


def test_set_position(window):
    """The position of the window can be set."""
    window.position = (123, 456)

    assert window.position == (123, 456)


def test_set_size(window):
    """The size of the window can be set."""
    window.size = (123, 456)

    assert window.size == (123, 456)


def test_set_size_with_content(window):
    """The size of the window can be set."""
    content = toga.Box()
    window.content = content

    window.size = (123, 456)

    assert window.size == (123, 456)
    assert_action_performed(content, "refresh")


def test_show_hide(window, app):
    """The window can be shown and hidden."""
    assert window.app == app
    window.show()

    # The window has been assigned to the app, and is visible
    assert window.app == app
    assert window in app.windows
    assert_action_performed(window, "show")
    assert window.visible

    # Hide with an explicit call
    window.hide()

    # Window is still assigned to the app, but is not visible
    assert window.app == app
    assert window in app.windows
    assert_action_performed(window, "hide")
    assert not window.visible


def test_hide_show(window, app):
    """The window can be hidden then shown."""
    assert window.app == app
    window.hide()

    # The window has been assigned to the app, and is not visible
    assert window.app == app
    assert window in app.windows
    assert_action_performed(window, "hide")
    assert not window.visible

    # Show with an explicit call
    window.show()

    # Window is still assigned to the app, but is not visible
    assert window.app == app
    assert window in app.windows
    assert_action_performed(window, "show")
    assert window.visible


def test_visibility(window, app):
    """The window can be shown and hidden using the visible property."""
    assert window.app == app
    window.visible = True

    # The window has been assigned to the app, and is visible
    assert window.app == app
    assert window in app.windows
    assert_action_performed(window, "show")
    assert window.visible

    # Hide with an explicit call
    window.visible = False

    # Window is still assigned to the app, but is not visible
    assert window.app == app
    assert window in app.windows
    assert_action_performed(window, "hide")
    assert not window.visible


def test_full_screen(window, app):
    """A window can be set full screen."""
    assert not window.full_screen

    window.full_screen = True
    assert window.full_screen
    assert_action_performed_with(window, "set full screen", full_screen=True)

    window.full_screen = False
    assert not window.full_screen
    assert_action_performed_with(window, "set full screen", full_screen=False)


def test_close_direct(window, app):
    """A window can be closed directly"""
    on_close_handler = Mock(return_value=True)
    window.on_close = on_close_handler

    window.show()
    assert window.app == app
    assert window in app.windows

    # Close the window directly
    window.close()

    # Window has been closed, but the close handler has *not* been invoked.
    assert window.closed
    assert window.app == app
    assert window not in app.windows
    assert_action_performed(window, "close")
    on_close_handler.assert_not_called()


def test_close_no_handler(window, app):
    """A window without a close handler can be closed"""
    window.show()
    assert window.app == app
    assert window in app.windows

    # Close the window
    window._impl.simulate_close()

    # Window has been closed, and is no longer in the app's list of windows.
    assert window.closed
    assert window.app == app
    assert window not in app.windows
    assert_action_performed(window, "close")


def test_close_sucessful_handler(window, app):
    """A window with a successful close handler can be closed"""
    on_close_handler = Mock(return_value=True)
    window.on_close = on_close_handler

    window.show()
    assert window.app == app
    assert window in app.windows

    # Close the window
    window._impl.simulate_close()

    # Window has been closed, and is no longer in the app's list of windows.
    assert window.closed
    assert window.app == app
    assert window not in app.windows
    assert_action_performed(window, "close")
    on_close_handler.assert_called_once_with(window)


def test_close_rejected_handler(window, app):
    """A window can have a close handler that rejects closing"""
    on_close_handler = Mock(return_value=False)
    window.on_close = on_close_handler

    window.show()
    assert window.app == app
    assert window in app.windows

    # Close the window
    window._impl.simulate_close()

    # Window has *not* been closed
    assert not window.closed
    assert window.app == app
    assert window in app.windows
    assert_action_not_performed(window, "close")
    on_close_handler.assert_called_once_with(window)


def test_as_image(window):
    """A window can be captured as an image"""
    image = window.as_image()
    assert_action_performed(window, "get image data")
    # Don't need to check the raw data; just check it's the right size.
    assert image.size == (318, 346)


def test_info_dialog(window, app):
    """An info dialog can be shown"""
    on_result_handler = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog = window.info_dialog("Title", "Body", on_result=on_result_handler)

    assert dialog.window == window
    assert dialog.app == app

    with pytest.raises(
        RuntimeError,
        match=r"Can't check dialog result directly; use await or an on_result handler",
    ):
        # Perform a synchronous comparison; this will raise a runtime error
        dialog == 1

    async def run_dialog(dialog):
        dialog._impl.simulate_result(None)
        return await dialog

    assert app._impl.loop.run_until_complete(run_dialog(dialog)) is None

    assert_action_performed_with(
        window,
        "show info dialog",
        title="Title",
        message="Body",
    )
    on_result_handler.assert_called_once_with(window, None)


def test_question_dialog(window, app):
    """A question dialog can be shown"""
    on_result_handler = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog = window.question_dialog("Title", "Body", on_result=on_result_handler)

    assert dialog.window == window
    assert dialog.app == app

    with pytest.raises(
        RuntimeError,
        match=r"Can't check dialog result directly; use await or an on_result handler",
    ):
        # Perform a synchronous comparison; this will raise a runtime error
        dialog == 1

    async def run_dialog(dialog):
        dialog._impl.simulate_result(True)
        return await dialog

    assert app._impl.loop.run_until_complete(run_dialog(dialog))

    assert_action_performed_with(
        window,
        "show question dialog",
        title="Title",
        message="Body",
    )
    on_result_handler.assert_called_once_with(window, True)


def test_confirm_dialog(window, app):
    """A confirm dialog can be shown"""
    on_result_handler = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog = window.confirm_dialog("Title", "Body", on_result=on_result_handler)

    assert dialog.window == window
    assert dialog.app == app

    with pytest.raises(
        RuntimeError,
        match=r"Can't check dialog result directly; use await or an on_result handler",
    ):
        # Perform a synchronous comparison; this will raise a runtime error
        dialog == 1

    async def run_dialog(dialog):
        dialog._impl.simulate_result(True)
        return await dialog

    assert app._impl.loop.run_until_complete(run_dialog(dialog))

    assert_action_performed_with(
        window,
        "show confirm dialog",
        title="Title",
        message="Body",
    )
    on_result_handler.assert_called_once_with(window, True)


def test_error_dialog(window, app):
    """An error dialog can be shown"""
    on_result_handler = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog = window.error_dialog("Title", "Body", on_result=on_result_handler)

    assert dialog.window == window
    assert dialog.app == app

    with pytest.raises(
        RuntimeError,
        match=r"Can't check dialog result directly; use await or an on_result handler",
    ):
        # Perform a synchronous comparison; this will raise a runtime error
        dialog == 1

    async def run_dialog(dialog):
        dialog._impl.simulate_result(None)
        return await dialog

    assert app._impl.loop.run_until_complete(run_dialog(dialog)) is None

    assert_action_performed_with(
        window,
        "show error dialog",
        title="Title",
        message="Body",
    )
    on_result_handler.assert_called_once_with(window, None)


def test_stack_trace_dialog(window, app):
    """A stack trace dialog can be shown"""
    on_result_handler = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog = window.stack_trace_dialog(
            "Title",
            "Body",
            "The error",
            on_result=on_result_handler,
        )

    assert dialog.window == window
    assert dialog.app == app

    with pytest.raises(
        RuntimeError,
        match=r"Can't check dialog result directly; use await or an on_result handler",
    ):
        # Perform a synchronous comparison; this will raise a runtime error
        dialog == 1

    async def run_dialog(dialog):
        dialog._impl.simulate_result(None)
        return await dialog

    assert app._impl.loop.run_until_complete(run_dialog(dialog)) is None

    assert_action_performed_with(
        window,
        "show stack trace dialog",
        title="Title",
        message="Body",
        content="The error",
        retry=False,
    )
    on_result_handler.assert_called_once_with(window, None)


def test_save_file_dialog(window, app):
    """A save file dialog can be shown"""
    on_result_handler = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog = window.save_file_dialog(
            "Title",
            Path("/path/to/initial_file.txt"),
            on_result=on_result_handler,
        )

    assert dialog.window == window
    assert dialog.app == app

    with pytest.raises(
        RuntimeError,
        match=r"Can't check dialog result directly; use await or an on_result handler",
    ):
        # Perform a synchronous comparison; this will raise a runtime error
        dialog == 1

    saved_file = Path("/saved/path/filename.txt")

    async def run_dialog(dialog):
        dialog._impl.simulate_result(saved_file)
        return await dialog

    assert app._impl.loop.run_until_complete(run_dialog(dialog)) is saved_file

    assert_action_performed_with(
        window,
        "show save file dialog",
        title="Title",
        filename="initial_file.txt",
        initial_directory=Path("/path/to"),
        file_types=None,
    )
    on_result_handler.assert_called_once_with(window, saved_file)


def test_save_file_dialog_default_directory(window, app):
    """If no path is provided, a save file dialog will use the default directory"""
    on_result_handler = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog = window.save_file_dialog(
            "Title",
            "initial_file.txt",
            file_types=[".txt", ".pdf"],
            on_result=on_result_handler,
        )

    assert dialog.window == window
    assert dialog.app == app

    with pytest.raises(
        RuntimeError,
        match=r"Can't check dialog result directly; use await or an on_result handler",
    ):
        # Perform a synchronous comparison; this will raise a runtime error
        dialog == 1

    saved_file = Path("/saved/path/filename.txt")

    async def run_dialog(dialog):
        dialog._impl.simulate_result(saved_file)
        return await dialog

    assert app._impl.loop.run_until_complete(run_dialog(dialog)) is saved_file

    assert_action_performed_with(
        window,
        "show save file dialog",
        title="Title",
        filename="initial_file.txt",
        initial_directory=None,
        file_types=[".txt", ".pdf"],
    )
    on_result_handler.assert_called_once_with(window, saved_file)


def test_open_file_dialog(window, app):
    """A open file dialog can be shown"""
    on_result_handler = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog = window.open_file_dialog(
            "Title",
            "/path/to/folder",
            on_result=on_result_handler,
        )

    assert dialog.window == window
    assert dialog.app == app

    with pytest.raises(
        RuntimeError,
        match=r"Can't check dialog result directly; use await or an on_result handler",
    ):
        # Perform a synchronous comparison; this will raise a runtime error
        dialog == 1

    opened_file = Path("/opened/path/filename.txt")

    async def run_dialog(dialog):
        dialog._impl.simulate_result(opened_file)
        return await dialog

    assert app._impl.loop.run_until_complete(run_dialog(dialog)) is opened_file

    assert_action_performed_with(
        window,
        "show open file dialog",
        title="Title",
        initial_directory=Path("/path/to/folder"),
        file_types=None,
        multiple_select=False,
    )
    on_result_handler.assert_called_once_with(window, opened_file)


def test_open_file_dialog_default_directory(window, app):
    """If no path is provided, a open file dialog will use the default directory"""
    on_result_handler = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog = window.open_file_dialog(
            "Title",
            file_types=[".txt", ".pdf"],
            multiple_select=True,
            on_result=on_result_handler,
        )

    assert dialog.window == window
    assert dialog.app == app

    with pytest.raises(
        RuntimeError,
        match=r"Can't check dialog result directly; use await or an on_result handler",
    ):
        # Perform a synchronous comparison; this will raise a runtime error
        dialog == 1

    opened_files = [
        Path("/opened/path/filename.txt"),
        Path("/other/path/filename2.txt"),
    ]

    async def run_dialog(dialog):
        dialog._impl.simulate_result(opened_files)
        return await dialog

    assert app._impl.loop.run_until_complete(run_dialog(dialog)) is opened_files

    assert_action_performed_with(
        window,
        "show open file dialog",
        title="Title",
        initial_directory=None,
        file_types=[".txt", ".pdf"],
        multiple_select=True,
    )
    on_result_handler.assert_called_once_with(window, opened_files)


def test_select_folder_dialog(window, app):
    """A select folder dialog can be shown"""
    on_result_handler = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog = window.select_folder_dialog(
            "Title",
            Path("/path/to/folder"),
            on_result=on_result_handler,
        )

    assert dialog.window == window
    assert dialog.app == app

    with pytest.raises(
        RuntimeError,
        match=r"Can't check dialog result directly; use await or an on_result handler",
    ):
        # Perform a synchronous comparison; this will raise a runtime error
        dialog == 1

    opened_file = Path("/opened/path/filename.txt")

    async def run_dialog(dialog):
        dialog._impl.simulate_result(opened_file)
        return await dialog

    assert app._impl.loop.run_until_complete(run_dialog(dialog)) is opened_file

    assert_action_performed_with(
        window,
        "show select folder dialog",
        title="Title",
        initial_directory=Path("/path/to/folder"),
        multiple_select=False,
    )
    on_result_handler.assert_called_once_with(window, opened_file)


def test_select_folder_dialog_default_directory(window, app):
    """If no path is provided, a select folder dialog will use the default directory"""
    on_result_handler = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ):
        dialog = window.select_folder_dialog(
            "Title",
            multiple_select=True,
            on_result=on_result_handler,
        )

    assert dialog.window == window
    assert dialog.app == app

    with pytest.raises(
        RuntimeError,
        match=r"Can't check dialog result directly; use await or an on_result handler",
    ):
        # Perform a synchronous comparison; this will raise a runtime error
        dialog == 1

    opened_files = [
        Path("/opened/path/filename.txt"),
        Path("/other/path/filename2.txt"),
    ]

    async def run_dialog(dialog):
        dialog._impl.simulate_result(opened_files)
        return await dialog

    assert app._impl.loop.run_until_complete(run_dialog(dialog)) is opened_files

    assert_action_performed_with(
        window,
        "show select folder dialog",
        title="Title",
        initial_directory=None,
        multiple_select=True,
    )
    on_result_handler.assert_called_once_with(window, opened_files)


def test_deprecated_names_open_file_dialog(window, app):
    """Deprecated names still work on open file dialogs."""
    on_result_handler = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"open_file_dialog\(multiselect\) has been renamed multiple_select",
    ):
        dialog = window.open_file_dialog(
            "Title",
            "/path/to/folder",
            multiselect=True,
            on_result=on_result_handler,
        )

    opened_files = [Path("/opened/path/filename.txt")]

    async def run_dialog(dialog):
        dialog._impl.simulate_result(opened_files)
        return await dialog

    assert app._impl.loop.run_until_complete(run_dialog(dialog)) is opened_files

    assert_action_performed_with(
        window,
        "show open file dialog",
        title="Title",
        initial_directory=Path("/path/to/folder"),
        file_types=None,
        multiple_select=True,
    )
    on_result_handler.assert_called_once_with(window, opened_files)


def test_deprecated_names_select_folder_dialog(window, app):
    """Deprecated names still work on open file dialogs."""
    on_result_handler = Mock()

    with pytest.warns(
        DeprecationWarning,
        match=r"select_folder_dialog\(multiselect\) has been renamed multiple_select",
    ):
        dialog = window.select_folder_dialog(
            "Title",
            "/path/to/folder",
            multiselect=True,
            on_result=on_result_handler,
        )

    opened_files = [Path("/opened/path")]

    async def run_dialog(dialog):
        dialog._impl.simulate_result(opened_files)
        return await dialog

    assert app._impl.loop.run_until_complete(run_dialog(dialog)) is opened_files

    assert_action_performed_with(
        window,
        "show select folder dialog",
        title="Title",
        initial_directory=Path("/path/to/folder"),
        multiple_select=True,
    )
    on_result_handler.assert_called_once_with(window, opened_files)


def test_deprecated_names_resizeable():
    """Deprecated spelling of resizable still works"""
    with pytest.warns(
        DeprecationWarning,
        match=r"Window.resizeable has been renamed Window.resizable",
    ):
        window = toga.Window(title="Deprecated", resizeable=True)

    with pytest.warns(
        DeprecationWarning,
        match=r"Window.resizeable has been renamed Window.resizable",
    ):
        assert window.resizeable


def test_deprecated_names_closeable():
    """Deprecated spelling of closable still works"""
    with pytest.warns(
        DeprecationWarning,
        match=r"Window.closeable has been renamed Window.closable",
    ):
        window = toga.Window(title="Deprecated", closeable=True)

    with pytest.warns(
        DeprecationWarning,
        match=r"Window.closeable has been renamed Window.closable",
    ):
        assert window.closeable
