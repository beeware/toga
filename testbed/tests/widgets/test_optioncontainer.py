from unittest.mock import Mock

import pytest

import toga
from toga.colors import CORNFLOWERBLUE, GOLDENROD, REBECCAPURPLE, SEAGREEN
from toga.style.pack import Pack

from .conftest import build_cleanup_test, safe_create
from .probe import get_probe
from .properties import (  # noqa: F401
    test_enable_noop,
    test_flex_widget_size,
    test_focus_noop,
)


@pytest.fixture
async def content1():
    return toga.Box(
        children=[toga.Label("Box 1 content", style=Pack(flex=1))],
        style=Pack(background_color=REBECCAPURPLE),
    )


@pytest.fixture
async def content2():
    return toga.Box(
        children=[toga.Label("Box 2 content", style=Pack(flex=1))],
        style=Pack(background_color=CORNFLOWERBLUE),
    )


@pytest.fixture
async def content3():
    return toga.Box(
        children=[toga.Label("Box 3 content", style=Pack(flex=1))],
        style=Pack(background_color=GOLDENROD),
    )


@pytest.fixture
async def content1_probe(content1):
    return get_probe(content1)


@pytest.fixture
async def content2_probe(content2):
    return get_probe(content2)


@pytest.fixture
async def content3_probe(content3):
    return get_probe(content3)


@pytest.fixture
async def on_select_handler():
    return Mock()


@pytest.fixture
async def widget(content1, content2, content3, on_select_handler):
    with safe_create():
        return toga.OptionContainer(
            content=[
                ("Tab 1", content1, "resources/tab-icon-1"),
                toga.OptionItem(
                    "Tab 2",
                    content2,
                    icon=toga.Icon("resources/tab-icon-2"),
                ),
                ("Tab 3", content3),
            ],
            style=Pack(flex=1),
            on_select=on_select_handler,
        )


test_cleanup = build_cleanup_test(
    # Pass a function here to prevent init of toga.Box() in a different thread than
    # toga.OptionContainer. This would raise a runtime error on Windows.
    lambda: toga.OptionContainer(content=[("Tab 1", toga.Box())]),
    xfail_platforms=("linux",),
)


def assert_tab_text(tab, expected):
    assert tab.text == expected
    assert type(tab.text) is str


async def test_content_size_rehint(
    widget,
    probe,
    content1,
    content1_probe,
    content3,
    main_window,
    main_window_probe,
):
    """The OptionContainer should rehint to minimum size of all widgets plus necessary
    decors, and should automatically rehint upon the addition of new tabs."""
    probe.assert_supports_content_based_rehint()
    main_window.size = (300, 300)
    await main_window_probe.redraw("Main window size should be 300x300")

    content3.width = 500
    content3.height = 600

    # Wait for size of content to change. Use content1 because content3 is not selected,
    # and as a result, may not have a valid size.
    await probe.redraw(
        "Tab 3's size should be explicitly set to 500x600",
        wait_for=lambda: (
            content1_probe.width == pytest.approx(500, abs=2)
            and content1_probe.height == pytest.approx(600, abs=2)
        ),
    )

    assert main_window.size.width >= 500
    assert main_window.size.height > 600
    assert probe.width >= 500
    assert probe.height > 600
    # Asserting content1 for content size because content3, by virtue of not being
    # selected, may have an invalid size.
    assert content1_probe.width == pytest.approx(500, abs=2)
    assert content1_probe.height == pytest.approx(600, abs=2)


async def test_select_tab(
    widget,
    probe,
    on_select_handler,
    content1_probe,
    content2_probe,
    content3_probe,
):
    """Tabs of content can be selected"""
    # Initially selected tab has content that is the full size of the widget
    await probe.wait_for_tab("Tab 1 should be selected")
    assert widget.current_tab.index == 0

    # The content should be the same size as the container; these dimensions can
    # be impacted by the size of tabs and other widget chrome. Test that the
    # content has expanded by asserting that the content is at least 80% the
    # size of the widget.
    assert content1_probe.width > probe.width * 0.8
    assert content1_probe.height > probe.height * 0.8

    # on_select hasn't been invoked.
    on_select_handler.assert_not_called()

    # Select item 1 programmatically
    widget.current_tab = "Tab 2"
    await probe.wait_for_tab("Tab 2 should be selected")

    assert widget.current_tab.index == 1
    assert content2_probe.width > probe.width * 0.8
    assert content2_probe.height > probe.height * 0.8
    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    handler_current_index = -1

    def on_select(widget, **kwargs):
        nonlocal handler_current_index
        handler_current_index = widget.current_tab.index

    on_select_handler.side_effect = on_select

    # Select item 2 in the GUI
    probe.select_tab(2)
    await probe.wait_for_tab("Tab 3 should be selected")

    assert widget.current_tab.index == 2
    assert content3_probe.width > probe.width * 0.8
    assert content3_probe.height > probe.height * 0.8
    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()
    # The current index as evaluated in the handler agrees
    assert handler_current_index == 2


