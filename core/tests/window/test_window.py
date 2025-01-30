from pathlib import Path
from unittest.mock import Mock

import pytest

import toga
from toga.constants import WindowState
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)

from ..utils import (
    assert_window_gain_focus,
    assert_window_lose_focus,
    assert_window_on_hide,
    assert_window_on_show,
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
    # Request for resizing to a new window size.
    window.size = (123, 456)

    assert window.size == toga.Size(123, 456)
    assert_action_performed(window, "set size")
    EventLog.reset()

    # Again request for resizing to the same window size.
    window.size = (123, 456)

    assert window.size == toga.Size(123, 456)
    assert_action_not_performed(window, "set size")


def test_set_size_with_content(window):
    """The size of the window can be set."""
    content = toga.Box()
    window.content = content

    # Request for resizing to a new window size.
    window.size = (123, 456)

    assert window.size == toga.Size(123, 456)
    assert_action_performed(window, "set size")
    assert_action_performed(content, "refresh")
    EventLog.reset()

    # Again request for resizing to the same window size.
    window.size = (123, 456)

    assert window.size == toga.Size(123, 456)
    assert_action_not_performed(window, "set size")
    assert_action_not_performed(content, "refresh")


def test_show_hide(window, app):
    """The window can be shown & hidden, but requesting visibility change when
    the window is already in that requested visibility state is a no-op."""
    # Window is assigned to the app, but is not visible
    assert window.app == app
    assert window in app.windows
    assert not window.visible

    # Show the window
    window.show()

    # The window has been assigned to the app, and is visible
    assert window.app == app
    assert window in app.windows
    assert window.visible
    assert_action_performed(window, "show")
    EventLog.reset()

    # The window is already shown, so this call will be a no-op
    window.show()

    # The window is still assigned to the app, and is visible
    assert window.app == app
    assert window in app.windows
    assert window.visible
    assert_action_not_performed(window, "show")

    # Hide the window
    window.hide()

    # Window is still assigned to the app, but is not visible
    assert window.app == app
    assert window in app.windows
    assert not window.visible
    assert_action_performed(window, "hide")
    EventLog.reset()

    # The window is already hidden, so this call will be a no-op
    window.hide()

    # Window is still assigned to the app, but is not visible
    assert window.app == app
    assert window in app.windows
    assert not window.visible
    assert_action_not_performed(window, "hide")

    # Show the window
    window.show()

    # The window is still assigned to the app, and is visible
    assert window.app == app
    assert window in app.windows
    assert window.visible
    assert_action_performed(window, "show")


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


@pytest.mark.parametrize(
    "state",
    [
        WindowState.MINIMIZED,
        WindowState.FULLSCREEN,
        WindowState.PRESENTATION,
    ],
)
def test_show_hide_disallowed_on_window_state(window, app, state):
    """A window in MINIMIZED, FULLSCREEN or PRESENTATION state cannot be
    shown or hidden."""
    window.show()

    window.state = state
    assert window.state == state
    assert window.visible is True
    EventLog.reset()

    with pytest.raises(
        ValueError,
        match=f"A window in {state} state cannot be hidden.",
    ):
        window.hide()
        assert_action_not_performed(window, "hide")

    with pytest.raises(
        ValueError,
        match=f"A window in {state} state cannot be hidden.",
    ):
        window.visible = False
        assert_action_not_performed(window, "hide")

    # Using only the Toga API, it shouldn't be possible to get a window into a hidden
    # state while minimized; but if you're poking underlying APIs it might be possible.
    # It's also good from the point of view of symmetry that the same error conditions
    # exist. So - fake using "native APIs" to make the window hidden
    window._impl._visible = False
    assert window.state == state
    assert window.visible is False

    with pytest.raises(
        ValueError,
        match=f"A window in {state} state cannot be shown.",
    ):
        window.show()
        assert_action_not_performed(window, "show")

    with pytest.raises(
        ValueError,
        match=f"A window in {state} state cannot be shown.",
    ):
        window.visible = True
        assert_action_not_performed(window, "show")


@pytest.mark.parametrize(
    "initial_state, final_state",
    [
        # Direct switch from NORMAL:
        (WindowState.NORMAL, WindowState.MINIMIZED),
        (WindowState.NORMAL, WindowState.MAXIMIZED),
        (WindowState.NORMAL, WindowState.FULLSCREEN),
        (WindowState.NORMAL, WindowState.PRESENTATION),
        # Direct switch from MINIMIZED:
        (WindowState.MINIMIZED, WindowState.NORMAL),
        (WindowState.MINIMIZED, WindowState.MAXIMIZED),
        (WindowState.MINIMIZED, WindowState.FULLSCREEN),
        (WindowState.MINIMIZED, WindowState.PRESENTATION),
        # Direct switch from MAXIMIZED:
        (WindowState.MAXIMIZED, WindowState.NORMAL),
        (WindowState.MAXIMIZED, WindowState.MINIMIZED),
        (WindowState.MAXIMIZED, WindowState.FULLSCREEN),
        (WindowState.MAXIMIZED, WindowState.PRESENTATION),
        # Direct switch from FULLSCREEN:
        (WindowState.FULLSCREEN, WindowState.NORMAL),
        (WindowState.FULLSCREEN, WindowState.MINIMIZED),
        (WindowState.FULLSCREEN, WindowState.MAXIMIZED),
        (WindowState.FULLSCREEN, WindowState.PRESENTATION),
        # Direct switch from PRESENTATION:
        (WindowState.PRESENTATION, WindowState.NORMAL),
        (WindowState.PRESENTATION, WindowState.MINIMIZED),
        (WindowState.PRESENTATION, WindowState.MAXIMIZED),
        (WindowState.PRESENTATION, WindowState.FULLSCREEN),
    ],
)
def test_window_state(window, initial_state, final_state):
    """A window can have different states."""
    window.show()
    window.on_show = Mock()
    window.on_hide = Mock()
    assert window.state == WindowState.NORMAL

    window.state = initial_state
    assert window.state == initial_state
    # A newly created window will always be in NORMAL state.
    # Since, both the current state and initial_state, would
    # be the same, hence "set window state to WindowState.NORMAL"
    # action would not be performed again.
    if initial_state != WindowState.NORMAL:
        assert_action_performed_with(
            window,
            f"set window state to {initial_state}",
            state=initial_state,
        )

    # Check for visibility event notification
    if initial_state == WindowState.MINIMIZED:
        # on_hide() will be triggered, as it was set to a
        # not-visible-to-user(minimized) state.
        assert_window_on_hide(window)
    else:
        # on_show() will not be triggered again, as it was
        # already in a visible-to-user(not hidden) state, and
        # was set to a visible-to-user(not minimized) state.
        assert_window_on_show(window, trigger_expected=False)

    window.state = final_state
    assert window.state == final_state
    assert_action_performed_with(
        window,
        f"set window state to {final_state}",
        state=final_state,
    )

    # Check for visibility event notification
    if initial_state == WindowState.MINIMIZED:
        if final_state == WindowState.MINIMIZED:
            # on_hide() will not be triggered again, as it was
            # already in a not-visible-to-user(minimized) state.
            assert_window_on_hide(window, trigger_expected=False)
        else:
            # on_show() will be triggered, as it was previously
            # in a not-visible-to-user(minimized) state.
            assert_window_on_show(window)
    else:
        if final_state == WindowState.MINIMIZED:
            # on_hide() will be triggered, as it was previously
            # in a visible-to-user(not minimized) state.
            assert_window_on_hide(window)
        else:
            # on_show() will not be triggered again, as it was
            # already in a visible-to-user(not minimized) state.
            assert_window_on_show(window, trigger_expected=False)


@pytest.mark.parametrize(
    "state",
    [
        WindowState.NORMAL,
        WindowState.MINIMIZED,
        WindowState.MAXIMIZED,
        WindowState.FULLSCREEN,
        WindowState.PRESENTATION,
    ],
)
def test_window_state_same_as_current(window, state):
    """Setting window state the same as current is a no-op."""
    window.show()

    window.state = state
    assert window.state == state

    # Reset the EventLog to check that the action was not re-performed.
    EventLog.reset()
    window.show()

    window.state = state
    assert window.state == state
    assert_action_not_performed(window, f"set window state to {state}")


@pytest.mark.parametrize(
    "state",
    [
        WindowState.NORMAL,
        WindowState.MINIMIZED,
        WindowState.MAXIMIZED,
        WindowState.FULLSCREEN,
        WindowState.PRESENTATION,
    ],
)
def test_hidden_window_state(state):
    """Window state of a hidden window cannot be changed."""
    hidden_window = toga.Window(title="Hidden Window")
    hidden_window.hide()

    with pytest.raises(
        RuntimeError,
        match="Window state of a hidden window cannot be changed.",
    ):
        hidden_window.state = state
        assert_action_not_performed(hidden_window, f"set window state to {state}")
    hidden_window.close()


@pytest.mark.parametrize(
    "state",
    [
        WindowState.MAXIMIZED,
        WindowState.FULLSCREEN,
        WindowState.PRESENTATION,
    ],
)
def test_non_resizable_window_state(state):
    """Non-resizable window's states other than minimized or normal are no-ops."""
    non_resizable_window = toga.Window(title="Non-Resizable Window", resizable=False)
    non_resizable_window.show()

    with pytest.raises(
        ValueError,
        match=f"A non-resizable window cannot be set to a state of {state}.",
    ):
        non_resizable_window.state = state
        assert_action_not_performed(
            non_resizable_window, f"set window state to {state}"
        )
    non_resizable_window.close()


@pytest.mark.parametrize(
    "state",
    [
        WindowState.FULLSCREEN,
        WindowState.PRESENTATION,
    ],
)
def test_resize_in_window_state(state):
    """Window size cannot be changed while in fullscreen or presentation state."""
    window = toga.Window(title="Non-resizing window")
    window.show()
    window.state = state

    with pytest.raises(RuntimeError, match=f"Cannot resize window while in {state}"):
        window.size = (100, 200)
    window.close()


@pytest.mark.parametrize(
    "state",
    [
        WindowState.FULLSCREEN,
        WindowState.PRESENTATION,
    ],
)
def test_move_in_window_state(state):
    """Window position cannot be changed while in fullscreen or presentation state."""
    window = toga.Window(title="Non-resizing window")
    window.show()
    window.state = state

    with pytest.raises(
        RuntimeError, match=f"Cannot change window position while in {state}"
    ):
        window.position = (100, 200)

    with pytest.raises(
        RuntimeError, match=f"Cannot change window position while in {state}"
    ):
        window.screen_position = (100, 200)
    window.close()


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


def test_focus_events(app):
    """The window can trigger on_gain_focus() and on_lose_focus()
    event handlers, when the window gains or loses input focus."""
    window1 = toga.Window()
    window1.show()
    assert window1.on_gain_focus._raw is None
    assert window1.on_lose_focus._raw is None
    window1_on_gain_focus_handler = Mock()
    window1_on_lose_focus_handler = Mock()
    window1.on_gain_focus = window1_on_gain_focus_handler
    window1.on_lose_focus = window1_on_lose_focus_handler
    assert window1.on_gain_focus._raw == window1_on_gain_focus_handler
    assert window1.on_lose_focus._raw == window1_on_lose_focus_handler

    window2 = toga.Window()
    window2.show()
    assert window2.on_gain_focus._raw is None
    assert window2.on_lose_focus._raw is None
    window2_on_gain_focus_handler = Mock()
    window2_on_lose_focus_handler = Mock()
    window2.on_gain_focus = window2_on_gain_focus_handler
    window2.on_lose_focus = window2_on_lose_focus_handler
    assert window2.on_gain_focus._raw == window2_on_gain_focus_handler
    assert window2.on_lose_focus._raw == window2_on_lose_focus_handler

    app.current_window = window1
    assert_window_gain_focus(window1)

    app.current_window = window2
    assert_window_gain_focus(window2)
    assert_window_lose_focus(window1)

    app.current_window = window1
    assert_window_gain_focus(window1)
    assert_window_lose_focus(window2)


def test_visibility_events(window):
    """The window can trigger on_show() and on_hide() event handlers,
    when the window is shown or hidden respectively."""
    window.show()
    assert window.on_show._raw is None
    assert window.on_hide._raw is None
    on_show_handler = Mock()
    on_hide_handler = Mock()
    window.on_show = on_show_handler
    window.on_hide = on_hide_handler
    assert window.on_show._raw == on_show_handler
    assert window.on_hide._raw == on_hide_handler

    window.hide()
    assert_window_on_hide(window)

    window.show()
    assert_window_on_show(window)


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
        pytest.fail("Widget IDs that aren't part of a layout can be reused.")

    # Create 2 new visible windows
    second_window = toga.Window()
    second_window.show()

    third_window = toga.Window()
    third_window.show()

    # Assign the window content widget to the second window
    second_window.content = second_window_content
    assert CONTENT_WIDGET_ID in app.widgets
    assert LABEL_WIDGET_ID in app.widgets

    # CONTENT_WIDGET_ID is in use, so a widget with that ID can't be assigned
    # to a window.
    with pytest.raises(
        KeyError,
        match=r"There is already a widget with the id 'sample_label'",
    ):
        third_window.content = new_label_widget
    assert CONTENT_WIDGET_ID not in third_window.widgets
    assert LABEL_WIDGET_ID not in third_window.widgets

    # Adding content that has a child with a reused ID should raise an error
    with pytest.raises(
        KeyError,
        match=r"There is already a widget with the id 'sample_label'",
    ):
        third_window.content = toga.Box(children=[new_label_widget])
    assert CONTENT_WIDGET_ID not in third_window.widgets
    assert LABEL_WIDGET_ID not in third_window.widgets

    # Adding a child with a reused ID should raise an error.
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
        pytest.fail("Widget IDs that aren't part of a layout can be reused.")

    # If a widget using an ID is being *replaced*, the ID can be reused.
    try:
        second_window.content = another_label_widget
    except KeyError:
        pytest.fail("Widget IDs that are replaced can be reused.")

    # Close Window 2
    second_window.close()
    assert CONTENT_WIDGET_ID not in app.widgets
    assert LABEL_WIDGET_ID not in app.widgets

    # Now that second_window has been closed, the duplicate ID can be used
    try:
        third_window_content.add(new_label_widget)
    except KeyError:
        pytest.fail("Widget IDs that are replaced can be reused.")

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
        match=(
            r"info_dialog\(...\) has been deprecated; "
            r"use dialog\(toga.InfoDialog\(...\)\)"
        ),
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
        match=(
            r"question_dialog\(...\) has been deprecated; "
            r"use dialog\(toga.QuestionDialog\(...\)\)"
        ),
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
        match=(
            r"confirm_dialog\(...\) has been deprecated; "
            r"use dialog\(toga.ConfirmDialog\(...\)\)"
        ),
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
        match=(
            r"error_dialog\(...\) has been deprecated; "
            r"use dialog\(toga.ErrorDialog\(...\)\)"
        ),
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
        match=(
            r"stack_trace_dialog\(...\) has been deprecated; "
            r"use dialog\(toga.StackTraceDialog\(...\)\)"
        ),
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
        match=(
            r"save_file_dialog\(...\) has been deprecated; "
            r"use dialog\(toga.SaveFileDialog\(...\)\)"
        ),
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
        match=(
            r"save_file_dialog\(...\) has been deprecated; "
            r"use dialog\(toga.SaveFileDialog\(...\)\)"
        ),
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
        match=(
            r"open_file_dialog\(...\) has been deprecated; "
            r"use dialog\(toga.OpenFileDialog\(...\)\)"
        ),
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
        match=(
            r"open_file_dialog\(...\) has been deprecated; "
            r"use dialog\(toga.OpenFileDialog\(...\)\)"
        ),
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
        match=(
            r"select_folder_dialog\(...\) has been deprecated; "
            r"use dialog\(toga.SelectFolderDialog\(...\)\)"
        ),
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
        match=(
            r"select_folder_dialog\(...\) has been deprecated; "
            r"use dialog\(toga.SelectFolderDialog\(...\)\)"
        ),
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
        match=(
            r"Synchronous `on_result` handlers have been deprecated; "
            r"use `await` on the asynchronous result"
        ),
    ), pytest.warns(
        DeprecationWarning,
        match=(
            r"open_file_dialog\(...\) has been deprecated; "
            r"use dialog\(toga.OpenFileDialog\(...\)\)"
        ),
    ):
        dialog = window.open_file_dialog(
            "Title",
            "/path/to/folder",
            multiple_select=True,
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
        match=(
            r"Synchronous `on_result` handlers have been deprecated; "
            r"use `await` on the asynchronous result"
        ),
    ), pytest.warns(
        DeprecationWarning,
        match=(
            r"select_folder_dialog\(...\) has been deprecated; "
            r"use dialog\(toga.SelectFolderDialog\(...\)\)"
        ),
    ):
        dialog = window.select_folder_dialog(
            "Title",
            "/path/to/folder",
            multiple_select=True,
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


def test_deprecated_full_screen(window, app):
    """A window can be set full screen using the deprecated API."""
    full_screen_warning = (
        "`Window.full_screen` is deprecated. Use `Window.state` instead."
    )
    with pytest.warns(
        DeprecationWarning,
        match=full_screen_warning,
    ):
        assert not window.full_screen
    with pytest.warns(
        DeprecationWarning,
        match=full_screen_warning,
    ):
        window.full_screen = True
    with pytest.warns(
        DeprecationWarning,
        match=full_screen_warning,
    ):
        assert window.full_screen
    assert_action_performed_with(
        window,
        "set window state to WindowState.FULLSCREEN",
        state=WindowState.FULLSCREEN,
    )
    with pytest.warns(
        DeprecationWarning,
        match=full_screen_warning,
    ):
        window.full_screen = False
    with pytest.warns(
        DeprecationWarning,
        match=full_screen_warning,
    ):
        assert not window.full_screen
    assert_action_performed_with(
        window,
        "set window state to WindowState.NORMAL",
        state=WindowState.NORMAL,
    )

    # Clear the test event log to check that the previous task was not re-performed.
    EventLog.reset()

    assert window.state == WindowState.NORMAL
    with pytest.warns(
        DeprecationWarning,
        match=full_screen_warning,
    ):
        assert not window.full_screen
    with pytest.warns(
        DeprecationWarning,
        match=full_screen_warning,
    ):
        window.full_screen = False

    assert_action_not_performed(window, "set window state to WindowState.NORMAL")
