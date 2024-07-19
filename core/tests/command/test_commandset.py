import random
from unittest.mock import Mock

import pytest

import toga
from toga.command import CommandSet, Separator


def test_create():
    """A CommandSet can be created with defaults."""
    cs = CommandSet()

    assert list(cs) == []
    assert cs.on_change is None


def test_create_with_values():
    """A CommandSet can be created with values."""
    change_handler = Mock()
    cs = CommandSet(on_change=change_handler)

    assert list(cs) == []
    assert cs.on_change == change_handler


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_add_clear(app, change_handler):
    """Commands can be added and removed from a commandset."""
    # Make sure the app commands are clear to start with.
    app.commands.clear()

    # Put some commands into the app
    cmd_a = toga.Command(None, text="App command a")
    cmd_b = toga.Command(None, text="App command b", order=10)
    app.commands.add(cmd_a, cmd_b)
    assert list(app.commands) == [cmd_a, cmd_b]

    # Create a standalone command set and add some commands
    cs = CommandSet(on_change=change_handler)
    cmd1a = toga.Command(None, text="Test command 1a", order=3)
    cmd1b = toga.Command(None, text="Test command 1b", order=1)
    cs.add(cmd1a, cmd1b)

    # Change handler was called once.
    if change_handler:
        change_handler.assert_called_once()
        change_handler.reset_mock()

    # Command set has commands, and the order is the opposite to the insertion order.
    assert list(cs) == [cmd1b, cmd1a]

    # New Commands aren't known to the app
    assert list(app.commands) == [cmd_a, cmd_b]

    # Clear the command set
    cs.clear()

    # Change handler was called once.
    if change_handler:
        change_handler.assert_called_once()
        change_handler.reset_mock()

    # Command set no commands.
    assert list(cs) == []

    # App command set hasn't changed.
    assert list(app.commands) == [cmd_a, cmd_b]


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_add_clear_with_app(app, change_handler):
    """Commands can be added and removed from a commandset that is linked to an app."""
    # Make sure the app commands are clear to start with.
    app.commands.clear()

    # Put some commands into the app
    cmd_a = toga.Command(None, text="App command a")
    cmd_b = toga.Command(None, text="App command b", order=10)
    app.commands.add(cmd_a, cmd_b)
    assert list(app.commands) == [cmd_a, cmd_b]

    # Create a command set that is linked to the app and add some commands
    cs = CommandSet(on_change=change_handler, app=app)
    cmd1a = toga.Command(None, text="Test command 1a", order=3)
    cmd1b = toga.Command(None, text="Test command 1b", order=1)
    cs.add(cmd1a, cmd1b)

    # Change handler was called once.
    if change_handler:
        change_handler.assert_called_once()
        change_handler.reset_mock()

    # Command set has commands, and the order is the opposite to the insertion order.
    assert list(cs) == [cmd1b, cmd1a]

    # New Commands are known to the app
    assert list(app.commands) == [cmd_a, cmd1b, cmd1a, cmd_b]

    # Add another command to the commandset
    cmd2 = toga.Command(None, text="Test command 2", order=2)
    cs.add(cmd2)

    # Change handler was called once.
    if change_handler:
        change_handler.assert_called_once()
        change_handler.reset_mock()

    # Command set has commands, and the output is ordered.
    assert list(cs) == [cmd1b, cmd2, cmd1a]

    # App also knows about the command
    assert list(app.commands) == [cmd_a, cmd1b, cmd2, cmd1a, cmd_b]

    # Clear the command set
    cs.clear()

    # Change handler was called once.
    if change_handler:
        change_handler.assert_called_once()
        change_handler.reset_mock()

    # Command set has no commands.
    assert list(cs) == []

    # App command set hasn't changed.
    assert list(app.commands) == [cmd_a, cmd1b, cmd2, cmd1a, cmd_b]