async def test_select_tab_overflow(widget, probe, on_select_handler):
    """If there's a lot of tabs, content can still be selected"""
    # Set up 5 extra tabs
    extra_widgets = [
        toga.Box(
            children=[toga.Label(f"Box {i + 4} content", style=Pack(flex=1))],
            style=Pack(
                background_color={
                    0: CORNFLOWERBLUE,
                    1: GOLDENROD,
                    2: REBECCAPURPLE,
                }[i % 3]
            ),
        )
        for i in range(5)
    ]
    extra_probes = [get_probe(w) for w in extra_widgets]

    # Some platforms (Android) are limited in the number of tabs they can display.
    # Other platforms have no tab limit.
    if probe.max_tabs is None:
        # No tab limit. Add all the extra widgets
        for i, extra in enumerate(extra_widgets, start=4):
            widget.content.append(f"Tab {i}", extra)

        await probe.wait_for_tab("Tab 1 should be selected initially")
        assert widget.current_tab.index == 0

        # Ensure mock call count is clean
        on_select_handler.reset_mock()

        # Some platforms (iOS) have a "more" option for tabs beyond a display limit. If
        # `select_more()` doesn't exist, that feature doesn't exist on the platform.
        try:
            probe.select_more()
            await probe.wait_for_tab("More option should be displayed")
            # When the "more" menu is visible, the current tab is None.
            assert widget.current_tab.index is None
        except AttributeError:
            pass

        # on_select has been not been invoked
        on_select_handler.assert_not_called()

        # Select the second last tab in the GUI
        probe.select_tab(6)
        await probe.wait_for_tab("Tab 7 should be selected")

        assert widget.current_tab.index == 6
        assert extra_probes[3].width > probe.width * 0.8
        assert extra_probes[3].height > probe.height * 0.8

        # on_select has been invoked
        on_select_handler.assert_called_once_with(widget)
        on_select_handler.reset_mock()

        # Select the last tab programmatically while already on a "more" option
        widget.current_tab = "Tab 8"
        await probe.wait_for_tab("Tab 8 should be selected")

        assert widget.current_tab.index == 7
        assert extra_probes[4].width > probe.width * 0.8
        assert extra_probes[4].height > probe.height * 0.8
        # on_select has been invoked
        on_select_handler.assert_called_once_with(widget)
        on_select_handler.reset_mock()

        # Select the first tab in the GUI
        probe.select_tab(0)
        await probe.wait_for_tab("Tab 0 should be selected")
        assert widget.current_tab.index == 0
        # on_select has been invoked
        on_select_handler.assert_called_once_with(widget)
        on_select_handler.reset_mock()

        # Select the "more" option again. If the more option is stateful,
        # this will result is displaying the last "more" option selected
        try:
            probe.select_more()
            if probe.more_option_is_stateful:
                await probe.wait_for_tab("Previous more option should be displayed")
                assert widget.current_tab.index == 7
                # more is stateful, so there's a been a select event for the
                # previously selected "more" option.
                on_select_handler.assert_called_once_with(widget)
                on_select_handler.reset_mock()

                probe.reset_more()
                await probe.wait_for_tab("More option should be reset")
            else:
                await probe.wait_for_tab("More option should be displayed")

            assert widget.current_tab.index is None
        except AttributeError:
            pass

        on_select_handler.assert_not_called()

        # Select the second last tab in the GUI
        probe.select_tab(6)
        await probe.wait_for_tab("Tab 7 should be selected")

        assert widget.current_tab.index == 6
        assert extra_probes[3].width > probe.width * 0.8
        assert extra_probes[3].height > probe.height * 0.8

        # on_select has been invoked
        on_select_handler.assert_called_once_with(widget)
        on_select_handler.reset_mock()

        # Select the first tab in the GUI
        probe.select_tab(0)
        await probe.wait_for_tab("Tab 0 should be selected")
        assert widget.current_tab.index == 0
        # on_select has been invoked
        on_select_handler.assert_called_once_with(widget)
        on_select_handler.reset_mock()

        # Select the last tab programmatically while on a non-more option
        widget.current_tab = "Tab 8"
        await probe.wait_for_tab("Tab 8 should be selected")

        assert widget.current_tab.index == 7
        assert extra_probes[4].width > probe.width * 0.8
        assert extra_probes[4].height > probe.height * 0.8
        # on_select has been invoked. There may be a refresh event
        # associated with the display of the the stateful more option.
        on_select_handler.assert_called_with(widget)
        on_select_handler.reset_mock()
    else:
        # Platform has a tab limit. Add as many tabs as the tab limit allows
        for i in range(4, probe.max_tabs + 1):
            extra = extra_widgets.pop(0)
            extra_probes.pop(0)
            widget.content.append(f"Tab {i}", extra)

        await probe.wait_for_tab("OptionContainer is at capacity")

        # Ensure mock call count is clean
        on_select_handler.reset_mock()

        # Append two more widgets. This raises a warning; the new content will
        # be stored, but not displayed
        with pytest.warns(match=r"Additional item will be ignored"):
            extra = extra_widgets.pop(0)
            extra_probes.pop(0)
            widget.content.append("Tab A", extra)

        with pytest.warns(match=r"Additional item will be ignored"):
            extra = extra_widgets.pop(0)
            extra_probes.pop(0)
            widget.content.append("Tab B", extra)

        await probe.wait_for_tab("Appended items were ignored")

        # Excess tab details can still be read and written
        widget.content[probe.max_tabs].text = "Extra Tab"
        widget.content[probe.max_tabs].icon = "resources/new-tab"
        widget.content[probe.max_tabs].enabled = False

        assert_tab_text(widget.content[probe.max_tabs], "Extra Tab")
        probe.assert_tab_icon(probe.max_tabs, "new-tab")
        assert not widget.content[probe.max_tabs].enabled

        assert_tab_text(widget.content[probe.max_tabs + 1], "Tab B")
        probe.assert_tab_icon(probe.max_tabs + 1, None)
        assert widget.content[probe.max_tabs + 1].enabled

        # Programmatically selecting a non-visible tab raises a warning, doesn't change
        # the tab, and doesn't generate a selection event.
        with pytest.warns(match=r"Tab is outside selectable range"):
            widget.current_tab = probe.max_tabs + 1

        await probe.wait_for_tab("Item selection was ignored")
        on_select_handler.assert_not_called()

        # Insert a tab at the start. This will bump the last tab into the void
        with pytest.warns(match=r"Excess items will be ignored"):
            extra = extra_widgets.pop(0)
            extra_probes.pop(0)
            widget.content.insert(2, "Tab C", extra)

        await probe.wait_for_tab("Inserted item bumped the last item")

        # Assert the properties of the last visible item
        assert_tab_text(widget.content[probe.max_tabs - 1], f"Tab {probe.max_tabs - 1}")
        probe.assert_tab_icon(probe.max_tabs - 1, None)
        assert widget.content[probe.max_tabs - 1].enabled

        # As the item is visible, also verify the actual widget properties
        probe.assert_tab_content(
            probe.max_tabs - 1,
            f"Tab {probe.max_tabs - 1}",
            enabled=True,
        )

        # Assert the properties of the first invisible item
        assert_tab_text(widget.content[probe.max_tabs], f"Tab {probe.max_tabs}")
        probe.assert_tab_icon(probe.max_tabs, None)
        assert widget.content[probe.max_tabs].enabled

        # Remove a visible tab. This will bring the tab that was bumped by
        # the previous insertion back into view.
        widget.content.remove(1)

        await probe.wait_for_tab("Deleting an item restores previously bumped item")

        assert_tab_text(widget.content[probe.max_tabs - 1], f"Tab {probe.max_tabs}")
        probe.assert_tab_icon(probe.max_tabs - 1, None)
        assert widget.content[probe.max_tabs - 1].enabled

        # As the item is visible, also verify the actual widget properties
        probe.assert_tab_content(
            probe.max_tabs - 1,
            f"Tab {probe.max_tabs}",
            enabled=True,
        )

        # Remove another visible tab. This will make the first "extra" tab
        # come into view for the first time. It has a custom icon, and
        # was disabled while it wasn't visible.
        widget.content.remove(1)

        await probe.wait_for_tab("Deleting an item creates a previously excess item")

        assert_tab_text(widget.content[probe.max_tabs - 1], "Extra Tab")
        probe.assert_tab_icon(probe.max_tabs - 1, "new-tab")
        assert not widget.content[probe.max_tabs - 1].enabled

        # As the item is visible, also verify the actual widget properties
        probe.assert_tab_content(
            probe.max_tabs - 1,
            "Extra Tab",
            enabled=False,
        )


