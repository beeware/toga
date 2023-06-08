import pytest

import toga
from toga.style.pack import COLUMN, ROW

from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_enable_noop,
    test_focus_noop,
)


@pytest.fixture
async def widget():
    return toga.ImageView(image="resources/sample.png")


async def test_implicit_size(widget, probe, container_probe):
    """If the image view size is implicit, the image provides flexible size hints."""

    await probe.redraw("ImageView takes size hint from the image")
    assert probe.width == pytest.approx(144, abs=2)
    assert probe.height == pytest.approx(72, abs=2)
    assert probe.preserve_aspect_ratio

    # Clear the image; it's now an explicit sized empty image.
    widget.image = None

    await probe.redraw("Image has been cleared")
    assert probe.width == pytest.approx(0, abs=2)
    assert probe.height == pytest.approx(0, abs=2)
    assert not probe.preserve_aspect_ratio

    # Restore the image; Make the parent a flex row
    widget.image = "resources/sample.png"
    widget.style.flex = 1
    widget.parent.style.direction = ROW

    await probe.redraw("Image is in a row box")
    assert probe.width == pytest.approx(container_probe.width, abs=2)
    assert probe.height == pytest.approx(container_probe.height, abs=2)
    assert probe.preserve_aspect_ratio

    # Make the parent a flex column
    widget.parent.style.direction = COLUMN

    await probe.redraw("Image is in a column box")
    assert probe.width == pytest.approx(container_probe.width, abs=2)
    assert probe.height == pytest.approx(container_probe.height, abs=2)
    assert probe.preserve_aspect_ratio


async def test_explicit_width(widget, probe, container_probe):
    """If the image width is explicit, the image view will resize preserving aspect ratio."""
    # Explicitly set width
    widget.style.width = 200

    await probe.redraw("Image has explicit width")
    assert probe.width == pytest.approx(200, abs=2)
    assert probe.height == pytest.approx(100, abs=2)
    assert probe.preserve_aspect_ratio

    # Clear the image; it's now an explicit sized empty image.
    widget.image = None

    await probe.redraw("Image has been cleared")
    assert probe.width == pytest.approx(200, abs=2)
    assert probe.height == pytest.approx(0, abs=2)
    assert not probe.preserve_aspect_ratio

    # Restore the image; Make the parent a flex row
    widget.image = "resources/sample.png"
    widget.style.flex = 1
    widget.parent.style.direction = ROW

    await probe.redraw("Image is in a row box")
    assert probe.width == pytest.approx(200, abs=2)
    assert probe.height == pytest.approx(container_probe.height, abs=2)
    assert probe.preserve_aspect_ratio

    # Make the parent a flex column
    widget.parent.style.direction = COLUMN

    await probe.redraw("Image is in a column box")
    assert probe.width == pytest.approx(200, abs=2)
    assert probe.height == pytest.approx(container_probe.height, abs=2)
    assert probe.preserve_aspect_ratio


async def test_explicit_height(widget, probe, container_probe):
    """If the image height is explicit, the image view will resize preserving aspect ratio."""
    # Explicitly set height
    widget.style.height = 150

    await probe.redraw("Image has explicit height")
    assert probe.width == pytest.approx(300, abs=2)
    assert probe.height == pytest.approx(150, abs=2)
    assert probe.preserve_aspect_ratio

    # Clear the image; it's now an explicit sized empty image.
    widget.image = None

    await probe.redraw("Image has been cleared")
    assert probe.width == pytest.approx(0, abs=2)
    assert probe.height == pytest.approx(150, abs=2)
    assert not probe.preserve_aspect_ratio

    # Restore the image; Make the parent a flex row
    widget.image = "resources/sample.png"
    widget.style.flex = 1
    widget.parent.style.direction = ROW

    await probe.redraw("Image is in a row box")
    assert probe.width == pytest.approx(container_probe.width, abs=2)
    assert probe.height == pytest.approx(150, abs=2)
    assert probe.preserve_aspect_ratio

    # Make the parent a flex column
    widget.parent.style.direction = COLUMN

    await probe.redraw("Image is in a column box")
    assert probe.width == pytest.approx(container_probe.width, abs=2)
    assert probe.height == pytest.approx(150, abs=2)
    assert probe.preserve_aspect_ratio


async def test_explicit_size(widget, probe):
    """If the image size is explicit, the image view doesn't change size."""
    # Explicitly set both size axes
    widget.style.width = 200
    widget.style.height = 300

    await probe.redraw("Image has explicit sizing")
    assert probe.width == pytest.approx(200, abs=2)
    assert probe.height == pytest.approx(300, abs=2)
    assert not probe.preserve_aspect_ratio

    # Clear the image; it's now an explicit sized empty image.
    widget.image = None

    await probe.redraw("Image has been cleared")
    assert probe.width == pytest.approx(200, abs=2)
    assert probe.height == pytest.approx(300, abs=2)
    assert not probe.preserve_aspect_ratio

    # Restore the image; Make the parent a flex row
    widget.image = "resources/sample.png"
    widget.style.flex = 1
    widget.parent.style.direction = ROW

    await probe.redraw("Image is in a row box")
    assert probe.width == pytest.approx(200, abs=2)
    assert probe.height == pytest.approx(300, abs=2)
    assert not probe.preserve_aspect_ratio

    # Make the parent a flex column
    widget.parent.style.direction = COLUMN

    await probe.redraw("Image is in a column box")
    assert probe.width == pytest.approx(200, abs=2)
    assert probe.height == pytest.approx(300, abs=2)
    assert not probe.preserve_aspect_ratio