def test_add_missing_command(app):
    """Missing commands are ignored by addition."""
    # Make sure the app commands are clear to start with.
    app.commands.clear()

    # Put some commands (and some missing commands) into the app
    cmd_a = toga.Command(None, text="App command a")
    cmd_b = toga.Command(None, text="App command b", order=10)
    app.commands.add(cmd_a, None, cmd_b, None)
    # The missing commands are ignored.
    assert list(app.commands) == [cmd_a, cmd_b]


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_add_by_existing_id(change_handler):
    """Commands can be added by ID."""
    change_handler = Mock()
    cs = CommandSet(on_change=change_handler)

    # Define a command with an ID
    cmd_a = toga.Command(None, text="App command a", id="custom-command-a")

    # Install a command without an ID
    cs["custom-command-a"] = cmd_a

    # The command can be retrieved by ID or instance
    assert "custom-command-a" in cs
    assert cmd_a in cs
    assert cs["custom-command-a"] == cmd_a
    # Change handler was invoked
    change_handler.assert_called_once_with()


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_add_by_different_id(change_handler):
    """If a command is added using a different ID, an error is raised."""
    change_handler = Mock()
    cs = CommandSet(on_change=change_handler)

    # Define a command with an ID
    cmd_a = toga.Command(None, text="App command a", id="custom-command-a")

    # Install a command with a different ID:
    with pytest.raises(
        ValueError,
        match=r"Command has id 'custom-command-a'; can't add as 'new-id'",
    ):
        cs["new-id"] = cmd_a

    # The command can be retrieved by ID or instance
    assert "new-id" not in cs
    assert "custom-command-a" not in cs
    assert cmd_a not in cs
    # Change handler was not invoked
    change_handler.assert_not_called()


def test_retrieve_by_id(app):
    """Commands can be retrieved by ID."""

    # Put some extra commands into the app
    cmd_a = toga.Command(None, text="App command a")
    cmd_b = toga.Command(None, text="App command b", id="custom-command-b")
    cmd_c = toga.Command(None, text="App command C", id="custom-command-c")

    app.commands.add(cmd_a, cmd_b)

    # Retrieve the custom command by ID.
    assert "custom-command-b" in app.commands
    assert cmd_b in app.commands
    assert app.commands["custom-command-b"] == cmd_b

    # Look up a command that *hasn't* been added to the app
    assert "custom-command-c" not in app.commands
    assert cmd_c not in app.commands
    with pytest.raises(KeyError):
        app.commands["custom-command-c"]

    # Check a system installed command
    assert toga.Command.ABOUT in app.commands
    assert app.commands[toga.Command.ABOUT].text == "About Test App"


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_delitem(change_handler):
    """A command can be deleted by ID."""
    cs = CommandSet(on_change=change_handler)

    # Define some commands
    cmd_a = toga.Command(None, text="App command a", id="custom-command-a")
    cmd_b = toga.Command(None, text="App command b", id="custom-command-b")
    cs.add(cmd_a, cmd_b)
    if change_handler:
        change_handler.reset_mock()

    # Delete one of the commands
    del cs["custom-command-a"]

    # The deleted command is no longer in the command set.
    assert "custom-command-a" not in cs
    assert cmd_a not in cs
    # Change handler was invoked
    if change_handler:
        change_handler.assert_called_once_with()


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_delitem_missing(change_handler):
    """If an ID doesn't exist, delitem raises an error."""
    cs = CommandSet(on_change=change_handler)

    # Define some commands
    cmd_a = toga.Command(None, text="App command a", id="custom-command-a")
    cmd_b = toga.Command(None, text="App command b", id="custom-command-b")
    cs.add(cmd_a, cmd_b)
    if change_handler:
        change_handler.reset_mock()

    # Try to delete a command that doesn't exist
    with pytest.raises(KeyError, match=r"does-not-exist"):
        del cs["does-not-exist"]

    # The deleted command is no longer in the command set.
    assert "custom-command-a" in cs
    assert cmd_a in cs
    # Change handler was invoked
    if change_handler:
        change_handler.assert_not_called()


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_discard(change_handler):
    """A command can be discarded."""
    cs = CommandSet(on_change=change_handler)

    # Define some commands
    cmd_a = toga.Command(None, text="App command a", id="custom-command-a")
    cmd_b = toga.Command(None, text="App command b", id="custom-command-b")
    cs.add(cmd_a, cmd_b)
    if change_handler:
        change_handler.reset_mock()

    # discard one of the commands
    cs.discard(cmd_a)

    # The discarded command is no longer in the command set.
    assert "custom-command-a" not in cs
    assert cmd_a not in cs
    # Change handler was invoked
    if change_handler:
        change_handler.assert_called_once_with()


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_discard_missing(change_handler):
    """If a command doesn't exist, discard is an no-op."""
    cs = CommandSet(on_change=change_handler)

    # Define some commands
    cmd_a = toga.Command(None, text="App command a", id="custom-command-a")
    cmd_b = toga.Command(None, text="App command b", id="custom-command-b")
    cs.add(cmd_a, cmd_b)
    if change_handler:
        change_handler.reset_mock()

    # Define a third command that isn't added.
    cmd_c = toga.Command(None, text="App command c", id="custom-command-c")

    # Try to discard a command that doesn't exist; this is a no-op
    cs.discard(cmd_c)

    # Change handler was not invoked
    if change_handler:
        change_handler.assert_not_called()


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_remove(change_handler):
    """A command can be removed from a commandset."""
    cs = CommandSet(on_change=change_handler)

    # Define some commands
    cmd_a = toga.Command(None, text="App command a", id="custom-command-a")
    cmd_b = toga.Command(None, text="App command b", id="custom-command-b")
    cs.add(cmd_a, cmd_b)
    if change_handler:
        change_handler.reset_mock()

    # Remove one of the commands
    cs.remove(cmd_a)

    # The removed command is no longer in the command set.
    assert "custom-command-a" not in cs
    assert cmd_a not in cs
    # Change handler was invoked
    if change_handler:
        change_handler.assert_called_once_with()


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_remove_missing(change_handler):
    """If a command doesn't exist, remove raises an error."""
    cs = CommandSet(on_change=change_handler)

    # Define some commands
    cmd_a = toga.Command(None, text="App command a", id="custom-command-a")
    cmd_b = toga.Command(None, text="App command b", id="custom-command-b")
    cs.add(cmd_a, cmd_b)
    if change_handler:
        change_handler.reset_mock()

    # Define a third command that isn't added.
    cmd_c = toga.Command(None, text="App command c", id="custom-command-c")

    # Try to remove a command that doesn't exist
    with pytest.raises(KeyError, match=str(cmd_c)):
        cs.remove(cmd_c)

    # Change handler was not invoked
    if change_handler:
        change_handler.assert_not_called()


