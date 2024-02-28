import asyncio
import gc
import platform
from time import time
from unittest.mock import Mock

import pytest

import toga
from toga.style import Pack

from .properties import (  # noqa: F401
    test_flex_widget_size,
)

# MapVierw can't be given focus on mobile
if toga.platform.current_platform in {"android", "iOS"}:
    from .properties import test_focus_noop  # noqa: F401
else:
    from .properties import test_focus  # noqa: F401


# These timeouts are loose because CI can be very slow, especially on mobile.
WINDOWS_INIT_TIMEOUT = 60


@pytest.fixture
async def on_select():
    on_select = Mock()
    return on_select


@pytest.fixture
async def widget(on_select):
    if toga.platform.current_platform == "linux":
        # On Gtk, ensure that any WebViews from a previous test runs have been garbage
        # collected. This prevents a segfault at GC time likely coming from the test
        # suite running in a thread and Gtk WebViews sharing resources between
        # instances. We perform the GC run here since pytest fixtures make earlier
        # cleanup difficult.
        gc.collect()

    widget = toga.MapView(style=Pack(flex=1), on_select=on_select)

    # Some implementations of MapView are a WebView wearing a trenchcoat.
    # Ensure that the webview is fully configured before proceeding.
    if toga.platform.current_platform in {"linux", "windows"}:
        deadline = time() + WINDOWS_INIT_TIMEOUT
        while widget._impl.backlog is not None:
            if time() < deadline:
                await asyncio.sleep(0.05)
            else:
                raise RuntimeError("MapView web canvas didn't initialize")
    else:
        # All other implementations still need a second to load map tiles etc.
        await asyncio.sleep(1)

    yield widget

    if toga.platform.current_platform == "linux":
        # On Gtk, ensure that the MapView is garbage collection before the next test
        # case. This prevents a segfault at GC time likely coming from the test suite
        # running in a thread and Gtk WebViews sharing resources between instances.
        del widget
        gc.collect()


# The next two tests fail about 75% of the time in the macOS x86_64 CI configuration.
# The failure mode appears to be that the widget *exists*, but doesn't respond to
# changes in location or zoom. I've been unable to reproduce this in actual testing on
# an actual macOS x86_64 machine, and the test is 100% reliable on every other platform,
# including ARM64 macOS. Given that macOS x86_64 support is of waning significance, I've
# take the practical measure of converting these test failures to an xfail. They'll
# occasionally XPASS, but that won't fail the test; and we'll still get coverage
# because all the necessary APIs have been invoked prior to the failure.
@pytest.mark.xfail(
    condition=platform.system() == "Darwin" and platform.machine() == "x86_64",
    reason="Test is unreliable on macOS x86_64",
)
async def test_location(widget, probe):
    """The location of the map can be changed"""
    # Initial location is Perth
    widget.location = (-31.9559, 115.8606)
    await probe.wait_for_map("Map is centered on Perth", max_delay=2)
    assert isinstance(widget.location, toga.LatLng)
    assert widget.location == pytest.approx((-31.9559, 115.8606), abs=0.005)

    # Set location to Margaret River, just south of Perth
    widget.location = (-33.9550, 115.0750)
    await probe.wait_for_map("Location has panned to Margaret River", max_delay=2)
    assert isinstance(widget.location, toga.LatLng)
    assert widget.location == pytest.approx((-33.955, 115.075), abs=0.005)


# See test_location for an explanation of this xfail
@pytest.mark.xfail(
    condition=platform.system() == "Darwin" and platform.machine() == "x86_64",
    reason="Test is unreliable on macOS x86_64",
)
async def test_zoom(widget, probe):
    """The zoom factor of the map can be changed"""
    await probe.wait_for_map("Map is at initial location", max_delay=2)

    # We can't read the zoom of a map; but we can probe to get the delta from the
    # minimum to maximum latitude that is currently visible. That delta should be within
    # a broad range at each zoom level.
    for zoom, min_span, max_span in [
        (0, 45, 180),
        (3, 6, 45),
        (6, 0.7, 6),
        (9, 0.09, 0.7),
        (12, 0.01, 0.09),
        (15, 0.002, 0.01),
        (18, 0.0, 0.002),
    ]:
        widget.zoom = zoom
        await probe.wait_for_map(f"Map has been zoomed to level {zoom}", max_delay=2)

        # Work out the span associated with a 256px vertical space.
        scale_span = await probe.longitude_span() / (probe.height / 256)
        assert (
            min_span < scale_span < max_span
        ), f"Zoom level {zoom}: failed {min_span} < {scale_span} < {max_span}"

        # Zoom level 0 can result in a map that needs to wrap content. Some implementations
        # prevent zooming out that far, so the reported zoom level can be has high as 2.
        if zoom == 0:
            assert widget.zoom <= 2
        else:
            assert widget.zoom == zoom


async def test_add_pins(widget, probe, on_select):
    """Pins can be added and removed from the map."""

    fremantle = toga.MapPin((-32.05423, 115.74763), title="Fremantle")
    lesmurdie = toga.MapPin((-31.994, 116.05), title="lesmurdie")
    joondalup = toga.MapPin((-31.745, 115.766), title="Joondalup")
    stadium = toga.MapPin((-31.95985, 115.8795), title="WACA Ground", subtitle="Old")

    widget.pins.add(joondalup)
    await probe.wait_for_map("Joondalup pin has been added")
    assert probe.pin_count == 1

    widget.pins.add(lesmurdie)
    widget.pins.add(fremantle)
    widget.pins.add(stadium)
    await probe.wait_for_map("Other pins have been added")
    assert probe.pin_count == 4

    # Move the sports ground to a new location
    stadium.location = (-31.951111, 115.889167)
    stadium.title = "Perth Stadium"
    stadium.subtitle = "New"
    await probe.wait_for_map("Stadium has been moved and renamed")

    widget.pins.remove(stadium)
    await probe.wait_for_map("Stadium has been removed")
    assert probe.pin_count == 3

    widget.pins.clear()
    await probe.wait_for_map("All pins have been removed")
    assert probe.pin_count == 0


async def test_select_pin(widget, probe, on_select):
    """Pins can be selected."""

    fremantle = toga.MapPin((-32.05423, 115.74763), title="Fremantle")
    lesmurdie = toga.MapPin((-31.994, 116.05), title="lesmurdie")
    joondalup = toga.MapPin((-31.745, 115.766), title="Joondalup")

    widget.pins.add(joondalup)
    widget.pins.add(lesmurdie)
    widget.pins.add(fremantle)
    await probe.wait_for_map("Pins have been added")

    await probe.select_pin(lesmurdie)
    await probe.wait_for_map("Lesmurdie pin has been selected")
    on_select.assert_called_once_with(widget, pin=lesmurdie)
    on_select.reset_mock()

    await probe.select_pin(fremantle)
    await probe.wait_for_map("Fremantle pin has been selected")
    on_select.assert_called_once_with(widget, pin=fremantle)
    on_select.reset_mock()
