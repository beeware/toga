import math
from unittest.mock import Mock, call

import pytest
from PIL import Image

import toga
from toga.colors import (
    CORNFLOWERBLUE,
    GOLDENROD,
    REBECCAPURPLE,
    RED,
    TRANSPARENT,
    WHITE,
    rgba,
)
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
async def canvas(widget, probe, on_resize_handler):
    # Modify the base canvas fixture to make it more useful for drawing tests.
    widget.style.background_color = WHITE
    widget.style.width = 200
    widget.style.height = 200
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
        stroke.line_to(x=200, y=200)
        stroke.move_to(x=200, y=0)
        stroke.line_to(x=0, y=200)

        stroke.rect(2, 2, 198, 198)

    await probe.redraw("Test image has been drawn")

    image = canvas.as_image()
    imageview = toga.ImageView(image)
    canvas.window.content.add(imageview)

    await probe.redraw("Cloned image should be visible")

    # Cloned image is the right size. The platform may do DPI scaling;
    # let the probe determine the correct scaled size.
    probe.assert_image_size(image, 200, 200)


def assert_reference(probe, reference, threshold=0.0):
    """Assert that the canvas currently matches a reference image, within an RMS threshold"""
    # Get the canvas image.
    image = probe.get_image()
    scaled_image = image.resize((200, 200))

    # Look for a platform-specific reference variant.
    reference_variant = probe.reference_variant(reference)
    path = toga.App.app.paths.app / "resources" / "canvas" / f"{reference_variant}.png"
    save_path = toga.App.app.paths.data / "canvas" / f"{reference_variant}.png"

    # If a reference image exists, scale the image to the same size as the reference,
    # and do an MSE comparison on every pixel in 0-1 RGBA colorspace.
    if path.exists():
        reference_image = Image.open(path)

        total = 0.0
        for y in range(0, reference_image.size[1]):
            for x in range(0, reference_image.size[0]):
                actual = scaled_image.getpixel((x, y))
                expected = reference_image.getpixel((x, y))

                for act, exp in zip(actual, expected):
                    err = (act / 255) - (exp / 255)
                    total += err * err

        rmse = math.sqrt(total / (reference_image.size[0] * reference_image.size[1]))
        # If the delta exceeds threshold, save the test image and fail the test.
        if rmse > threshold:
            print(f"Saving {save_path}")
            save_path.parent.mkdir(parents=True, exist_ok=True)
            scaled_image.save(save_path)
            assert pytest.fail(f"Rendered image doesn't match reference (RMSE=={rmse})")
    else:
        print(f"Saving {save_path}")
        save_path.parent.mkdir(parents=True, exist_ok=True)
        scaled_image.save(save_path)
        assert pytest.fail(f"Couldn't find {reference_variant!r} reference image")


async def test_transparency(canvas, probe):
    "Transparency is preserved in captured images"
    canvas.style.background_color = TRANSPARENT

    # Draw a rectangle. move_to is implied
    canvas.context.begin_path()
    canvas.context.rect(x=20, y=20, width=120, height=120)
    canvas.context.fill(color=REBECCAPURPLE)

    canvas.context.begin_path()
    canvas.context.rect(x=60, y=60, width=120, height=120)
    canvas.context.fill(color=rgba(0x33, 0x66, 0x99, 0.5))

    await probe.redraw("Image with transparent content and background")
    # 0.1 is a big threshold; it's equivalent to 400 pixels being 100% the wrong color.
    # This occurs because pixel aliasing around the edge of the squares generates
    # different colors due to image scaling and alpha blending differences on each
    # platform. You could also generate 0.1 threshold error by moving the entire image 1
    # px to the left. However, it's difficult to find a measure that passes the edge
    # issue without also passing a translation error.
    assert_reference(probe, "transparency", threshold=0.1)


