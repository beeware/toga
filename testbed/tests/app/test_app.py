from unittest.mock import Mock

import toga


async def test_main_window_toolbar(app, main_window, main_window_probe):
    """A toolbar can be added to a main window"""
    # Add some items to show the toolbar
    assert not main_window_probe.has_toolbar()
    main_window.toolbar.add(app.cmd1, app.cmd2)

    # Add some more items to an existing toolbar
    main_window.toolbar.add(app.cmd3, app.cmd4)

    await main_window_probe.redraw("Main window has a toolbar")
    assert main_window_probe.has_toolbar()
    # Ordering is lexicographical for cmd 2 and 3.
    main_window_probe.assert_toolbar_item(
        0,
        label="Full command",
        tooltip="A full command definition",
        has_icon=True,
        enabled=True,
    )
    main_window_probe.assert_is_toolbar_separator(1)
    main_window_probe.assert_toolbar_item(
        2,
        label="No Icon",
        tooltip="A command with no icon",
        has_icon=False,
        enabled=True,
    )
    main_window_probe.assert_toolbar_item(
        3,
        label="No Tooltip",
        tooltip=None,
        has_icon=True,
        enabled=True,
    )
    main_window_probe.assert_is_toolbar_separator(4, section=True)
    main_window_probe.assert_toolbar_item(
        5,
        label="Sectioned",
        tooltip="I'm in another section",
        has_icon=True,
        enabled=True,
    )

    # Press the first toolbar button
    main_window_probe.press_toolbar_button(0)
    await main_window_probe.redraw("Command 1 invoked")
    app.cmd_action.assert_called_once_with(app.cmd1)
    app.cmd_action.reset_mock()

    # Disable the first toolbar button
    app.cmd1.enabled = False
    await main_window_probe.redraw("Command 1 disabled")
    main_window_probe.assert_toolbar_item(
        0,
        label="Full command",
        tooltip="A full command definition",
        has_icon=True,
        enabled=False,
    )

    # Re-enable the first toolbar button
    app.cmd1.enabled = True
    await main_window_probe.redraw("Command 1 re-enabled")
    main_window_probe.assert_toolbar_item(
        0,
        label="Full command",
        tooltip="A full command definition",
        has_icon=True,
        enabled=True,
    )

    # Remove the toolbar
    main_window.toolbar.clear()
    await main_window_probe.redraw("Main window has no toolbar")
    assert not main_window_probe.has_toolbar()

    # Removing it again should have no effect
    main_window.toolbar.clear()
    await main_window_probe.redraw("Main window has no toolbar")
    assert not main_window_probe.has_toolbar()


async def test_system_menus(app_probe):
    """System-specific menus behave as expected"""
    # Check that the system menus (which can be platform specific) exist.
    app_probe.assert_system_menus()


async def test_menu_about(monkeypatch, app, app_probe):
    """The about menu can be displayed"""
    app_probe.activate_menu_about()
    # When in CI, Cocoa needs a little time to guarantee the dialog is displayed.
    await app_probe.redraw("About dialog shown", delay=0.1)

    await app_probe.close_about_dialog()
    await app_probe.redraw("About dialog destroyed")

    # Make the app definition minimal to verify the dialog still displays
    monkeypatch.setattr(app, "_author", None)
    monkeypatch.setattr(app, "_version", None)
    monkeypatch.setattr(app, "_home_page", None)
    monkeypatch.setattr(app, "_description", None)

    app_probe.activate_menu_about()
    # When in CI, Cocoa needs a little time to guarantee the dialog is displayed.
    await app_probe.redraw("About dialog with no details shown", delay=0.1)

    await app_probe.close_about_dialog()
    await app_probe.redraw("About dialog with no details destroyed")


async def test_menu_visit_homepage(monkeypatch, app, app_probe):
    """The visit homepage menu item can be used"""
    # If the backend defines a VISIT_HOMEPAGE command, mock the visit_homepage method,
    # and rebind the visit homepage command to the visit_homepage method.
    visit_homepage = Mock()
    if toga.Command.VISIT_HOMEPAGE in app.commands:
        monkeypatch.setattr(app, "visit_homepage", visit_homepage)
        monkeypatch.setattr(
            app.commands[toga.Command.VISIT_HOMEPAGE], "_action", app.visit_homepage
        )

    app_probe.activate_menu_visit_homepage()

    # Browser opened
    visit_homepage.assert_called_once_with()


async def test_menu_items(app, app_probe):
    """Menu items can be created, disabled and invoked"""

    app_probe.assert_menu_item(
        ["Other", "Full command"],
        enabled=True,
    )
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "Disabled"],
        enabled=False,
    )
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "No Action"],
        enabled=False,
    )
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "Submenu1 menu1", "Deep"],
        enabled=True,
    )
    app_probe.assert_menu_item(
        ["Other", "Wiggle"],
        enabled=True,
    )

    app_probe.assert_menu_order(
        ["Other"],
        ["Full command", "---", "Submenu1", "Submenu2", "Wiggle"],
    )
    app_probe.assert_menu_order(
        ["Other", "Submenu1"],
        ["Disabled", "No Action", "Submenu1 menu1"],
    )
    app_probe.assert_menu_order(
        ["Other", "Submenu1", "Submenu1 menu1"],
        ["Deep"],
    )
    app_probe.assert_menu_order(
        ["Other", "Submenu2"],
        ["Jiggle"],
    )

    app_probe.assert_menu_item(
        ["Commands", "No Tooltip"],
        enabled=True,
    )
    app_probe.assert_menu_item(
        ["Commands", "No Icon"],
        enabled=True,
    )
    app_probe.assert_menu_item(
        ["Commands", "Sectioned"],
        enabled=True,
    )

    # Enabled the disabled items
    app.disabled_cmd.enabled = True
    app.no_action_cmd.enabled = True
    await app_probe.redraw("Menu items enabled")

    app_probe.assert_menu_item(
        ["Other", "Submenu1", "Disabled"],
        enabled=True,
    )
    # Item has no action - it can't be enabled
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "No Action"],
        enabled=False,
    )

    # Disable the items
    app.disabled_cmd.enabled = False
    app.no_action_cmd.enabled = False

    await app_probe.redraw("Menu item disabled again")
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "Disabled"],
        enabled=False,
    )
    app_probe.assert_menu_item(
        ["Other", "Submenu1", "No Action"],
        enabled=False,
    )


