from unittest.mock import Mock

import pytest

import toga
from toga.colors import CORNFLOWERBLUE, GOLDENROD, REBECCAPURPLE, SEAGREEN
from toga.style.pack import Pack

from ..conftest import skip_on_platforms
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
    skip_on_platforms("android")
    return toga.OptionContainer(
        content=[("Tab 1", content1), ("Tab 2", content2), ("Tab 3", content3)],
        style=Pack(flex=1),
        on_select=on_select_handler,
    )


async def test_select_tab(
    widget,
    probe,
    on_select_handler,
    container_probe,
    content1_probe,
    content2_probe,
    content3_probe,
):
    """Tabs of content can be selected"""
    # Initially selected tab has content that is the full size of the widget
    await probe.redraw("Tab 1 should be selected")
    assert widget.current_tab.index == 0

    # The content should be the same size as the container; this is simple to
    # test in width, but the height can be impacted by the size of the tabs
    # themselves. Test that the content has expanded; but for height, check that
    # the size is > 80% of the container (allowing up to 20% for tabs)
    assert content1_probe.width == pytest.approx(container_probe.width, abs=2)
    assert content1_probe.height > container_probe.height * 0.8

    # on_select hasn't been invoked.
    on_select_handler.assert_not_called()

    # Select item 1 programmatically
    widget.current_tab = "Tab 2"
    await probe.redraw("Tab 2 should be selected")

    assert widget.current_tab.index == 1
    assert content2_probe.width == pytest.approx(container_probe.width, abs=2)
    assert content2_probe.height > container_probe.height * 0.8
    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Select item 2 in the GUI
    probe.select_tab(2)
    await probe.redraw("Tab 3 should be selected")

    assert widget.current_tab.index == 2
    assert content3_probe.width == pytest.approx(container_probe.width, abs=2)
    assert content3_probe.height > container_probe.height * 0.8
    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()


async def test_select_tab_overflow(
    widget,
    probe,
    on_select_handler,
    container_probe,
):
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
        for i in range(0, 5)
    ]
    extra_probes = [get_probe(w) for w in extra_widgets]

    # Add the extra widgets
    for i, extra in enumerate(extra_widgets, start=4):
        widget.content.append(f"Tab {i}", extra)

    await probe.redraw("Tab 1 should be selected initially")
    assert widget.current_tab.index == 0

    # Ensure mock call count is clean
    on_select_handler.reset_mock()

    # Some platforms have a "more" option for tabs beyond a display limit. If
    # `select_more()` doesn't exist, that feature doesn't exist on the platform.
    try:
        probe.select_more()
        await probe.redraw("More option should be displayed")
        # When the "more" menu is visible, the current tab is None.
        assert widget.current_tab.index is None
    except AttributeError:
        pass

    # on_select has been not been invoked
    on_select_handler.assert_not_called()

    # Select the second last tab in the GUI
    probe.select_tab(6)
    await probe.redraw("Tab 7 should be selected")

    assert widget.current_tab.index == 6
    assert extra_probes[3].width == pytest.approx(container_probe.width, abs=2)
    assert extra_probes[3].height > container_probe.height * 0.8

    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Select the last tab programmatically while already on a "more" option
    widget.current_tab = "Tab 8"
    await probe.redraw("Tab 8 should be selected")

    assert widget.current_tab.index == 7
    assert extra_probes[4].width == pytest.approx(container_probe.width, abs=2)
    assert extra_probes[4].height > container_probe.height * 0.8
    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Select the first tab in the GUI
    probe.select_tab(0)
    await probe.redraw("Tab 0 should be selected")
    assert widget.current_tab.index == 0
    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Select the "more" option again. If the more option is stateful,
    # this will result is displaying the last "more" option selected
    try:
        probe.select_more()
        if probe.more_option_is_stateful:
            await probe.redraw("Previous more option should be displayed")
            assert widget.current_tab.index == 7
            # more is stateful, so there's a been a select event for the
            # previously selected "more" option.
            on_select_handler.assert_called_once_with(widget)
            on_select_handler.reset_mock()

            probe.reset_more()
            await probe.redraw("More option should be reset")
        else:
            await probe.redraw("More option should be displayed")

        assert widget.current_tab.index is None
    except AttributeError:
        pass

    on_select_handler.assert_not_called()

    # Select the second last tab in the GUI
    probe.select_tab(6)
    await probe.redraw("Tab 7 should be selected")

    assert widget.current_tab.index == 6
    assert extra_probes[3].width == pytest.approx(container_probe.width, abs=2)
    assert extra_probes[3].height > container_probe.height * 0.8

    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Select the first tab in the GUI
    probe.select_tab(0)
    await probe.redraw("Tab 0 should be selected")
    assert widget.current_tab.index == 0
    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Select the last tab programmatically while on a non-more option
    widget.current_tab = "Tab 8"
    await probe.redraw("Tab 8 should be selected")

    assert widget.current_tab.index == 7
    assert extra_probes[4].width == pytest.approx(container_probe.width, abs=2)
    assert extra_probes[4].height > container_probe.height * 0.8
    # on_select has been invoked. There may be a refresh event
    # associated with the display of the the stateful more option.
    on_select_handler.assert_called_with(widget)
    on_select_handler.reset_mock()


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
    await probe.redraw("Tab 2 should be disabled")

    assert widget.content[0].enabled
    assert not widget.content[1].enabled
    assert probe.tab_enabled(0)
    assert not probe.tab_enabled(1)

    # Try to select a disabled tab
    probe.select_tab(1)
    await probe.redraw("Try to select tab 2")

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
    await probe.redraw("Tab 2 should still be disabled")

    assert widget.content[0].enabled
    assert not widget.content[1].enabled

    # Select tab 3, which is index 2 in the widget's content; but on platforms
    # where disabling a tab means hiding the tab completely, it will be *visual*
    # index 1, but content index 2. Make sure the indices are all correct.
    widget.current_tab = 2
    await probe.redraw("Tab 3 should be selected")

    assert widget.current_tab.index == 2
    assert widget.current_tab.text == "Tab 3"

    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Enable item 1
    widget.content[1].enabled = True
    await probe.redraw("Tab 2 should be enabled")

    assert widget.content[0].enabled
    assert widget.content[1].enabled
    assert probe.tab_enabled(0)
    assert probe.tab_enabled(1)

    # Try to select tab 1
    probe.select_tab(1)
    await probe.redraw("Tab 1 should be selected")

    assert widget.current_tab.index == 1
    assert widget.content[0].enabled
    assert widget.content[1].enabled

    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Enable item 1 again, even though it's enabled
    widget.content[1].enabled = True
    await probe.redraw("Tab 2 should still be enabled")

    assert widget.content[0].enabled
    assert widget.content[1].enabled