async def test_paths(canvas, probe):
    "A path can be drawn"

    canvas.context.begin_path()
    canvas.context.move_to(20, 20)
    canvas.context.line_to(140, 20)
    canvas.context.line_to(20, 140)
    canvas.context.fill()

    # Stroked triangle requires explicit close
    canvas.context.begin_path()
    canvas.context.move_to(180, 180)
    canvas.context.line_to(180, 60)
    canvas.context.line_to(60, 180)
    canvas.context.close_path()
    canvas.context.stroke()

    await probe.redraw("Pair of triangles should be drawn")
    assert_reference(probe, "paths", threshold=0.04)


async def test_bezier_curve(canvas, probe):
    "A Bézier curve can be drawn"

    canvas.context.begin_path()
    canvas.context.move_to(100, 44)
    canvas.context.bezier_curve_to(100, 40, 92, 20, 60, 20)
    canvas.context.bezier_curve_to(12, 20, 12, 80, 12, 80)
    canvas.context.bezier_curve_to(12, 108, 44, 144, 100, 172)
    canvas.context.bezier_curve_to(156, 144, 188, 108, 188, 80)
    canvas.context.bezier_curve_to(188, 80, 188, 20, 140, 20)
    canvas.context.bezier_curve_to(116, 20, 100, 40, 100, 44)
    canvas.context.stroke()

    await probe.redraw("Heart should be drawn")
    assert_reference(probe, "bezier_curve", threshold=0.05)


async def test_quadratic_curve(canvas, probe):
    "A quadratic curve can be drawn"

    canvas.context.begin_path()
    canvas.context.move_to(100, 20)
    canvas.context.quadratic_curve_to(20, 20, 20, 80)
    canvas.context.quadratic_curve_to(20, 140, 60, 140)
    canvas.context.quadratic_curve_to(60, 172, 28, 180)
    canvas.context.quadratic_curve_to(76, 172, 110, 140)
    canvas.context.quadratic_curve_to(180, 140, 180, 80)
    canvas.context.quadratic_curve_to(180, 20, 100, 20)
    canvas.context.stroke()

    await probe.redraw("Quote bubble should be drawn")
    assert_reference(probe, "quadratic_curve", threshold=0.05)


async def test_arc(canvas, probe):
    "An arc can be drawn"
    canvas.context.begin_path()
    # Face
    canvas.context.arc(100, 100, 80, 0)

    # Smile
    canvas.context.move_to(150, 100)
    canvas.context.arc(100, 100, 50, 0, math.pi, False)

    # Hair
    canvas.context.move_to(190, 100)
    canvas.context.arc(100, 100, 90, 0, math.pi, True)

    # Left eye
    canvas.context.move_to(70, 70)
    canvas.context.arc(64, 70, 6, 0)

    # Right eye
    canvas.context.move_to(130, 70)
    canvas.context.arc(124, 70, 6, 0)
    canvas.context.stroke()

    await probe.redraw("Smiley face should be drawn")
    assert_reference(probe, "arc", threshold=0.06)


async def test_ellipse(canvas, probe):
    "An ellipse can be drawn"

    # Nucleus (filled circle)
    canvas.context.move_to(90, 100)
    canvas.context.ellipse(100, 100, 20, 20)
    canvas.context.fill(color=RED)

    # Purple orbit
    canvas.context.ellipse(100, 100, 90, 20, rotation=math.pi * 3 / 4)
    canvas.context.stroke(color=REBECCAPURPLE)

    # Blue orbit
    canvas.context.ellipse(
        100,
        100,
        radiusx=20,
        radiusy=90,
        rotation=-math.pi / 4,
        startangle=math.pi * 7 / 4,
        endangle=math.pi / 4,
        anticlockwise=True,
    )
    canvas.context.stroke(color=CORNFLOWERBLUE)

    # Yellow orbit
    canvas.context.ellipse(
        100,
        100,
        radiusx=20,
        radiusy=90,
        startangle=math.pi / 4,
        endangle=math.pi * 7 / 4,
    )
    canvas.context.stroke(color=GOLDENROD)

    await probe.redraw("Atom should be drawn")
    assert_reference(probe, "ellipse", threshold=0.04)


