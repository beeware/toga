import random
from unittest.mock import Mock

import pytest

import toga
from toga.command import GROUP_BREAK, SECTION_BREAK, CommandSet


def test_create():
    """A CommandSet can be created with defaults"""
    cs = CommandSet()

    assert list(cs) == []
    assert cs.on_change is None


def test_create_with_values():
    """A CommandSet can be created with values"""
    change_handler = Mock()
    cs = CommandSet(on_change=change_handler)

    assert list(cs) == []
    assert cs.on_change == change_handler


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_add_clear(app, change_handler):
    """Commands can be added and removed from a commandset"""
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
    """Commands can be added and removed from a commandset that is linked to an app"""
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

    # Command set no commands.
    assert list(cs) == []

    # App command set hasn't changed.
    assert list(app.commands) == [cmd_a, cmd1b, cmd2, cmd1a, cmd_b]


def test_ordering(parent_group_1, parent_group_2, child_group_1, child_group_2):
    """Ordering of groups, breaks and commands is preserved"""

    command_a = toga.Command(None, "A", group=parent_group_2, order=1)
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
        command_a,
    ]

    # Do this a couple of times to make sure insertion order doesn't matter
    for _ in range(0, 10):
        random.shuffle(commands)
        cs = CommandSet()
        cs.add(*commands)

        assert list(cs) == [
            command_z,
            GROUP_BREAK,
            command_y,
            command_x,
            command_w,
            SECTION_BREAK,
            command_b,
            GROUP_BREAK,
            command_v,
            GROUP_BREAK,
            command_u,
            command_t,
            GROUP_BREAK,
            command_s,
            GROUP_BREAK,
            command_a,
        ]
