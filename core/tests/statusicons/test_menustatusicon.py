from pathlib import Path

import pytest

import toga
from toga import MenuStatusIcon
from toga_dummy.utils import assert_action_not_performed, assert_action_performed


def test_create(app):
    """A group can be created with defaults."""
    status_icon = MenuStatusIcon()

    # StatusIcon properties
    assert status_icon.icon is None

    # Group properties
    assert status_icon.text == "Test App"
    assert status_icon.id.startswith("menustatusitem-")
    assert status_icon.order == 0
    assert status_icon.section == 0
    assert status_icon.parent is None

    assert repr(status_icon).startswith("<MenuStatusIcon 'Test App': menustatusitem-")

    # Status icon wasn't created as a result of being instantiated
    assert_action_not_performed(status_icon, "create")
    # ... but an icon was set.
    assert_action_performed(status_icon, "set icon")


@pytest.mark.parametrize("construct_icon", [True, False])
def test_create_with_params(app, construct_icon):
    """A fully specified MenuStatusIcon can be created."""
    if construct_icon:
        icon = toga.Icon("path/to/icon")
    else:
        icon = "path/to/icon"

    status_icon = MenuStatusIcon(
        id="my-menustatusicon",
        icon=icon,
        text="My MenuStatusIcon",
    )

    # StatusIcon properties
    assert isinstance(status_icon.icon, toga.Icon)
    assert status_icon.icon.path == Path("path/to/icon")

    assert status_icon._impl.interface == status_icon

    assert (
        repr(status_icon) == "<MenuStatusIcon 'My MenuStatusIcon': my-menustatusicon>"
    )

    # Group properties
    assert status_icon.text == "My MenuStatusIcon"
    assert status_icon.id == "my-menustatusicon"
    assert status_icon.order == 0
    assert status_icon.section == 0
    assert status_icon.parent is None

    # Status icon wasn't created as a result of being instantiated
    assert_action_not_performed(status_icon, "create")
    # ... but an icon was set.
    assert_action_performed(status_icon, "set icon")
