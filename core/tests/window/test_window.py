from pathlib import Path
from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)


def test_window_created(app):
    """A Window can be created with minimal arguments."""
    window = toga.Window()

    assert window.app == app
    assert window.content is None

    assert window._impl.interface == window
    assert_action_performed(window, "create Window")

    # We can't know what the ID is, but it must be a string.
    assert isinstance(window.id, str)
    assert window.title == "Test App"
    # The app has created a main window, so this will be the second window.
    assert window.position == toga.Position(150, 150)
    assert window.size == toga.Size(640, 480)
    assert window.resizable
    assert window.closable
    assert window.minimizable
    assert not hasattr(window, "toolbar")
    assert window.on_close._raw is None


def test_window_created_explicit(app):
    """Explicit arguments at construction are stored."""
    on_close_handler = Mock()
    window_content = toga.Box()

    window = toga.Window(
        id="my-window",
        title="My Window",
        position=toga.Position(10, 20),
        size=toga.Position(200, 300),
        resizable=False,
        closable=False,
        minimizable=False,
        content=window_content,
        on_close=on_close_handler,
    )

    assert window.app == app
    assert window.content == window_content

    window_content.window == window
    window_content.app == app

    assert window._impl.interface == window
    assert_action_performed(window, "create Window")

    assert window.id == "my-window"
    assert window.title == "My Window"
    assert window.position == toga.Position(10, 20)
    assert window.size == toga.Size(200, 300)
    assert not window.resizable
    assert not window.closable
    assert not window.minimizable
    assert not hasattr(window, "toolbar")
    assert window.on_close._raw == on_close_handler


def test_window_creation_accepts_tuples(app):
    """Tuple args are accepted and converted to NamedTuples"""
    on_close_handler = Mock()
    window = toga.Window(position=(10, 20), size=(200, 300), on_close=on_close_handler)
    assert window.position == toga.Position(10, 20)
    assert window.size == toga.Size(200, 300)


def test_window_created_without_app():
    """A window cannot be created without an active app."""
    toga.App.app = None
    with pytest.raises(
        RuntimeError, match="Cannot create a Window before creating an App"
    ):
        toga.Window()


def test_set_app(window, app):
    """A window's app cannot be reassigned."""
    assert window.app == app

    app2 = toga.App("Test App 2", "org.beeware.toga.test-app-2")
    with pytest.raises(ValueError, match=r"Window is already associated with an App"):
        window.app = app2


def test_set_app_with_content(window, app):
    """If a window has content, the content is assigned to the app."""
    assert window.app == app

    content = toga.Box()
    assert content.app is None

    window.content = content
    assert content.app == app


def test_set_app_with_content_at_instantiation(app):
    """A window can be created with initial content"""
    # Set up some initial content box with something inside it:
    label1 = toga.Label("Hello World")
    content = toga.Box(children=[label1])
    assert content.app is None

    window_with_content = toga.Window(content=content)

    # The window content has been set
    assert window_with_content.content == content
    # The full tree of content has been assigned to the app
    assert content.app == app
    assert label1.app == app

    assert content.window == window_with_content
    assert label1.window == window_with_content


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Text", "New Text"),
        ("", "Test App"),
        (None, "Test App"),
        (12345, "12345"),
        ("Contains\nnewline", "Contains"),
    ],
)
def test_title(window, value, expected):
    """The title of the window can be changed."""
    window.title = value
    assert window.title == expected


def test_change_content(window, app):
    """The content of a window can be changed."""
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

    assert window.position == toga.Position(123, 456)


def test_position_cascade(app):
    """The initial position of windows will cascade."""
    windows = [app.main_window]

    for i in range(0, 14):
        win = toga.Window(title=f"Window {i}")
        # The for the first 14 new windows (the app creates the first window)
        # the x and y coordinates must be the same
        assert win.position[0] == win.position[1]
        # The position of the window should cascade down
        assert win.position[0] > windows[-1].position[0]
        assert win.position[1] > windows[-1].position[1]

        windows.append(win)

    # The 15th window will come back to the y origin, but shift along the x axis.
    win = toga.Window(title=f"Window {i}")
    assert win.position[0] > windows[0].position[0]
    assert win.position[1] == windows[0].position[1]

    windows.append(win)

    # Cascade another 15 windows
    for i in range(16, 30):
        win = toga.Window(title=f"Window {i}")
        # The position of the window should cascade down
        assert win.position[0] > windows[-1].position[0]
        assert win.position[1] > windows[-1].position[1]

        # The y coordinate of these windows should be the same
        # as 15 windows ago; the x coordinate is shifted right
        assert win.position[0] > windows[i - 15].position[0]
        assert win.position[1] == windows[i - 15].position[1]

        windows.append(win)

    # The 30 window will come back to the y origin, but shift along the x axis.
    win = toga.Window(title=f"Window {i}")
    assert win.position[0] > windows[15].position[0]
    assert win.position[1] == windows[15].position[1]


