from unittest.mock import Mock

import pytest

from toga.command import Command
from toga.statusicons import MenuStatusIcon, SimpleStatusIcon, StatusIconSet
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
)


@pytest.fixture
def change_handler():
    return Mock()


@pytest.fixture
def statusiconset(app):
    return StatusIconSet()


def test_create(app):
    """A StatusIconSet can be created with defaults."""
    statusiconset = StatusIconSet()

    assert len(statusiconset) == 0
    assert list(statusiconset) == []
    assert statusiconset._primary_menu_status_icon is None
    assert list(statusiconset._menu_status_icons) == []

    assert len(statusiconset.commands) == 0
    assert statusiconset.commands.on_change is None

    # Create the standard commands on the StatusIconSet
    statusiconset._create_standard_commands()

    assert len(statusiconset.commands) == 2
    assert Command.ABOUT in statusiconset.commands
    assert Command.EXIT in statusiconset.commands


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_add_single(statusiconset, change_handler):
    """A single icon can be added to a StatusIconSet."""
    if change_handler:
        statusiconset.commands.on_change = change_handler

    status_1 = SimpleStatusIcon(id="s1")
    statusiconset.add(status_1)

    assert len(statusiconset) == 1
    assert list(statusiconset) == [status_1]

    assert statusiconset["s1"] == status_1
    assert statusiconset[0] == status_1
    assert statusiconset[-1] == status_1

    assert "s1" in statusiconset
    assert "sX" not in statusiconset

    assert status_1 in statusiconset

    assert_action_performed(status_1, "create")

    if change_handler:
        change_handler.assert_called_once_with()


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_add_multiple(statusiconset, change_handler):
    """Multiple icons can be added to a StatusIconSet."""
    if change_handler:
        statusiconset.commands.on_change = change_handler

    status_1 = SimpleStatusIcon(id="s1")
    status_2 = SimpleStatusIcon(id="s2")
    status_3 = SimpleStatusIcon(id="s3")
    statusiconset.add(status_1, status_2, status_3)

    assert len(statusiconset) == 3
    assert list(statusiconset) == [status_1, status_2, status_3]

    assert statusiconset["s1"] == status_1
    assert statusiconset["s2"] == status_2
    assert statusiconset["s3"] == status_3

    assert statusiconset[0] == status_1
    assert statusiconset[-1] == status_3
    assert statusiconset[1] == status_2
    assert statusiconset[2] == status_3

    assert "s1" in statusiconset
    assert "s2" in statusiconset
    assert "s3" in statusiconset
    assert "sX" not in statusiconset

    assert status_1 in statusiconset
    assert status_2 in statusiconset
    assert status_3 in statusiconset

    assert_action_performed(status_1, "create")
    assert_action_performed(status_2, "create")
    assert_action_performed(status_3, "create")

    if change_handler:
        change_handler.assert_called_once_with()


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_add_existing(statusiconset, change_handler):
    """An existing item cannot be re-added to a StatusIconSet."""
    if change_handler:
        statusiconset.commands.on_change = change_handler

    status_1 = SimpleStatusIcon(id="s1")
    status_2 = SimpleStatusIcon(id="s2")
    status_3 = SimpleStatusIcon(id="s3")
    statusiconset.add(status_1, status_2, status_3)

    assert len(statusiconset) == 3
    assert list(statusiconset) == [status_1, status_2, status_3]
    assert "s2" in statusiconset

    EventLog.reset()
    if change_handler:
        change_handler.reset_mock()

    # Re-adding a status icon is a no-op
    statusiconset.add(status_2)

    assert len(statusiconset) == 3
    assert list(statusiconset) == [status_1, status_2, status_3]
    assert "s2" in statusiconset

    assert_action_not_performed(status_2, "create")

    if change_handler:
        change_handler.assert_not_called()


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_empty_add(statusiconset, change_handler):
    """An empty add is a no-op."""
    if change_handler:
        statusiconset.commands.on_change = change_handler

    statusiconset.add()
    assert len(statusiconset) == 0
    assert list(statusiconset) == []

    if change_handler:
        change_handler.assert_not_called()


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_remove(statusiconset, change_handler):
    """An icon can be removed from a statusiconset."""
    if change_handler:
        statusiconset.commands.on_change = change_handler

    status_1 = SimpleStatusIcon(id="s1")
    status_2 = SimpleStatusIcon(id="s2")
    status_3 = SimpleStatusIcon(id="s3")
    statusiconset.add(status_1, status_2, status_3)

    assert list(statusiconset) == [status_1, status_2, status_3]
    assert len(statusiconset) == 3

    EventLog.reset()
    if change_handler:
        change_handler.reset_mock()

    statusiconset.remove(status_2)

    assert list(statusiconset) == [status_1, status_3]
    assert len(statusiconset) == 2

    assert statusiconset[0] == status_1
    assert statusiconset[-1] == status_3
    assert statusiconset[1] == status_3

    assert "s1" in statusiconset
    assert "s2" not in statusiconset
    assert "s3" in statusiconset
    assert "sX" not in statusiconset

    assert status_1 in statusiconset
    assert status_2 not in statusiconset
    assert status_3 in statusiconset

    if change_handler:
        change_handler.assert_called_once_with()

    assert_action_performed(status_2, "remove")
    EventLog.reset()
    if change_handler:
        change_handler.reset_mock()

    # Removing the same item a second time is an error
    with pytest.raises(ValueError, match=r"Not a known status icon."):
        statusiconset.remove(status_2)

    assert_action_not_performed(status_2, "remove")

    if change_handler:
        change_handler.assert_not_called()