async def test_rect(canvas, probe):
    "A rectangle can be drawn"

    # Draw a rectangle. move_to is implied
    canvas.context.begin_path()
    canvas.context.rect(x=20, y=60, width=160, height=100)
    canvas.context.fill(color=REBECCAPURPLE)

    await probe.redraw("Filled rectangle should be drawn")
    assert_reference(probe, "rect", threshold=0.02)


async def test_fill(canvas, probe):
    "A fill can be drawn with primitives"
    # Draw a closed path
    canvas.context.begin_path()
    canvas.context.move_to(x=60, y=10)
    canvas.context.line_to(x=30, y=110)
    canvas.context.line_to(x=110, y=50)
    canvas.context.line_to(x=10, y=50)
    canvas.context.line_to(x=90, y=110)
    canvas.context.fill(color=REBECCAPURPLE)

    # Same path (slightly offset), but with EVENODD winding.
    canvas.context.begin_path()
    canvas.context.move_to(x=140, y=90)
    canvas.context.line_to(x=110, y=190)
    canvas.context.line_to(x=190, y=130)
    canvas.context.line_to(x=90, y=130)
    canvas.context.line_to(x=170, y=190)
    canvas.context.fill(color=CORNFLOWERBLUE, fill_rule=FillRule.EVENODD)

    await probe.redraw("Stars should be drawn")
    assert_reference(probe, "fill", threshold=0.02)


async def test_stroke(canvas, probe):
    "A stroke can be drawn with primitives"
    # Draw a closed path
    canvas.context.begin_path()
    canvas.context.move_to(x=20, y=20)
    canvas.context.line_to(x=100, y=20)
    canvas.context.line_to(x=180, y=180)
    canvas.context.line_to(x=100, y=180)
    canvas.context.close_path()
    canvas.context.stroke(color=REBECCAPURPLE)

    # Draw an open path inside it
    canvas.context.begin_path()
    canvas.context.move_to(x=50, y=40)
    canvas.context.line_to(x=90, y=40)
    canvas.context.line_to(x=150, y=160)
    canvas.context.line_to(x=110, y=160)
    canvas.context.stroke(color=CORNFLOWERBLUE)

    await probe.redraw("Stroke should be drawn")
    assert_reference(probe, "stroke", threshold=0.02)


async def test_closed_path_context(canvas, probe):
    "A closed path can be built with a context"

    # Build a parallelogram path
    with canvas.context.ClosedPath(x=20, y=20) as path:
        path.line_to(x=100, y=20)
        path.line_to(x=180, y=180)
        path.line_to(x=100, y=180)

    # Draw it with a thick dashed line
    canvas.context.stroke(color=REBECCAPURPLE, line_width=5, line_dash=[20, 30])

    await probe.redraw("Closed path should be drawn with context")
    assert_reference(probe, "closed_path_context", threshold=0.02)


async def test_fill_context(canvas, probe):
    "A fill path can be built with a context"

    # Build a filled parallelogram
    with canvas.context.Fill(x=20, y=20, color=REBECCAPURPLE) as path:
        path.line_to(x=100, y=20)
        path.line_to(x=180, y=180)
        path.line_to(x=100, y=180)

    await probe.redraw("Fill should be drawn with context")
    assert_reference(probe, "fill_context", threshold=0.01)


async def test_stroke_context(canvas, probe):
    "A stroke can be drawn with a context"
    # Draw a thin line
    with canvas.context.Stroke(x=40, y=20, color=REBECCAPURPLE) as stroke:
        stroke.line_to(x=80, y=180)

    # Draw a thick dashed line
    with canvas.context.Stroke(
        x=80, y=20, line_width=20, line_dash=[20, 10], color=CORNFLOWERBLUE
    ) as stroke:
        stroke.line_to(x=120, y=180)

    await probe.redraw("Stroke should be drawn with context")
    assert_reference(probe, "stroke_context", threshold=0.02)