def test_set_size(window):
    """The size of the window can be set."""
    window.size = (123, 456)

    assert window.size == toga.Size(123, 456)


def test_set_size_with_content(window):
    """The size of the window can be set."""
    content = toga.Box()
    window.content = content

    window.size = (123, 456)

    assert window.size == toga.Size(123, 456)
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
    """A window can be closed directly."""
    on_close_handler = Mock(return_value=True)
    window.on_close = on_close_handler

    window.show()
    assert window.app == app
    assert window in app.windows

    # Close the window directly
    assert window.close()

    # Window has been closed, but the close handler has *not* been invoked.
    assert window.closed
    assert window.app == app
    assert window not in app.windows
    assert_action_performed(window, "close")
    on_close_handler.assert_not_called()


def test_close_direct_main_window(app):
    """If the main window is closed directly, it triggers app exit logic."""
    window = app.main_window

    on_close_handler = Mock(return_value=True)
    window.on_close = on_close_handler

    on_exit_handler = Mock(return_value=True)
    app.on_exit = on_exit_handler

    window.show()
    assert window.app == app
    assert window in app.windows

    # Close the window directly;
    assert not window.close()

    # Window has *not* been closed.
    assert not window.closed
    assert window.app == app
    assert window in app.windows
    assert_action_not_performed(window, "close")

    # The close handler has *not* been invoked, but
    # the exit handler *has*.
    on_close_handler.assert_not_called()
    on_exit_handler.assert_called_once_with(app)
    assert_action_performed(app, "exit")


def test_close_no_handler(window, app):
    """A window without a close handler can be closed."""
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


def test_close_successful_handler(window, app):
    """A window with a successful close handler can be closed."""
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
    """A window can have a close handler that rejects closing."""
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
    """A window can be captured as an image."""
    image = window.as_image()
    assert_action_performed(window, "get image data")
    # Don't need to check the raw data; just check it's the right size.
    assert image.size == (318, 346)


def test_screen(window, app):
    """A window can be moved to a different screen."""
    # Cannot actually change window.screen, so just check
    # the window positions as a substitute for moving the
    # window between the screens.
    # `window.screen` will return `Secondary Screen`
    assert window.screen == app.screens[1]
    # The app has created a main window; the secondary window will be at second
    # position.
    assert window.position == toga.Position(150, 150)
    window.screen = app.screens[0]
    assert window.position == toga.Position(1516, 918)


def test_screen_position(window, app):
    """The window can be relocated using absolute and relative screen positions."""
    # Details about screen layout are in toga_dummy=>app.py=>get_screens()
    initial_position = window.position
    window.position = (-100, -100)
    assert window.position != initial_position
    assert window.position == toga.Position(-100, -100)
    assert window.screen_position == toga.Position(1266, 668)

    # Move the window to a new position.
    window.screen_position = (100, 100)
    assert window.position == toga.Position(-1266, -668)
    assert window.screen_position == toga.Position(100, 100)


