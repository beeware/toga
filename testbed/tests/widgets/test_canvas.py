import math
import sys
from unittest.mock import Mock, call

import pytest
from PIL import Image

import toga
from toga.colors import CORNFLOWERBLUE, REBECCAPURPLE, RED, WHITE
from toga.style.pack import Pack

from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_enable_noop,
    test_flex_widget_size,
    test_focus_noop,
)


@pytest.fixture
def on_resize_handler():
    return Mock()


@pytest.fixture
def on_press_handler():
    return Mock()


@pytest.fixture
def on_drag_handler():
    return Mock()


@pytest.fixture
def on_release_handler():
    return Mock()


@pytest.fixture
def on_activate_handler():
    return Mock()


@pytest.fixture
def on_alt_press_handler():
    return Mock()


@pytest.fixture
def on_alt_drag_handler():
    return Mock()


@pytest.fixture
def on_alt_release_handler():
    return Mock()


@pytest.fixture
async def widget(
    on_resize_handler,
    on_press_handler,
    on_activate_handler,
    on_release_handler,
    on_drag_handler,
    on_alt_press_handler,
    on_alt_release_handler,
    on_alt_drag_handler,
):
    return toga.Canvas(
        on_resize=on_resize_handler,
        on_press=on_press_handler,
        on_activate=on_activate_handler,
        on_release=on_release_handler,
        on_drag=on_drag_handler,
        on_alt_press=on_alt_press_handler,
        on_alt_release=on_alt_release_handler,
        on_alt_drag=on_alt_drag_handler,
        style=Pack(flex=1),
    )


@pytest.fixture
async def canvas(widget):
    # Modify the base canvas fixture to make it more useful for drawing tests.
    widget.style.background_color = WHITE
    widget.style.width = 100
    widget.style.height = 100
    return widget


def assert_pixel(image, x, y, color):
    assert image.getpixel((x, y)) == color


async def test_press(canvas, probe, on_press_handler, on_release_handler):
    "Press/release events trigger handlers"
    await probe.mouse_press(20, 30)
    await probe.redraw("Press has been handled")

    on_press_handler.assert_called_once_with(canvas, 20, 30)
    on_release_handler.assert_called_once_with(canvas, 20, 30)


async def test_activate(
    canvas,
    probe,
    on_press_handler,
    on_release_handler,
    on_activate_handler,
):
    "Activation events trigger handlers"
    await probe.mouse_activate(20, 30)
    await probe.redraw("Activate has been handled")

    on_press_handler.assert_called_once_with(canvas, 20, 30)
    on_release_handler.mock_calls = [call(canvas, 20, 30), call(canvas, 20, 30)]
    on_activate_handler.assert_called_once_with(canvas, 20, 30)


async def test_drag(
    canvas,
    probe,
    on_press_handler,
    on_drag_handler,
    on_release_handler,
):
    "A drag event triggers a handler"
    await probe.mouse_drag(20, 40, 70, 90)
    await probe.redraw("Drag has been handled")

    on_press_handler.assert_called_once_with(canvas, 20, 40)
    on_drag_handler.assert_called_once_with(canvas, 45, 65)
    on_release_handler.assert_called_once_with(canvas, 70, 90)


async def test_alt_press(canvas, probe, on_alt_press_handler, on_alt_release_handler):
    "An alternate press event triggers a handler"
    await probe.alt_mouse_press(20, 40)
    await probe.redraw("Alt press has been handled")

    on_alt_press_handler.assert_called_once_with(canvas, 20, 40)
    on_alt_release_handler.assert_called_once_with(canvas, 20, 40)


async def test_alt_drag(
    canvas,
    probe,
    on_alt_press_handler,
    on_alt_drag_handler,
    on_alt_release_handler,
):
    "A drag event triggers a handler"
    await probe.alt_mouse_drag(20, 40, 70, 90)
    await probe.redraw("Alternate drag has been handled")

    on_alt_press_handler.assert_called_once_with(canvas, 20, 40)
    on_alt_drag_handler.assert_called_once_with(canvas, 45, 65)
    on_alt_release_handler.assert_called_once_with(canvas, 70, 90)


async def test_image_data(canvas, probe):
    "The canvas can be saved as an image"
    with canvas.Stroke(x=0, y=0, color=RED) as stroke:
        stroke.line_to(x=100, y=100)
        stroke.move_to(x=100, y=0)
        stroke.line_to(x=0, y=100)

        stroke.rect(1, 1, 98, 98)

    await probe.redraw("Test image has been drawn")

    image = canvas.as_image()
    imageview = toga.ImageView(image)
    canvas.window.content.add(imageview)

    await probe.redraw("Cloned image should be visible")

    # Cloned image is the right size. The platform may do DPI scaling;
    # let the probe determine the correct scaled size.
    probe.assert_image_size(image, 100, 100)


def assert_reference(image, reference, threshold=25.0):
    # Look for a platform-specific reference image; if one doesn't exist,
    # use a cross-platform reference image.
    path = (
        toga.App.app.paths.app
        / "resources"
        / "canvas"
        / f"{reference}-{toga.platform.current_platform}.png"
    )
    if not path.exists():
        path = toga.App.app.paths.app / "resources" / "canvas" / f"{reference}.png"

    # If a reference image exists, scale the image to the same size as the reference,
    # and do an RMS comparison on every pixel in 0-1 RGBA colorspace.
    if path.exists():
        reference_image = Image.open(path)
        scaled_image = image.resize(reference_image.size)

        delta = 0.0
        for y in range(0, reference_image.size[1]):
            for x in range(0, reference_image.size[0]):
                actual = scaled_image.getpixel((x, y))
                expected = reference_image.getpixel((x, y))

                diff = 0.0
                for a, e in zip(actual, expected):
                    diff += ((a / 255) - (e / 255)) * ((a / 255) - (e / 255))
                delta += math.sqrt(diff)
    else:
        # Fail the test
        delta = sys.maxint

    # If the delta exceeds threshold, save the test image and fail the test.
    if delta > threshold:
        scaled_image.save(
            toga.App.app.paths.app
            / "resources"
            / "canvas"
            / f"test-{reference}-{toga.platform.current_platform}.png"
        )
        assert pytest.fail(
            f"Rendered image doesn't match reference (RMS delta=={delta})"
        )


async def test_line(canvas, probe):
    "A line can be drawn"
    # Draw a thin line
    with canvas.Stroke(x=20, y=10, color=REBECCAPURPLE) as stroke:
        stroke.line_to(x=40, y=90)

    # Draw a thick dashed line
    with canvas.Stroke(
        x=40, y=10, line_width=10, line_dash=[10, 5], color=CORNFLOWERBLUE
    ) as stroke:
        stroke.line_to(x=60, y=90)

    await probe.redraw("Line should be drawn")
    assert_reference(probe.get_image(), "line", threshold=25)


# async def test_path(canvas, probe):
# async def test_bezier_curve(canvas, probe):
# async def test_quadratic_curve(canvas, probe):
# async def test_arc(canvas, probe):
# async def test_ellipse(canvas, probe):
# async def test_rect(canvas, probe):

# async def test_closed_path_context(canvas, probe):
# async def test_fill_context(canvas, probe):

# async def test_translate(canvas, probe):
# async def test_rotate(canvas, probe):
# async def test_scale(canvas, probe):
# async def test_compound_transform():
#     # test reset plus context push

# async def test_write_text(canvas, probe):
#     # include measure
