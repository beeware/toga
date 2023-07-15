import math
from unittest.mock import Mock, call

import pytest
from PIL import Image

import toga
from toga.colors import CORNFLOWERBLUE, GOLDENROD, REBECCAPURPLE, RED, WHITE
from toga.constants import FillRule
from toga.fonts import SANS_SERIF, SERIF, Font
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
async def canvas(widget, on_resize_handler):
    # Modify the base canvas fixture to make it more useful for drawing tests.
    widget.style.background_color = WHITE
    widget.style.width = 100
    widget.style.height = 100
    return widget


def assert_pixel(image, x, y, color):
    assert image.getpixel((x, y)) == color


async def test_resize(widget, probe, on_resize_handler):
    "Resizing the widget causes on-resize events"
    # Make the canvas visible against window background.
    widget.style.background_color = CORNFLOWERBLUE

    # Just manifesting the widget causes at least one resize event;
    # the most recent of which has a large
    await probe.redraw("Canvas should be full size of window")
    assert on_resize_handler.call_count >= 1
    assert on_resize_handler.call_args.kwargs["width"] > 300
    assert on_resize_handler.call_args.kwargs["height"] > 300
    on_resize_handler.reset()

    widget.style.width = 100
    await probe.redraw("Canvas should be tall and narrow")
    assert on_resize_handler.call_count >= 1
    assert on_resize_handler.call_args.kwargs["width"] == 100
    assert on_resize_handler.call_args.kwargs["height"] > 300
    on_resize_handler.reset()

    widget.style.height = 100
    await probe.redraw("Canvas should be small")
    assert on_resize_handler.call_count >= 1
    assert on_resize_handler.call_args.kwargs["width"] == 100
    assert on_resize_handler.call_args.kwargs["height"] == 100
    on_resize_handler.reset()

    del widget.style.width
    await probe.redraw("Canvas should be width of the screen")
    assert on_resize_handler.call_count >= 1
    assert on_resize_handler.call_args.kwargs["width"] > 300
    assert on_resize_handler.call_args.kwargs["height"] == 100
    on_resize_handler.reset()


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


def assert_reference(probe, reference, threshold=25.0):
    """Assert that the canvas currently matches a reference image, within an RMS threshold"""

    # Get the canvas image.
    image = probe.get_image()
    scaled_image = image.resize((100, 100))

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

        delta = 0.0
        for y in range(0, reference_image.size[1]):
            for x in range(0, reference_image.size[0]):
                actual = scaled_image.getpixel((x, y))
                expected = reference_image.getpixel((x, y))

                diff = 0.0
                for a, e in zip(actual, expected):
                    diff += ((a / 255) - (e / 255)) * ((a / 255) - (e / 255))
                delta += math.sqrt(diff)

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
    else:
        scaled_image.save(
            toga.App.app.paths.app
            / "resources"
            / "canvas"
            / f"test-{reference}-{toga.platform.current_platform}.png"
        )
        assert pytest.fail(f"Couldn't find {reference!r} reference image")


async def test_paths(canvas, probe):
    "A path can be drawn"

    canvas.context.begin_path()
    canvas.context.move_to(10, 10)
    canvas.context.line_to(70, 10)
    canvas.context.line_to(10, 70)
    canvas.context.fill()

    # Stroked triangle requires explicit close
    canvas.context.begin_path()
    canvas.context.move_to(90, 90)
    canvas.context.line_to(90, 30)
    canvas.context.line_to(30, 90)
    canvas.context.close_path()
    canvas.context.stroke()

    await probe.redraw("Pair of triangles should be drawn")
    assert_reference(probe, "paths", threshold=25)


async def test_bezier_curve(canvas, probe):
    "A Bézier curve can be drawn"

    canvas.context.begin_path()
    canvas.context.move_to(50, 22)
    canvas.context.bezier_curve_to(50, 20, 46, 10, 30, 10)
    canvas.context.bezier_curve_to(6, 10, 6, 40, 6, 40)
    canvas.context.bezier_curve_to(6, 54, 22, 72, 50, 86)
    canvas.context.bezier_curve_to(78, 72, 94, 54, 94, 40)
    canvas.context.bezier_curve_to(94, 40, 94, 10, 70, 10)
    canvas.context.bezier_curve_to(58, 10, 50, 20, 50, 22)
    canvas.context.stroke()

    await probe.redraw("Heart should be drawn")
    assert_reference(probe, "bezier_curve", threshold=25)