def test_widget_id_reusablity(window, app):
    """Widget IDs can be reused after the associated widget's window is closed."""
    # Common IDs
    CONTENT_WIDGET_ID = "sample_window_content"
    LABEL_WIDGET_ID = "sample_label"

    label_widget = toga.Label(text="Sample Label", id=LABEL_WIDGET_ID)
    second_window_content = toga.Box(id=CONTENT_WIDGET_ID, children=[label_widget])

    third_window_content = toga.Box(children=[])

    # A widget ID is only "used" when it is part of a visible layout;
    # creating a widget and *not* putting it in a layout isn't an problem.
    try:
        new_label_widget = toga.Label(text="New Label", id=LABEL_WIDGET_ID)
    except KeyError:
        pytest.fail("Widget IDs that aren't part of a layout can be re-used.")

    # Create 2 new visible windows
    second_window = toga.Window()
    second_window.show()

    third_window = toga.Window()
    third_window.show()

    # Assign the window content widget to the second window
    second_window.content = second_window_content
    assert CONTENT_WIDGET_ID in app.widgets
    assert LABEL_WIDGET_ID in app.widgets

    # CONTENT_WIDGET_ID is in use, so a widget with that ID can't be assigned to a window.
    with pytest.raises(
        KeyError,
        match=r"There is already a widget with the id 'sample_label'",
    ):
        third_window.content = new_label_widget
    assert CONTENT_WIDGET_ID not in third_window.widgets
    assert LABEL_WIDGET_ID not in third_window.widgets

    # Adding content that has a child with a re-used ID should raise an error
    with pytest.raises(
        KeyError,
        match=r"There is already a widget with the id 'sample_label'",
    ):
        third_window.content = toga.Box(children=[new_label_widget])
    assert CONTENT_WIDGET_ID not in third_window.widgets
    assert LABEL_WIDGET_ID not in third_window.widgets

    # Adding a child with a re-used ID should raise an error.
    third_window.content = third_window_content
    with pytest.raises(
        KeyError,
        match=r"There is already a widget with the id 'sample_label'",
    ):
        third_window_content.add(new_label_widget)
    assert CONTENT_WIDGET_ID not in third_window.widgets
    assert LABEL_WIDGET_ID not in third_window.widgets

    # Creating a new widget with same widget ID should not raise KeyError
    try:
        another_label_widget = toga.Label(text="Another Label", id=LABEL_WIDGET_ID)
    except KeyError:
        pytest.fail("Widget IDs that aren't part of a layout can be re-used.")

    # If a widget using an ID is being *replaced*, the ID can be re-used.
    try:
        second_window.content = another_label_widget
    except KeyError:
        pytest.fail("Widget IDs that are replaced can be re-used.")

    # Close Window 2
    second_window.close()
    assert CONTENT_WIDGET_ID not in app.widgets
    assert LABEL_WIDGET_ID not in app.widgets

    # Now that second_window has been closed, the duplicate ID can be used
    try:
        third_window_content.add(new_label_widget)
    except KeyError:
        pytest.fail("Widget IDs that are replaced can be re-used.")

    third_window.close()


