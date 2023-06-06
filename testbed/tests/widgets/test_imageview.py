import pytest

import toga

from .properties import (  # noqa: F401
    test_enable_noop,
    test_focus_noop,
)


@pytest.fixture
async def widget():
    return toga.ImageView(image="resources/sample.png")


async def test_image_sizing(widget, probe):
    """The ImageView responds correctly to size changes."""

    # Initial image size is implicit
    assert probe.width == 144
    assert probe.height == 72
    assert probe.preserve_aspect_ratio

    # Explicitly set both size axes
    widget.style.width = 200
    widget.style.height = 300

    await probe.redraw("Image has explicit sizing; aspect ratio is ignored")
    assert probe.width == 200
    assert probe.height == 300
    assert not probe.preserve_aspect_ratio

    widget.image = None

    await probe.redraw("Image has been cleared; but has explicit size")
    assert probe.width == 200
    assert probe.height == 300
    assert not probe.preserve_aspect_ratio

    del widget.style.width
    del widget.style.height

    await probe.redraw("Image has been cleared; explicit size removed")
    assert probe.width == 0
    assert probe.height == 0
    assert not probe.preserve_aspect_ratio
