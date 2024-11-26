from unittest.mock import Mock

import pytest

import toga


async def test_add_remove(app, app_probe):
    """Status icons and items can be added and removed."""
    # Assert the structure of the default status items
    assert app_probe.has_status_icon(app.status1)
    assert app_probe.status_menu_items(app.status1) == [
        "Action 1",
        "Sub Menu",
        "Action 2",
        # The standard commands come after a separator;
        # but the text varies depending on the platform.
        "---",
        "**ABOUT**",
        "**EXIT**",
    ]

    assert app_probe.has_status_icon(app.status2)
    assert app_probe.status_menu_items(app.status2) == [
        "Action 5",
        "Action 6",
    ]

    assert app_probe.has_status_icon(app.status_button)
    assert app_probe.status_menu_items(app.status_button) is None

    # Create a new menu status item
    new_status_icon = toga.MenuStatusIcon(text="New Item")
    new_cmd1 = toga.Command(
        Mock(),
        text="New Action 1",
        tooltip="Perform action 1",
        group=new_status_icon,
        order=20,
    )
    await app_probe.redraw("Status icon created but not added")
    assert not app_probe.has_status_icon(new_status_icon)

    # Add the command to the status command set. It won't have any commands yet.
    app.status_icons.add(new_status_icon)
    await app_probe.redraw("Status icon added")
    assert app_probe.has_status_icon(new_status_icon)
    assert app_probe.status_menu_items(new_status_icon) == []

    # Add the command to the status command set.
    app.status_icons.commands.add(new_cmd1)
    await app_probe.redraw("Command added, but not visible")
    assert app_probe.has_status_icon(new_status_icon)
    assert app_probe.status_menu_items(new_status_icon) == [
        "New Action 1",
    ]

    # A second command
    new_cmd2 = toga.Command(
        Mock(),
        text="New Action 2",
        tooltip="Perform new action 2",
        group=new_status_icon,
        order=10,
    )
    app.status_icons.commands.add(new_cmd2)
    await app_probe.redraw("Second command added")
    assert app_probe.has_status_icon(new_status_icon)
    assert app_probe.status_menu_items(new_status_icon) == [
        "New Action 2",
        "New Action 1",
    ]

    # Remove the first command
    app.status_icons.commands.remove(new_cmd1)
    await app_probe.redraw("First command removed")
    assert app_probe.has_status_icon(new_status_icon)
    assert app_probe.status_menu_items(new_status_icon) == [
        "New Action 2",
    ]

    # Remove the second command
    app.status_icons.commands.remove(new_cmd2)
    await app_probe.redraw("Second command removed")
    assert app_probe.has_status_icon(new_status_icon)
    assert app_probe.status_menu_items(new_status_icon) == []

    # Remove the extra status icon
    app.status_icons.remove(new_status_icon)
    await app_probe.redraw("Status icon removed")
    assert not app_probe.has_status_icon(new_status_icon)


async def test_unknown_status_icon(app, app_probe):
    """Adding a command when the status icon is unknown raises an error."""
    # Verify the app status icons are present. This enforces the test skip
    # if the platform doesn't support status icons.
    assert app_probe.has_status_icon(app.status1)

    # Create a new menu status item
    absent_status_icon = toga.MenuStatusIcon(text="Absent Item")
    bad_cmd = toga.Command(
        Mock(),
        text="Bad Action",
        group=absent_status_icon,
    )

    # Add the command without adding the status icon first
    try:
        with pytest.raises(
            ValueError,
            match=(
                r"Command 'Bad Action' "
                r"does not belong to a current status icon group."
            ),
        ):
            app.status_icons.commands.add(bad_cmd)
    finally:
        # Clean up and make sure the bad command is removed.
        app.status_icons.commands.remove(bad_cmd)


async def test_activate_button_icon(app, app_probe):
    """A button status icon can be activated."""
    app_probe.activate_status_icon_button("button")
    await app_probe.redraw("Pressed status icon button")

    app.cmd_action.assert_called_once_with(app.status_icons["button"])


async def test_activate_status_menu_item(app, app_probe):
    """A menu status item can be activated."""
    app_probe.activate_status_menu_item("second", "Action 5")
    await app_probe.redraw("Pressed menu status item")

    app.cmd_action.assert_called_once_with(app.status_cmd5)