def test_default_command_ordering(app):
    """The default app commands are in a known order."""

    assert [
        (
            (obj.group.text, obj.id)
            if isinstance(obj, toga.Command)
            else "---" if isinstance(obj, Separator) else "?"
        )
        for obj in app.commands
    ] == [
        # App menu
        ("*", toga.Command.EXIT),
        # Help menu
        ("Help", toga.Command.ABOUT),
    ]


def test_ordering(
    parent_group_1,
    parent_group_2,
    child_group_1,
    child_group_2,
    child_group_3,
    child_group_4,
    child_group_5,
):
    """Ordering of groups, separators and commands is preserved."""

    # Menu structure is:
    # - parent group 1
    #   - Z                 - a group that starts with a command
    #   - child group 1
    #     - Y
    #     - X
    #     - W
    #     ---               - a separator between two items
    #     - B
    #   - V
    #   - child group 2
    #     - U
    #     - T
    #   - S
    # - parent group 2
    #   - child group 5     - a group that starts with a child group
    #     - G
    #   - A
    #   ---
    #   - child group 4     - a child group with a separator before it
    #     - E
    #   - child group 3     - a child group with a separator after it
    #     - D
    #   ---
    #   - F
    command_a = toga.Command(None, "A", group=parent_group_2, section=1, order=2)
    command_d = toga.Command(None, "D", group=child_group_3)
    command_e = toga.Command(None, "E", group=child_group_4)
    command_f = toga.Command(None, "F", group=parent_group_2, section=3)
    command_g = toga.Command(None, "G", group=child_group_5, section=1)
    command_b = toga.Command(None, "B", group=child_group_1, section=2, order=1)
    command_s = toga.Command(None, "S", group=parent_group_1, order=5)
    command_t = toga.Command(None, "T", group=child_group_2, order=2)
    command_u = toga.Command(None, "U", group=child_group_2, order=1)
    command_v = toga.Command(None, "V", group=parent_group_1, order=3)
    command_w = toga.Command(None, "W", group=child_group_1, order=4)
    command_x = toga.Command(None, "X", group=child_group_1, order=2)
    command_y = toga.Command(None, "Y", group=child_group_1, order=1)
    command_z = toga.Command(None, "Z", group=parent_group_1, order=1)

    commands = [
        command_z,
        command_y,
        command_x,
        command_w,
        command_b,
        command_v,
        command_u,
        command_t,
        command_s,
        command_e,
        command_f,
        command_d,
        command_a,
        command_g,
    ]

    # First iteration, use the order as defined. Then repeat multiple times
    # to validate insertion order doesn't matter.
    for attempt in range(0, 10):
        if attempt:
            random.shuffle(commands)
        cs = CommandSet()
        cs.add(*commands)

        assert list(cs) == [
            command_z,
            command_y,
            command_x,
            command_w,
            Separator(group=child_group_1),
            command_b,
            command_v,
            command_u,
            command_t,
            command_s,
            command_g,
            command_a,
            Separator(group=parent_group_2),
            command_e,
            command_d,
            Separator(group=parent_group_2),
            command_f,
        ]
