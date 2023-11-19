import random
from unittest.mock import Mock

import pytest

import toga
from toga.command import CommandSet, Separator


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

    # Command set has no commands.
    assert list(cs) == []

    # App command set hasn't changed.
    assert list(app.commands) == [cmd_a, cmd1b, cmd2, cmd1a, cmd_b]


def test_ordering(
    parent_group_1,
    parent_group_2,
    child_group_1,
    child_group_2,
    child_group_3,
    child_group_4,
    child_group_5,
):
    """Ordering of groups, separators and commands is preserved"""

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