async def test_enable_tab(widget, probe, on_select_handler):
    """Tabs of content can be enabled and disabled"""
    # All tabs are enabled, current tab is 0
    assert widget.current_tab.index == 0
    assert widget.content[0].enabled
    assert widget.content[1].enabled

    # on_select hasn't been invoked.
    on_select_handler.assert_not_called()

    # Disable item 1
    widget.content[1].enabled = False
    await probe.wait_for_tab("Tab 2 should be disabled")

    assert widget.content[0].enabled
    assert not widget.content[1].enabled
    assert probe.tab_enabled(0)
    assert not probe.tab_enabled(1)

    # Try to select a disabled tab
    probe.select_tab(1)
    await probe.wait_for_tab("Try to select tab 2")

    if probe.disabled_tab_selectable:
        assert widget.current_tab.index == 1
        on_select_handler.assert_called_once_with(widget)
        widget.current_tab = 0
        on_select_handler.reset_mock()
    else:
        assert widget.current_tab.index == 0
        on_select_handler.assert_not_called()

    assert widget.content[0].enabled
    assert not widget.content[1].enabled

    # Disable item 1 again, even though it's disabled
    widget.content[1].enabled = False
    await probe.wait_for_tab("Tab 2 should still be disabled")

    assert widget.content[0].enabled
    assert not widget.content[1].enabled

    # Select tab 3, which is index 2 in the widget's content; but on platforms
    # where disabling a tab means hiding the tab completely, it will be *visual*
    # index 1, but content index 2. Make sure the indices are all correct.
    widget.current_tab = 2
    await probe.wait_for_tab("Tab 3 should be selected")

    assert widget.current_tab.index == 2
    assert_tab_text(widget.current_tab, "Tab 3")

    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Enable item 1
    widget.content[1].enabled = True
    await probe.wait_for_tab("Tab 2 should be enabled")

    assert widget.content[0].enabled
    assert widget.content[1].enabled
    assert probe.tab_enabled(0)
    assert probe.tab_enabled(1)

    # Try to select tab 1
    probe.select_tab(1)
    await probe.wait_for_tab("Tab 1 should be selected")

    assert widget.current_tab.index == 1
    assert widget.content[0].enabled
    assert widget.content[1].enabled

    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Enable item 1 again, even though it's enabled
    widget.content[1].enabled = True
    await probe.wait_for_tab("Tab 2 should still be enabled")

    assert widget.content[0].enabled
    assert widget.content[1].enabled