async def test_change_content(
    widget,
    probe,
    container_probe,
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
    await probe.redraw("New tab has been added disabled")

    assert len(widget.content) == 4
    assert widget.content[1].text == "New tab"
    assert not widget.content[1].enabled

    # Enable the new content and select it
    widget.content[1].enabled = True
    widget.current_tab = "New tab"
    await probe.redraw("New tab has been enabled and selected")

    assert widget.current_tab.index == 1
    assert widget.current_tab.text == "New tab"
    # The content should be the same size as the container; this is simple to
    # test in width, but the height can be impacted by the size of the tabs
    # themselves. Test that the content has expanded; but for height, check that
    # the size is > 80% of the container (allowing up to 20% for tabs)
    assert new_probe.width == pytest.approx(container_probe.width, abs=2)
    assert new_probe.height > container_probe.height * 0.8

    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Change the title of Tab 2
    widget.content["Tab 2"].text = "New 2"
    await probe.redraw("Tab 2 has been renamed")

    assert widget.content[2].text == "New 2"

    # Remove Tab 2
    widget.content.remove("New 2")
    await probe.redraw("Tab 2 has been removed")
    assert len(widget.content) == 3

    # Add tab 2 back in at the end with a new title
    widget.content.append("New Tab 2", content2)
    await probe.redraw("Tab 2 has been added with a new title")

    widget.current_tab = "New Tab 2"
    await probe.redraw("Revised tab 2 has been selected")

    assert widget.current_tab.index == 3
    assert widget.current_tab.text == "New Tab 2"
    # The content should be the same size as the container; this is simple to
    # test in width, but the height can be impacted by the size of the tabs
    # themselves. Test that the content has expanded; but for height, check that
    # the size is > 80% of the container (allowing up to 20% for tabs)
    assert content2_probe.width == pytest.approx(container_probe.width, abs=2)
    assert content2_probe.height > container_probe.height * 0.8

    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()