@pytest.mark.parametrize("change_handler", [(None), (Mock())])
def test_clear(statusiconset, change_handler):
    """The statusiconset can be cleared."""
    if change_handler:
        statusiconset.commands.on_change = change_handler

    status_1 = SimpleStatusIcon(id="s1")
    status_2 = SimpleStatusIcon(id="s2")
    status_3 = SimpleStatusIcon(id="s3")
    statusiconset.add(status_1, status_2, status_3)

    assert list(statusiconset) == [status_1, status_2, status_3]
    assert len(statusiconset) == 3

    EventLog.reset()
    if change_handler:
        change_handler.reset_mock()

    statusiconset.clear()
    assert len(statusiconset) == 0
    assert list(statusiconset) == []

    assert "s1" not in statusiconset
    assert "s2" not in statusiconset
    assert "s3" not in statusiconset

    assert status_1 not in statusiconset
    assert status_2 not in statusiconset
    assert status_3 not in statusiconset

    if change_handler:
        change_handler.assert_called_once_with()


def test_menu_status_items(statusiconset):
    """Menu status items can be differentiated from non-menu items."""
    # There are initially no menu status icons
    assert list(statusiconset._menu_status_icons) == []
    assert statusiconset._primary_menu_status_icon is None

    # When the list *only* contains non-menu status icons, nothing is returned
    status_1 = SimpleStatusIcon(id="s1")
    status_2 = SimpleStatusIcon(id="s2")
    status_3 = SimpleStatusIcon(id="s3")
    statusiconset.add(status_1, status_2, status_3)

    assert list(statusiconset._menu_status_icons) == []
    assert statusiconset._primary_menu_status_icon is None

    # When there is a menu status item, the can be filtered out.
    menu_status_1 = MenuStatusIcon(id="m1")
    status_4 = SimpleStatusIcon(id="s4")
    menu_status_2 = MenuStatusIcon(id="m2")
    menu_status_3 = MenuStatusIcon(id="m3")
    statusiconset.add(menu_status_1, status_4, menu_status_2, menu_status_3)

    assert list(statusiconset._menu_status_icons) == [
        menu_status_1,
        menu_status_2,
        menu_status_3,
    ]
    assert statusiconset._primary_menu_status_icon is menu_status_1

    # If a menu status item is removed, others take their place.
    statusiconset.remove(menu_status_1)

    assert list(statusiconset._menu_status_icons) == [menu_status_2, menu_status_3]
    assert statusiconset._primary_menu_status_icon is menu_status_2