async def test_quadratic_curve(canvas, probe):
    "A quadratic curve can be drawn"

    canvas.context.begin_path()
    canvas.context.move_to(50, 10)
    canvas.context.quadratic_curve_to(10, 10, 10, 40)
    canvas.context.quadratic_curve_to(10, 70, 30, 70)
    canvas.context.quadratic_curve_to(30, 86, 14, 90)
    canvas.context.quadratic_curve_to(38, 86, 55, 70)
    canvas.context.quadratic_curve_to(90, 70, 90, 40)
    canvas.context.quadratic_curve_to(90, 10, 50, 10)
    canvas.context.stroke()

    await probe.redraw("Quote bubble should be drawn")
    assert_reference(probe, "quadratic_curve", threshold=25)


async def test_arc(canvas, probe):
    "An arc can be drawn"
    canvas.context.begin_path()
    # Face
    canvas.context.arc(50, 50, 40, 0)

    # Smile
    canvas.context.move_to(75, 50)
    canvas.context.arc(50, 50, 25, 0, math.pi, False)

    # Hair
    canvas.context.move_to(95, 50)
    canvas.context.arc(50, 50, 45, 0, math.pi, True)

    # Left eye
    canvas.context.move_to(35, 35)
    canvas.context.arc(32, 35, 3, 0)

    # Right eye
    canvas.context.move_to(65, 35)
    canvas.context.arc(62, 35, 3, 0)
    canvas.context.stroke()

    await probe.redraw("Smiley face should be drawn")
    assert_reference(probe, "arc", threshold=25)


async def test_ellipse(canvas, probe):
    "An ellipse can be drawn"

    # Nucleus (filled circle)
    canvas.context.move_to(45, 50)
    canvas.context.ellipse(50, 50, 10, 10)
    canvas.context.fill(color=RED)

    # Purple orbit
    canvas.context.ellipse(50, 50, 45, 10, rotation=math.pi * 3 / 4)
    canvas.context.stroke(color=REBECCAPURPLE)

    # Blue orbit
    canvas.context.ellipse(
        50,
        50,
        radiusx=10,
        radiusy=45,
        rotation=-math.pi / 4,
        startangle=math.pi * 7 / 4,
        endangle=math.pi / 4,
        anticlockwise=True,
    )
    canvas.context.stroke(color=CORNFLOWERBLUE)

    # Yellow orbit
    canvas.context.ellipse(
        50,
        50,
        radiusx=10,
        radiusy=45,
        startangle=math.pi / 4,
        endangle=math.pi * 7 / 4,
    )
    canvas.context.stroke(color=GOLDENROD)

    await probe.redraw("Atom should be drawn")
    assert_reference(probe, "ellipse", threshold=25)


async def test_rect(canvas, probe):
    "A rectangle can be drawn"

    # Draw a rectangle. move_to is implied
    canvas.context.begin_path()
    canvas.context.rect(x=10, y=30, width=80, height=50)
    canvas.context.fill(color=REBECCAPURPLE)

    await probe.redraw("Filled rectangle should be drawn")
    assert_reference(probe, "rect", threshold=25)


async def test_fill(canvas, probe):
    "A fill can be drawn with primitives"
    # Draw a closed path
    canvas.context.begin_path()
    canvas.context.move_to(x=30, y=5)
    canvas.context.line_to(x=15, y=55)
    canvas.context.line_to(x=55, y=25)
    canvas.context.line_to(x=5, y=25)
    canvas.context.line_to(x=45, y=55)
    canvas.context.fill(color=REBECCAPURPLE)

    canvas.context.begin_path()
    canvas.context.move_to(x=70, y=45)
    canvas.context.line_to(x=55, y=95)
    canvas.context.line_to(x=95, y=65)
    canvas.context.line_to(x=45, y=65)
    canvas.context.line_to(x=85, y=95)
    canvas.context.fill(color=CORNFLOWERBLUE, fill_rule=FillRule.EVENODD)

    await probe.redraw("Stars should be drawn")
    assert_reference(probe, "fill", threshold=25)


async def test_stroke(canvas, probe):
    "A stroke can be drawn with primitives"
    # Draw a closed path
    canvas.context.move_to(x=20, y=20)
    canvas.context.begin_path()
    canvas.context.line_to(x=50, y=20)
    canvas.context.line_to(x=80, y=80)
    canvas.context.line_to(x=50, y=80)
    canvas.context.close_path()
    canvas.context.stroke(color=REBECCAPURPLE)

    # Draw an open path inside it
    canvas.context.move_to(x=40, y=40)
    canvas.context.begin_path()
    canvas.context.line_to(x=60, y=40)
    canvas.context.line_to(x=60, y=60)
    canvas.context.line_to(x=40, y=60)
    canvas.context.close_path()
    canvas.context.stroke(color=REBECCAPURPLE)

    await probe.redraw("Stroke should be drawn")
    assert_reference(probe, "stroke", threshold=25)