def test_deprecated_info_dialog(window, app):
    """An info dialog can be shown."""
    on_result_handler = Mock()

    # Prime the user's response
    window._impl.dialog_responses["InfoDialog"] = [None]

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ), pytest.warns(
        DeprecationWarning,
        match=r"info_dialog\(...\) has been deprecated; use dialog\(toga.InfoDialog\(...\)\)",
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

    assert app._impl.loop.run_until_complete(dialog) is None

    assert_action_performed_with(
        dialog.dialog,
        "create InfoDialog",
        title="Title",
        message="Body",
    )
    assert_action_performed_with(
        window,
        "show window InfoDialog",
    )
    on_result_handler.assert_called_once_with(window, None)


def test_deprecated_question_dialog(window, app):
    """A question dialog can be shown."""
    on_result_handler = Mock()

    # Prime the user's response
    window._impl.dialog_responses["QuestionDialog"] = [True]

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ), pytest.warns(
        DeprecationWarning,
        match=r"question_dialog\(...\) has been deprecated; use dialog\(toga.QuestionDialog\(...\)\)",
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

    assert app._impl.loop.run_until_complete(dialog)

    assert_action_performed_with(
        dialog.dialog,
        "create QuestionDialog",
        title="Title",
        message="Body",
    )
    assert_action_performed_with(
        window,
        "show window QuestionDialog",
    )
    on_result_handler.assert_called_once_with(window, True)


def test_deprecated_confirm_dialog(window, app):
    """A confirm dialog can be shown."""
    on_result_handler = Mock()

    # Prime the user's response
    window._impl.dialog_responses["ConfirmDialog"] = [True]

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ), pytest.warns(
        DeprecationWarning,
        match=r"confirm_dialog\(...\) has been deprecated; use dialog\(toga.ConfirmDialog\(...\)\)",
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

    assert app._impl.loop.run_until_complete(dialog)

    assert_action_performed_with(
        dialog.dialog,
        "create ConfirmDialog",
        title="Title",
        message="Body",
    )
    assert_action_performed_with(
        window,
        "show window ConfirmDialog",
    )
    on_result_handler.assert_called_once_with(window, True)


def test_deprecated_error_dialog(window, app):
    """An error dialog can be shown."""
    on_result_handler = Mock()

    # Prime the user's response
    window._impl.dialog_responses["ErrorDialog"] = [None]

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ), pytest.warns(
        DeprecationWarning,
        match=r"error_dialog\(...\) has been deprecated; use dialog\(toga.ErrorDialog\(...\)\)",
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

    assert app._impl.loop.run_until_complete(dialog) is None

    assert_action_performed_with(
        dialog.dialog,
        "create ErrorDialog",
        title="Title",
        message="Body",
    )
    assert_action_performed_with(
        window,
        "show window ErrorDialog",
    )
    on_result_handler.assert_called_once_with(window, None)


def test_deprecated_stack_trace_dialog(window, app):
    """A stack trace dialog can be shown."""
    on_result_handler = Mock()

    # Prime the user's response
    window._impl.dialog_responses["StackTraceDialog"] = [None]

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ), pytest.warns(
        DeprecationWarning,
        match=r"stack_trace_dialog\(...\) has been deprecated; use dialog\(toga.StackTraceDialog\(...\)\)",
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

    assert app._impl.loop.run_until_complete(dialog) is None

    assert_action_performed_with(
        dialog.dialog,
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
    on_result_handler.assert_called_once_with(window, None)


def test_deprecated_save_file_dialog(window, app):
    """A save file dialog can be shown."""
    on_result_handler = Mock()

    # Prime the user's response
    saved_file = Path("/saved/path/filename.txt")
    window._impl.dialog_responses["SaveFileDialog"] = [saved_file]

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ), pytest.warns(
        DeprecationWarning,
        match=r"save_file_dialog\(...\) has been deprecated; use dialog\(toga.SaveFileDialog\(...\)\)",
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

    assert app._impl.loop.run_until_complete(dialog) is saved_file

    assert_action_performed_with(
        dialog.dialog,
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
    on_result_handler.assert_called_once_with(window, saved_file)


def test_deprecated_save_file_dialog_default_directory(window, app):
    """If no path is provided, a save file dialog will use the default directory."""
    on_result_handler = Mock()

    # Prime the user's response
    saved_file = Path("/saved/path/filename.txt")
    window._impl.dialog_responses["SaveFileDialog"] = [saved_file]

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ), pytest.warns(
        DeprecationWarning,
        match=r"save_file_dialog\(...\) has been deprecated; use dialog\(toga.SaveFileDialog\(...\)\)",
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

    assert app._impl.loop.run_until_complete(dialog) is saved_file

    assert_action_performed_with(
        dialog.dialog,
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
    on_result_handler.assert_called_once_with(window, saved_file)


def test_deprecated_open_file_dialog(window, app):
    """A open file dialog can be shown."""
    on_result_handler = Mock()

    # Prime the user's response
    opened_file = Path("/opened/path/filename.txt")
    window._impl.dialog_responses["OpenFileDialog"] = [opened_file]

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ), pytest.warns(
        DeprecationWarning,
        match=r"open_file_dialog\(...\) has been deprecated; use dialog\(toga.OpenFileDialog\(...\)\)",
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

    assert app._impl.loop.run_until_complete(dialog) is opened_file

    assert_action_performed_with(
        dialog.dialog,
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
    on_result_handler.assert_called_once_with(window, opened_file)


def test_deprecated_open_file_dialog_default_directory(window, app):
    """If no path is provided, a open file dialog will use the default directory."""
    on_result_handler = Mock()

    # Prime the user's response
    opened_files = [
        Path("/opened/path/filename.txt"),
        Path("/opened/path/filename2.txt"),
    ]
    window._impl.dialog_responses["OpenFileDialog"] = [opened_files]

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ), pytest.warns(
        DeprecationWarning,
        match=r"open_file_dialog\(...\) has been deprecated; use dialog\(toga.OpenFileDialog\(...\)\)",
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

    assert app._impl.loop.run_until_complete(dialog) is opened_files

    assert_action_performed_with(
        dialog.dialog,
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
    on_result_handler.assert_called_once_with(window, opened_files)


def test_deprecated_select_folder_dialog(window, app):
    """A select folder dialog can be shown."""
    on_result_handler = Mock()

    # Prime the user's response
    opened_folder = Path("/opened/path")
    window._impl.dialog_responses["SelectFolderDialog"] = [opened_folder]

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ), pytest.warns(
        DeprecationWarning,
        match=r"select_folder_dialog\(...\) has been deprecated; use dialog\(toga.SelectFolderDialog\(...\)\)",
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

    assert app._impl.loop.run_until_complete(dialog) is opened_folder

    assert_action_performed_with(
        dialog.dialog,
        "create SelectFolderDialog",
        title="Title",
        initial_directory=Path("/path/to/folder"),
        multiple_select=False,
    )
    assert_action_performed_with(
        window,
        "show window SelectFolderDialog",
    )
    on_result_handler.assert_called_once_with(window, opened_folder)


def test_deprecated_select_folder_dialog_default_directory(window, app):
    """If no path is provided, a select folder dialog will use the default directory."""
    on_result_handler = Mock()

    # Prime the user's response
    opened_paths = [
        Path("/opened/path"),
        Path("/other/path"),
    ]
    window._impl.dialog_responses["SelectFolderDialog"] = [opened_paths]

    with pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated;",
    ), pytest.warns(
        DeprecationWarning,
        match=r"select_folder_dialog\(...\) has been deprecated; use dialog\(toga.SelectFolderDialog\(...\)\)",
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

    assert app._impl.loop.run_until_complete(dialog) is opened_paths

    assert_action_performed_with(
        dialog.dialog,
        "create SelectFolderDialog",
        title="Title",
        initial_directory=None,
        multiple_select=True,
    )
    assert_action_performed_with(
        window,
        "show window SelectFolderDialog",
    )
    on_result_handler.assert_called_once_with(window, opened_paths)


def test_deprecated_names_open_file_dialog(window, app):
    """Deprecated names still work on open file dialogs."""
    on_result_handler = Mock()

    # Prime the user's response
    opened_files = [Path("/opened/path/filename.txt")]
    window._impl.dialog_responses["OpenFileDialog"] = [opened_files]

    with pytest.warns(
        DeprecationWarning,
        match=r"open_file_dialog\(multiselect\) has been renamed multiple_select",
    ), pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated; use `await` on the asynchronous result",
    ), pytest.warns(
        DeprecationWarning,
        match=r"open_file_dialog\(...\) has been deprecated; use dialog\(toga.OpenFileDialog\(...\)\)",
    ):
        dialog = window.open_file_dialog(
            "Title",
            "/path/to/folder",
            multiselect=True,
            on_result=on_result_handler,
        )

    assert app._impl.loop.run_until_complete(dialog) is opened_files

    assert_action_performed_with(
        dialog.dialog,
        "create OpenFileDialog",
        title="Title",
        initial_directory=Path("/path/to/folder"),
        file_types=None,
        multiple_select=True,
    )
    assert_action_performed_with(
        window,
        "show window OpenFileDialog",
    )
    on_result_handler.assert_called_once_with(window, opened_files)


def test_deprecated_names_select_folder_dialog(window, app):
    """Deprecated names still work on selected folder dialogs."""
    on_result_handler = Mock()

    # Prime the user's response
    selected_folder = [Path("/opened/path")]
    window._impl.dialog_responses["SelectFolderDialog"] = [selected_folder]

    with pytest.warns(
        DeprecationWarning,
        match=r"select_folder_dialog\(multiselect\) has been renamed multiple_select",
    ), pytest.warns(
        DeprecationWarning,
        match=r"Synchronous `on_result` handlers have been deprecated; use `await` on the asynchronous result",
    ), pytest.warns(
        DeprecationWarning,
        match=r"select_folder_dialog\(...\) has been deprecated; use dialog\(toga.SelectFolderDialog\(...\)\)",
    ):
        dialog = window.select_folder_dialog(
            "Title",
            "/path/to/folder",
            multiselect=True,
            on_result=on_result_handler,
        )

    assert app._impl.loop.run_until_complete(dialog) is selected_folder

    assert_action_performed_with(
        dialog.dialog,
        "create SelectFolderDialog",
        title="Title",
        initial_directory=Path("/path/to/folder"),
        multiple_select=True,
    )
    assert_action_performed_with(
        window,
        "show window SelectFolderDialog",
    )
    on_result_handler.assert_called_once_with(window, selected_folder)


def test_deprecated_names_resizeable():
    """Deprecated spelling of resizable still works."""
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
    """Deprecated spelling of closable still works."""
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