async def test_beep(app):
    """The machine can go Bing!"""
    # This isn't a very good test. It ensures coverage, which verifies that the method
    # can be invoked without raising an error, but there's no way to verify that the app
    # actually made a noise.
    app.beep()


async def test_screens(app, app_probe):
    """Screens must have unique origins and names, with the primary screen at (0,0)."""

    # Get the origin of screen 0
    assert app.screens[0].origin == (0, 0)

    # Check for unique names
    screen_names = [s.name for s in app.screens]
    unique_names = set(screen_names)
    assert len(screen_names) == len(unique_names)

    # Check that the origin of every other screen is not "0,0"
    origins_not_zero = all(screen.origin != (0, 0) for screen in app.screens[1:])
    assert origins_not_zero is True


async def test_app_icon(app, app_probe):
    """The app icon can be changed."""
    # Icon is initially the default
    app_probe.assert_app_icon(None)

    # Change the icon to an alternate
    app.icon = "resources/alt-icon"
    await app_probe.redraw("Set app icon to alternate")
    app_probe.assert_app_icon("resources/alt-icon")

    # Reset the icon to the default
    app.icon = toga.Icon.APP_ICON
    await app_probe.redraw("Revert app icon to default")
    app_probe.assert_app_icon(None)


@pytest.mark.skipif(
    toga.platform.current_platform != "windows", reason="This test is Windows specific"
)
async def test_system_dpi_change(
    monkeypatch, app, app_probe, main_window, main_window_probe
):
    # Store original window content
    main_window_content_original = main_window.content

    from toga_winforms.libs import shcore

    GetScaleFactorForMonitor_original = getattr(shcore, "GetScaleFactorForMonitor")

    def set_mock_dpi_scale(value):
        def GetScaleFactorForMonitor_mock(hMonitor, pScale):
            pScale.value = int(value * 100)

        monkeypatch.setattr(
            "toga_winforms.libs.shcore.GetScaleFactorForMonitor",
            GetScaleFactorForMonitor_mock,
        )

    dpi_change_events = [
        app._impl.winforms_DisplaySettingsChanged,
        main_window._impl.winforms_LocationChanged,
        main_window._impl.winforms_Resize,
    ]
    for flex_direction in ("row", "column"):
        main_window.content = toga.Box(
            style=Pack(direction=flex_direction),
            children=[
                toga.Box(style=Pack(flex=1)),
                toga.Button(text="hello"),
                toga.Label(text="toga"),
                toga.Button(text="world"),
                toga.Box(style=Pack(flex=1)),
            ],
        )
        widget_dimension_to_compare = "width" if flex_direction == "row" else "height"
        await main_window_probe.redraw(
            "\nMain Window is ready for testing DPI scaling with "
            f"window content flex direction set to: {flex_direction}"
        )
        for dpi_change_event in dpi_change_events:
            print(
                f"\nRunning DPI change event: {dpi_change_event.__func__.__qualname__}"
            )

            # Set initial DPI scale value
            set_mock_dpi_scale(1.0)
            dpi_change_events[0](None, None)
            await main_window_probe.redraw(
                "Setting initial DPI scale value to 1.0 before starting DPI scale testing"
            )

            for pScale_value_mock in (1.25, 1.5, 1.75, 2.0):
                # Store original widget dimension
                original_widget_dimension = dict()
                for widget in main_window.content.children:
                    widget_probe = get_probe(widget)
                    original_widget_dimension[widget] = getattr(
                        widget_probe, widget_dimension_to_compare
                    )

                set_mock_dpi_scale(pScale_value_mock)
                # Trigger DPI change event
                dpi_change_event(None, None)
                await main_window_probe.redraw(
                    f"Triggering DPI change event for testing scaling at {pScale_value_mock} scale"
                )

                # Check Widget size DPI scaling
                for widget in main_window.content.children:
                    if isinstance(widget, toga.Box):
                        # Dimension of spacer boxes should decrease when dpi scale increases
                        getattr(
                            get_probe(widget), widget_dimension_to_compare
                        ) < original_widget_dimension[widget]
                    else:
                        # Dimension of other widgets should increase when dpi scale increases
                        getattr(
                            get_probe(widget), widget_dimension_to_compare
                        ) > original_widget_dimension[widget]

    # Restore original state
    monkeypatch.setattr(
        "toga_winforms.libs.shcore.GetScaleFactorForMonitor",
        GetScaleFactorForMonitor_original,
    )
    dpi_change_events[0](None, None)
    main_window.content.window = None
    main_window.content = main_window_content_original
    main_window.show()
    await main_window_probe.redraw("\nRestoring original state of Main Window")