async def test_transforms(canvas, probe):
    "Transforms can be applied"

    # Draw a rectangle after a horizontal translation
    canvas.context.translate(160, 20)
    canvas.context.rect(0, 0, 20, 60)
    canvas.context.fill(color=CORNFLOWERBLUE)

    canvas.context.reset_transform()
    canvas.context.rotate(math.pi / 4)
    canvas.context.rect(200, 0, 20, 60)
    canvas.context.fill(color=REBECCAPURPLE)

    canvas.context.reset_transform()
    canvas.context.scale(2, 5)
    canvas.context.rect(10, 10, 10, 10)
    canvas.context.fill(color=GOLDENROD)

    canvas.context.reset_transform()
    canvas.context.translate(100, 60)
    canvas.context.rotate(math.pi / 7 * 4)
    canvas.context.scale(5, 2)
    canvas.context.rect(2, 2, 10, 10)
    canvas.context.fill()

    await probe.redraw("Transforms can be applied")
    assert_reference(probe, "transforms", threshold=0.02)


async def test_write_text(canvas, probe):
    "Text can be measured and written"
    hello_text = "Hello"
    hello_size = canvas.measure_text(hello_text)

    with canvas.Fill(color=REBECCAPURPLE) as text_filler:
        text_filler.write_text(
            hello_text,
            100 - (hello_size[0] // 2),
            10 + hello_size[1],
        )
    # Draw a border around the text to verify text sizing
    with canvas.Stroke(color=CORNFLOWERBLUE) as stroke:
        stroke.rect(
            100 - (hello_size[0] // 2) - 4,
            10 + 4,
            hello_size[0] + 8,
            hello_size[1] + 8,
        )

    world_text = "World!"
    world_font = Font(SANS_SERIF, size=24)
    world_size = canvas.measure_text(world_text, font=world_font)

    with canvas.Stroke() as text_filler:
        text_filler.write_text(
            world_text,
            100 - (world_size[0] // 2),
            80,
            font=world_font,
        )

    # Draw a border around the text to verify text sizing
    with canvas.Stroke(color=CORNFLOWERBLUE) as stroke:
        stroke.rect(
            100 - (world_size[0] // 2) - 4,
            80 - world_size[1] + 4,
            world_size[0] + 8,
            world_size[1] + 8,
        )

    toga_text = "Toga"
    toga_font = Font(SERIF, 72)
    toga_size = canvas.measure_text(toga_text, font=toga_font)

    with canvas.Stroke(color=REBECCAPURPLE) as stroke:
        with stroke.Fill(color=CORNFLOWERBLUE) as text_filler:
            text_filler.write_text(
                toga_text,
                100 - (toga_size[0] // 2),
                130 + (toga_size[1] // 2),
                font=toga_font,
            )

    # Draw a border around the text to verify text sizing
    with canvas.Stroke(color=CORNFLOWERBLUE) as stroke:
        stroke.rect(
            100 - (toga_size[0] // 2) - 4,
            130 - (toga_size[1] // 2) + 4,
            toga_size[0] + 8,
            toga_size[1] + 8,
        )

    await probe.redraw("Text should be drawn")
    # 0.07 is quite a high error threshold; it's equivalent to 196 pixels being
    # 100% the wrong color. However, fonts are the worst case for evaluating with
    # RMSE, as they are 100% edges; and due to minor font rendering discrepancies
    # and antialiasing introduced by image scaling, edges are the source of error.
    assert_reference(probe, "write_text", threshold=0.07)


async def test_multiline_text(canvas, probe):
    "Multiline text can be measured and written"
    # Write a single line
    with canvas.context.Fill() as text_filler:
        text_filler.write_text("Single line", 20, 40)

    # Write multiple lines
    with canvas.context.Fill() as text_filler:
        text_filler.write_text("Line 1\nLine 2\nLine 3", 20, 160)

    # Write empty text
    with canvas.context.Fill() as text_filler:
        text_filler.write_text("", 100, 20)

    await probe.redraw("Multiple text blocks should be drawn")
    # 0.09 is quite a high error threshold; it's equivalent to 324 pixels being
    # 100% the wrong color. However, fonts are the worst case for evaluating with
    # RMSE, as they are 100% edges; and due to minor font rendering discrepancies
    # and antialiasing introduced by image scaling, edges are the source of error.
    assert_reference(probe, "multiline_text", threshold=0.09)
