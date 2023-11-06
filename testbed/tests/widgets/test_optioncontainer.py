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
    skip_on_platforms("android", "iOS")
    return toga.OptionContainer(
        content=[("Tab 1", content1), ("Tab 2", content2), ("Tab 3", content3)],
        style=Pack(flex=1),
        on_select=on_select_handler,
    )


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
    await probe.redraw("Tab 1 should be selected")
    assert widget.current_tab.index == 0
    assert content1_probe.width > 600
    assert content1_probe.height > 380

    # on_select hasn't been invoked.
    on_select_handler.assert_not_called()

    # Select item 1 programmatically
    widget.current_tab = "Tab 2"
    await probe.redraw("Tab 2 should be selected")

    assert widget.current_tab.index == 1
    assert content2_probe.width > 600
    assert content2_probe.height > 380
    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()

    # Select item 2 in the GUI
    probe.select_tab(2)
    await probe.redraw("Tab 3 should be selected")

    assert widget.current_tab.index == 2
    assert content3_probe.width > 600
    assert content3_probe.height > 380
    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
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
    assert new_probe.width > 600
    assert new_probe.height > 380

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
    assert content2_probe.width > 600
    assert content2_probe.height > 380

    # on_select has been invoked
    on_select_handler.assert_called_once_with(widget)
    on_select_handler.reset_mock()
