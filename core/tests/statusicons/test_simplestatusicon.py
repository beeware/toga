from pathlib import Path
from unittest.mock import Mock

import pytest

import toga
from toga import SimpleStatusIcon
from toga_dummy.utils import assert_action_not_performed, assert_action_performed


def test_create(app):
    """A group can be created with defaults."""
    status_icon = SimpleStatusIcon()

    assert status_icon.id.startswith("statusicon-")
    assert status_icon.icon is None
    assert status_icon.text == "Test App"
    assert status_icon.on_press._raw is None

    assert repr(status_icon).startswith("<SimpleStatusIcon 'Test App': statusicon-")

    # Status icon wasn't created as a result of being instantiated
    assert_action_not_performed(status_icon, "create")
    # ... but an icon was set.
    assert_action_performed(status_icon, "set icon")


@pytest.mark.parametrize("construct_icon", [True, False])
def test_create_with_params(app, construct_icon):
    """A fully specified SimpleStatusIcon can be created."""
    if construct_icon:
        icon = toga.Icon("path/to/icon")
    else:
        icon = "path/to/icon"

    press_handler = Mock()

    status_icon = SimpleStatusIcon(
        id="my-statusicon",
        icon=icon,
        text="My StatusIcon",
        on_press=press_handler,
    )

    assert status_icon.id == "my-statusicon"
    assert status_icon.text == "My StatusIcon"
    assert status_icon.on_press._raw == press_handler

    assert isinstance(status_icon.icon, toga.Icon)
    assert status_icon.icon.path == Path("path/to/icon")

    assert repr(status_icon) == "<SimpleStatusIcon 'My StatusIcon': my-statusicon>"

    # Status icon wasn't created as a result of being instantiated
    assert_action_not_performed(status_icon, "create")
    # ... but an icon was set.
    assert_action_performed(status_icon, "set icon")