async def test_closed_path_context(canvas, probe):
    "A closed path can be built with a context"

    # Build a parallelogram path
    with canvas.context.ClosedPath(x=10, y=10) as path:
        path.line_to(x=50, y=10)
        path.line_to(x=90, y=90)
        path.line_to(x=50, y=90)

    # Draw it with a thick dashed line
    canvas.context.stroke(color=REBECCAPURPLE, line_width=5, line_dash=[10, 15])

    await probe.redraw("Closed path should be drawn with context")
    assert_reference(probe, "closed_path_context", threshold=25)


async def test_fill_context(canvas, probe):
    "A fill path can be built with a context"

    # Build a filled parallelogram
    with canvas.context.Fill(x=10, y=10, color=REBECCAPURPLE) as path:
        path.line_to(x=50, y=10)
        path.line_to(x=90, y=90)
        path.line_to(x=50, y=90)

    await probe.redraw("Fill should be drawn with context")
    assert_reference(probe, "fill_context", threshold=25)


async def test_stroke_context(canvas, probe):
    "A stroke can be drawn with a context"
    # Draw a thin line
    with canvas.context.Stroke(x=20, y=10, color=REBECCAPURPLE) as stroke:
        stroke.line_to(x=40, y=90)

    # Draw a thick dashed line
    with canvas.context.Stroke(
        x=40, y=10, line_width=10, line_dash=[10, 5], color=CORNFLOWERBLUE
    ) as stroke:
        stroke.line_to(x=60, y=90)

    await probe.redraw("Stroke should be drawn with context")
    assert_reference(probe, "stroke_context", threshold=25)


async def test_transforms(canvas, probe):
    "Transforms can be applied"

    # Draw a rectangle after a horizontal translation
    canvas.context.translate(80, 10)
    canvas.context.rect(0, 0, 10, 30)
    canvas.context.fill(color=CORNFLOWERBLUE)

    canvas.context.reset_transform()
    canvas.context.rotate(math.pi / 4)
    canvas.context.rect(100, 0, 10, 30)
    canvas.context.fill(color=REBECCAPURPLE)

    canvas.context.reset_transform()
    canvas.context.scale(2, 5)
    canvas.context.rect(5, 5, 5, 5)
    canvas.context.fill(color=GOLDENROD)

    canvas.context.reset_transform()
    canvas.context.translate(50, 30)
    canvas.context.rotate(math.pi / 7 * 4)
    canvas.context.scale(5, 2)
    canvas.context.rect(1, 1, 5, 5)
    canvas.context.fill()

    await probe.redraw("Transforms can be applied")
    assert_reference(probe, "transforms", threshold=25)


async def test_write_text(canvas, probe):
    "Text can be measured and written"
    hello_text = "Hello"
    hello_size = canvas.measure_text(hello_text)

    with canvas.Fill(color=REBECCAPURPLE) as text_filler:
        text_filler.write_text(
            hello_text,
            50 - (hello_size[0] // 2),
            5 + hello_size[1],
        )
    # Draw a border around the text to verify text sizing
    with canvas.Stroke(color=CORNFLOWERBLUE) as stroke:
        stroke.rect(
            50 - (hello_size[0] // 2) - 2,
            5 + 2,
            hello_size[0] + 4,
            hello_size[1] + 4,
        )

    world_text = "World!"
    world_font = Font(SANS_SERIF, size=12)
    world_size = canvas.measure_text(world_text, font=world_font)

    with canvas.Stroke() as text_filler:
        text_filler.write_text(
            world_text,
            50 - (world_size[0] // 2),
            40,
            font=world_font,
        )

    # Draw a border around the text to verify text sizing
    with canvas.Stroke(color=CORNFLOWERBLUE) as stroke:
        stroke.rect(
            50 - (world_size[0] // 2) - 2,
            40 - world_size[1] + 2,
            world_size[0] + 4,
            world_size[1] + 4,
        )

    toga_text = "Toga"
    toga_font = Font(SERIF, 36)
    toga_size = canvas.measure_text(toga_text, font=toga_font)

    with canvas.Stroke(color=REBECCAPURPLE) as stroke:
        with stroke.Fill(color=CORNFLOWERBLUE) as text_filler:
            text_filler.write_text(
                toga_text,
                50 - (toga_size[0] // 2),
                65 + (toga_size[1] // 2),
                font=toga_font,
            )

    # Draw a border around the text to verify text sizing
    with canvas.Stroke(color=CORNFLOWERBLUE) as stroke:
        stroke.rect(
            50 - (toga_size[0] // 2) - 2,
            65 - (toga_size[1] // 2) + 2,
            toga_size[0] + 4,
            toga_size[1] + 4,
        )

    await probe.redraw("Text should be drawn")
    assert_reference(probe, "write_text", threshold=0)


# ellipse with radiusy > radiusx
# EvenOdd Fille