async def test_change_content(
    widget,
    probe,
    content2,
    content2_probe,
    on_select_handler,
):
    """Tabs of content can be added and removed"""

    # Add new content in an enabled state
    new_box = toga.Box(
        children=[toga.Label("New content", style=Pack(flex=1))],
        style=Pack(background_color=SEAGREEN),
    )
    new_probe = get_probe(new_box)

    widget.content.insert(1, "New tab", new_box, enabled=False)
    await probe.wait_for_tab("New tab has been added disabled")

    assert len(widget.content) == 4
    assert_tab_text(widget.content[1], "New tab")
    assert not widget.content[1].enabled

    # Enable the new content and select it
    widget.content[1].enabled = True
    widget.current_tab = "New tab"
    await probe.wait_for_tab("New tab has been enabled and selected")

    assert widget.current_tab.index == 1
    assert_tab_text(widget.current_tab, "New tab")

    # The content should be the same size as the container; these dimensions can
    # be impacted by the size of tabs and other widget chrome. Test that the
    # content has expanded by asserting that the content is at least 80% the
    # size of the widget.
    assert new_probe.width > probe.width * 0.8
    assert new_probe.height > probe.height * 0.8

    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Change the title of Tab 2
    widget.content["Tab 2"].text = "New 2"
    await probe.wait_for_tab("Tab 2 has been renamed")

    assert_tab_text(widget.content[2], "New 2")

    # Change the icon of Tab 2
    widget.content["New 2"].icon = "resources/new-tab"
    await probe.wait_for_tab("Tab 2 has a new icon")

    probe.assert_tab_icon(2, "new-tab")

    # Clear the icon of Tab 2
    widget.content["New 2"].icon = None
    await probe.wait_for_tab("Tab 2 has the default icon")

    probe.assert_tab_icon(2, None)

    # Remove Tab 2
    widget.content.remove("New 2")
    await probe.wait_for_tab("Tab 2 has been removed")
    assert len(widget.content) == 3

    # Add tab 2 back in at the end with a new title
    widget.content.append("New Tab 2", content2)
    await probe.wait_for_tab("Tab 2 has been added with a new title")

    widget.current_tab = "New Tab 2"
    await probe.wait_for_tab("Revised tab 2 has been selected")

    assert widget.current_tab.index == 3
    assert_tab_text(widget.current_tab, "New Tab 2")
    # The content should be the same size as the container; these dimensions can
    # be impacted by the size of tabs and other widget chrome. Test that the
    # content has expanded by asserting that the content is at least 80% the
    # size of the widget.
    assert content2_probe.width > probe.width * 0.8
    assert content2_probe.height > probe.height * 0.8

    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()
