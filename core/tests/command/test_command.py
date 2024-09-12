from pathlib import Path
from unittest.mock import Mock

import pytest

import toga
from toga.command import Separator
from toga_dummy.utils import assert_action_performed_with


def assert_order(*items):
    for i in range(0, len(items) - 1):
        for j in range(i + 1, len(items)):
            assert items[i] < items[j]
            assert items[j] > items[i]

            # For good measure; check comparisons with other types
            assert not items[i] < None
            assert not items[i] < 42
            assert not items[i] > None
            assert not items[i] > 42


def test_separator(parent_group_1):
    """A separator can be created."""

    separator = Separator(group=parent_group_1)
    assert repr(separator) == "<Separator group=P1>"


def test_separator_eq(parent_group_1, parent_group_2):
    """Separator objects can be compared for equality."""

    separator_1a = Separator(parent_group_1)
    separator_1b = Separator(parent_group_1)
    separator_2 = Separator(parent_group_2)

    # Separators are equal to breaks in the same section, but not to other
    # sections
    assert separator_1a == separator_1a
    assert separator_1a == separator_1b
    assert separator_1a != separator_2

    # Separators aren't equal to non-separator objects
    assert separator_1a != 3


def test_create():
    """A command can be created with defaults."""
    cmd = toga.Command(None, "Test command")

    assert cmd.text == "Test command"
    assert cmd.shortcut is None
    assert cmd.tooltip is None
    assert cmd.group == toga.Group.COMMANDS
    assert cmd.section == 0
    assert cmd.order == 0
    assert cmd.action._raw is None

    assert (
        repr(cmd)
        == "<Command text='Test command' group=<Group text='Commands' order=30> section=0 order=0>"
    )


def test_standard_command(app):
    """A standard command can be created."""
    cmd = toga.Command.standard(app, toga.Command.ABOUT)

    assert cmd.text == "About Test App"
    assert cmd.shortcut is None
    assert cmd.tooltip is None
    assert cmd.group == toga.Group.HELP
    assert cmd.section == 0
    assert cmd.order == 0
    assert cmd.id == toga.Command.ABOUT
    # Connected to the app's about method, as a wrapped simple handler
    assert cmd.action._raw._raw == app.about


def test_standard_command_override(app):
    """A standard command can be created with overrides."""
    action = Mock()
    cmd = toga.Command.standard(app, toga.Command.ABOUT, action=action, section=1)

    assert cmd.text == "About Test App"
    assert cmd.shortcut is None
    assert cmd.tooltip is None
    assert cmd.group == toga.Group.HELP
    assert cmd.order == 0
    assert cmd.id == toga.Command.ABOUT
    # Overrides have been applied
    assert cmd.action._raw == action
    assert cmd.section == 1


def test_unknown_standard_command(app):
    """An unknown standard command raises an exception"""
    with pytest.raises(ValueError, match=r"Unknown standard command 'mystery'"):
        toga.Command.standard(app, "mystery")


def test_change_action():
    """A command's action can be changed to another handler."""
    action1 = Mock()

    cmd = toga.Command(action1, "Test command")

    assert cmd.text == "Test command"
    assert cmd.shortcut is None
    assert cmd.tooltip is None
    assert cmd.group == toga.Group.COMMANDS
    assert cmd.section == 0
    assert cmd.order == 0
    assert cmd.id.startswith("cmd-")
    assert cmd.action._raw == action1

    # Change the action to a something new
    action2 = Mock()
    cmd.action = action2

    assert cmd.action._raw == action2

    # Clear the action
    cmd.action = None
    assert cmd.action._raw is None


def test_create_explicit(app):
    """A command can be created with explicit arguments."""
    grp = toga.Group("Test group", order=10)

    handler = Mock()
    cmd = toga.Command(
        handler,
        text="Test command",
        tooltip="This is a test command",
        shortcut="t",
        group=grp,
        section=3,
        order=4,
        id="slartibartfast",
    )

    assert cmd.text == "Test command"
    assert cmd.shortcut == "t"
    assert cmd.tooltip == "This is a test command"
    assert cmd.group == grp
    assert cmd.section == 3
    assert cmd.order == 4
    assert cmd.id == "slartibartfast"

    assert cmd.action._raw == handler

    assert (
        repr(cmd)
        == "<Command text='Test command' group=<Group text='Test group' order=10> section=3 order=4>"
    )


@pytest.mark.parametrize("construct", [True, False])
def test_icon_construction(app, construct):
    """The command icon can be set during construction."""
    if construct:
        icon = toga.Icon("path/to/icon")
    else:
        icon = "path/to/icon"

    cmd = toga.Command(None, "Test command", icon=icon)
    assert isinstance(cmd.icon, toga.Icon)
    assert cmd.icon.path == Path("path/to/icon")


@pytest.mark.parametrize("construct", [True, False])
def test_icon(app, construct):
    """The command icon can be changed."""
    if construct:
        icon = toga.Icon("path/to/icon")
    else:
        icon = "path/to/icon"

    cmd = toga.Command(None, "Test command")

    # No icon by default
    assert cmd.icon is None

    # Change icon
    cmd.icon = icon

    # Icon path matches
    assert isinstance(cmd.icon, toga.Icon)
    assert cmd.icon.path == Path("path/to/icon")


@pytest.mark.parametrize(
    "action, enabled, initial_state",
    [
        (Mock(), True, True),
        (Mock(), False, False),
        (None, True, False),
        (None, False, False),
    ],
)
def test_enable(action, enabled, initial_state):
    cmd = toga.Command(action, text="Test command", enabled=enabled)

    assert cmd.enabled is initial_state

    # Set enabled; triggers an implementation response
    cmd.enabled = True
    assert_action_performed_with(cmd, "set enabled", value=True)

    # Disable; triggers an implementation response
    cmd.enabled = False
    assert_action_performed_with(cmd, "set enabled", value=False)

    # Disable again; triggers an implementation response
    cmd.enabled = False
    assert_action_performed_with(cmd, "set enabled", value=False)

    # Set enabled; triggers an implementation response
    cmd.enabled = True
    assert_action_performed_with(cmd, "set enabled", value=True)


def test_order_by_text():
    """Commands are ordered by text when group, section and order match."""
    assert_order(
        toga.Command(None, "A"),
        toga.Command(None, "B"),
    )


def test_order_by_number():
    """Commands are ordered by number when group and section match."""
    assert_order(
        toga.Command(None, "B", order=1),
        toga.Command(None, "A", order=2),
    )


def test_order_by_section(parent_group_1):
    """Section ordering takes priority over order and text."""
    assert_order(
        toga.Command(None, "B", group=parent_group_1, section=1, order=2),
        toga.Command(None, "A", group=parent_group_1, section=2, order=1),
    )


def test_order_by_groups(parent_group_1, parent_group_2, child_group_1, child_group_2):
    """Commands are ordered by group over."""

    command_z = toga.Command(None, "Z", group=parent_group_1, order=1)
    command_y = toga.Command(None, "Y", group=child_group_1, order=1)
    command_x = toga.Command(None, "X", group=child_group_1, order=2)
    command_w = toga.Command(None, "W", group=child_group_1, order=4)
    command_b = toga.Command(None, "B", group=child_group_1, section=2, order=1)
    command_v = toga.Command(None, "V", group=parent_group_1, order=3)
    command_u = toga.Command(None, "U", group=child_group_2, order=1)
    command_t = toga.Command(None, "T", group=child_group_2, order=2)
    command_s = toga.Command(None, "S", group=parent_group_1, order=5)
    command_a = toga.Command(None, "A", group=parent_group_2, order=1)

    assert_order(
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
    )
