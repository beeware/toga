import math
import os
from itertools import chain
from math import pi, radians
from unittest.mock import call

import pytest
from PIL import Image, ImageChops

import toga
from toga import Font
from toga.colors import (
    BLACK,
    CORNFLOWERBLUE,
    GOLDENROD,
    REBECCAPURPLE,
    RED,
    TRANSPARENT,
    rgb,
)
from toga.constants import Baseline, FillRule
from toga.fonts import BOLD
from toga.images import Image as TogaImage
from toga.style.pack import SYSTEM

from ..conftest import build_cleanup_test
from ..properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_enable_noop,
    test_flex_widget_size,
    test_focus_noop,
)

test_cleanup = build_cleanup_test(toga.Canvas)


async def test_resize(widget, probe, on_resize_handler):
    "Resizing the widget causes on-resize events"
    # Make the canvas visible against window background.
    widget.style.background_color = CORNFLOWERBLUE

    # Just manifesting the widget causes at least one resize event;
    # the most recent of which has a large
    await probe.redraw("Canvas should be full size of window")
    assert on_resize_handler.call_count >= 1
    assert on_resize_handler.call_args.args == (widget,)
    assert on_resize_handler.call_args.kwargs["width"] > 300
    assert on_resize_handler.call_args.kwargs["height"] > 300
    on_resize_handler.reset()

    widget.style.width = 100
    await probe.redraw("Canvas should be tall and narrow")
    assert on_resize_handler.call_count >= 1
    assert on_resize_handler.call_args.args == (widget,)
    assert on_resize_handler.call_args.kwargs["width"] == 100
    assert on_resize_handler.call_args.kwargs["height"] > 300
    on_resize_handler.reset()

    widget.style.height = 100
    await probe.redraw("Canvas should be small")
    assert on_resize_handler.call_count >= 1
    assert on_resize_handler.call_args.args == (widget,)
    assert on_resize_handler.call_args.kwargs["width"] == 100
    assert on_resize_handler.call_args.kwargs["height"] == 100
    on_resize_handler.reset()

    del widget.style.width
    await probe.redraw("Canvas should be width of the screen")
    assert on_resize_handler.call_count >= 1
    assert on_resize_handler.call_args.args == (widget,)
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
    assert on_release_handler.mock_calls == [call(canvas, 20, 30), call(canvas, 20, 30)]
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
    with canvas.stroke(x=0, y=0, color=RED):
        canvas.line_to(x=200, y=200)
        canvas.move_to(x=200, y=0)
        canvas.line_to(x=0, y=200)

        canvas.rect(2, 2, 198, 198)

    await probe.redraw("Test image has been drawn")

    image = canvas.as_image()
    imageview = toga.ImageView(image)
    canvas.window.content.add(imageview)

    await probe.redraw("Cloned image should be visible")

    # Cloned image is the right size. The platform may do DPI scaling;
    # let the probe determine the correct scaled size.
    probe.assert_image_size(
        image.size,
        (200, 200),
        screen=canvas.window.screen,
        window=canvas.window,
    )


def assert_reference(probe, reference, threshold=0.01):
    """Assert that the canvas currently matches a reference image, within an
    RMS threshold"""
    # Get the canvas image.
    image = probe.get_image()
    scaled_image = image.resize((200, 200))

    # Look for a platform-specific reference variant.
    reference_variant = probe.reference_variant(reference)
    path = toga.App.app.paths.app / f"resources/canvas/{reference_variant}.png"
    save_dir = toga.App.app.paths.data / "canvas"

    def save():
        print(f"Saving to {save_dir}")
        save_dir.mkdir(parents=True, exist_ok=True)
        scaled_image.save(save_dir / f"{reference_variant}.png")
        image.save(save_dir / f"{reference_variant}-full.png")

    # If a reference image exists, scale the image to the same size as the reference,
    # and do an MSE comparison on every pixel in 0-1 RGBa (premultiplied) colorspace.
    if path.exists():
        reference_image = Image.open(path)

        difference = ImageChops.difference(
            scaled_image.convert("RGBa"),
            reference_image.convert("RGBa"),
        ).getdata()

        total_error = sum((diff / 255) ** 2 for diff in chain.from_iterable(difference))
        rmse = math.sqrt(total_error / 160_000)  # 200w * 200h * 4 bands
        # If the delta exceeds threshold, save the test image and fail the test.
        if rmse > threshold:
            save()
            pytest.fail(f"Rendered image doesn't match reference (RMSE=={rmse})")
    else:
        save()
        pytest.fail(f"Couldn't find {reference_variant!r} reference image")


async def test_transparency(canvas, probe):
    "Transparency is preserved in captured images"
    canvas.style.background_color = TRANSPARENT

    # Draw a rectangle. move_to is implied
    canvas.begin_path()
    canvas.rect(x=20, y=20, width=120, height=120)
    canvas.fill(color=REBECCAPURPLE)

    canvas.begin_path()
    canvas.rect(x=60, y=60, width=120, height=120)
    canvas.fill(color=rgb(0x33, 0x66, 0x99, 0.5))

    await probe.redraw("Image with transparent content and background")
    assert_reference(probe, "transparency")


async def test_paths(canvas, probe):
    "A path can be drawn"

    # A filled path closes automatically.
    canvas.begin_path()
    canvas.move_to(20, 20)
    canvas.line_to(140, 20)
    canvas.line_to(20, 140)
    canvas.fill()

    # A stroked path requires an explicit close. For an open stroke, see test_stroke.
    canvas.begin_path()
    # When there are two consecutive move_tos, the first one should leave no trace.
    canvas.move_to(140, 140)
    canvas.move_to(180, 180)
    canvas.line_to(180, 60)
    canvas.line_to(60, 180)
    canvas.close_path()
    canvas.stroke()

    # An empty path should not appear.
    canvas.begin_path()
    canvas.close_path()
    canvas.stroke(RED)

    # A path containing only move_to commands should not appear.
    canvas.begin_path()
    canvas.move_to(140, 140)
    canvas.move_to(160, 160)
    canvas.stroke(RED)

    # A path is not cleared after being stroked or filled.
    canvas.move_to(20, 10)
    canvas.line_to(60, 10)
    canvas.stroke(color=CORNFLOWERBLUE, line_width=10)
    canvas.move_to(60, 10)
    canvas.line_to(100, 10)
    canvas.fill(color=REBECCAPURPLE)
    canvas.line_to(140, 10)
    canvas.stroke()

    await probe.redraw("Pair of triangles and a black line should be drawn")
    assert_reference(probe, "paths", threshold=0.02)


async def test_bezier_curve(canvas, probe):
    "A Bézier curve can be drawn"

    canvas.begin_path()
    canvas.move_to(100, 44)
    canvas.bezier_curve_to(100, 40, 92, 20, 60, 20)
    canvas.bezier_curve_to(12, 20, 12, 80, 12, 80)
    canvas.bezier_curve_to(12, 108, 44, 144, 100, 172)
    canvas.bezier_curve_to(156, 144, 188, 108, 188, 80)
    canvas.bezier_curve_to(188, 80, 188, 20, 140, 20)
    canvas.bezier_curve_to(116, 20, 100, 40, 100, 44)
    canvas.stroke()

    await probe.redraw("Heart should be drawn")
    assert_reference(probe, "bezier_curve", threshold=0.03)


async def test_quadratic_curve(canvas, probe):
    "A quadratic curve can be drawn"

    canvas.begin_path()
    canvas.move_to(100, 20)
    canvas.quadratic_curve_to(20, 20, 20, 80)
    canvas.quadratic_curve_to(20, 140, 60, 140)
    canvas.quadratic_curve_to(60, 172, 28, 180)
    canvas.quadratic_curve_to(76, 172, 110, 140)
    canvas.quadratic_curve_to(180, 140, 180, 80)
    canvas.quadratic_curve_to(180, 20, 100, 20)
    canvas.stroke()

    await probe.redraw("Quote bubble should be drawn")
    assert_reference(probe, "quadratic_curve", threshold=0.03)


async def test_arc(canvas, probe):
    "An arc can be drawn"
    canvas.begin_path()

    # Face
    canvas.arc(100, 100, 80)

    # Smile (exactly half a turn)
    canvas.move_to(150, 100)
    canvas.arc(100, 100, 50, 0, pi, counterclockwise=False)

    # Hair (exactly half a turn, but in the opposite direction)
    canvas.move_to(190, 100)
    canvas.arc(100, 100, 90, 0, pi, counterclockwise=True)

    # Left eye
    canvas.move_to(70, 70)
    canvas.arc(64, 70, 6)

    # Right eye
    canvas.move_to(130, 70)
    canvas.arc(124, 70, 6)

    canvas.stroke()

    # Left eyebrow (less than half a turn)
    canvas.begin_path()
    canvas.arc(64, 70, 12, pi * 3 / 4, pi * 6 / 4)
    canvas.stroke()

    # Right eyebrow (less than half a turn, crossing the zero angle)
    canvas.begin_path()
    canvas.arc(124, 70, 12, pi * 6 / 4, pi * 1 / 4)
    canvas.stroke()

    await probe.redraw("Smiley face should be drawn")
    assert_reference(probe, "arc", threshold=0.03)


async def test_ellipse(canvas, probe):
    "An ellipse can be drawn"

    # Nucleus (filled circle)
    canvas.move_to(90, 100)
    canvas.ellipse(100, 100, 20, 20)
    canvas.fill(color=RED)

    # Purple orbit
    canvas.begin_path()
    canvas.ellipse(100, 100, 90, 20, rotation=pi * 3 / 4)
    canvas.stroke(color=REBECCAPURPLE)

    # Blue orbit (more than half a turn)
    canvas.begin_path()
    canvas.ellipse(
        100,
        100,
        radiusx=20,
        radiusy=90,
        rotation=-pi / 4,
        startangle=pi * 7 / 4,
        endangle=pi / 4,
        counterclockwise=True,
    )
    canvas.stroke(color=CORNFLOWERBLUE)

    # Yellow orbit (more than half a turn)
    canvas.begin_path()
    canvas.ellipse(
        100,
        100,
        radiusx=20,
        radiusy=90,
        startangle=pi / 4,
        endangle=pi * 7 / 4,
    )
    canvas.stroke(color=GOLDENROD)

    await probe.redraw("Atom should be drawn")
    assert_reference(probe, "ellipse", threshold=0.02)


async def test_ellipse_path(canvas, probe):
    "An elliptical arc can be connected to other segments of a path"

    ellipse_args = {
        "x": 100,
        "y": 100,
        "radiusx": 70,
        "radiusy": 40,
        "rotation": radians(30),
    }

    # Start of path -> arc
    canvas.ellipse(**ellipse_args, startangle=radians(80), endangle=radians(160))
    # Arc -> arc
    canvas.ellipse(**ellipse_args, startangle=radians(220), endangle=radians(260))
    canvas.stroke()

    canvas.begin_path()
    canvas.move_to(120, 20)
    # Move -> arc
    canvas.ellipse(**ellipse_args, startangle=radians(280), endangle=radians(340))
    # Arc -> line
    canvas.line_to(180, 50)
    canvas.stroke(RED)

    canvas.begin_path()
    canvas.move_to(180, 180)
    canvas.line_to(180, 160)
    # Line -> arc
    canvas.ellipse(**ellipse_args, startangle=radians(10), endangle=radians(60))
    canvas.stroke(CORNFLOWERBLUE)

    await probe.redraw("Broken ellipse with connected lines should be drawn")
    assert_reference(probe, "ellipse_path", threshold=0.02)


async def test_rect(canvas, probe):
    "A rectangle can be drawn"

    # Draw a rectangle. move_to is implied
    canvas.begin_path()
    canvas.rect(x=20, y=60, width=160, height=100)
    canvas.fill(color=REBECCAPURPLE)

    await probe.redraw("Filled rectangle should be drawn")
    assert_reference(probe, "rect")


async def test_round_rect(canvas, probe):
    "A rounded rectangle can be drawn"

    class Corner:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    # Draw a rounded rectangle. move_to is implied
    canvas.root_state.begin_path()
    canvas.root_state.round_rect(
        x=20, y=10, width=160, height=80, radii=[5, 30, Corner(50, 30)]
    )
    canvas.root_state.fill(color=GOLDENROD)
    canvas.root_state.stroke(color=REBECCAPURPLE)

    # Draw a rounded rectangle with negative width, height
    canvas.root_state.begin_path()
    canvas.root_state.round_rect(
        x=190, y=180, width=-160, height=-80, radii=[0, 30, Corner(50, 60)]
    )
    canvas.root_state.fill(color=CORNFLOWERBLUE)
    canvas.root_state.stroke(color=BLACK)

    await probe.redraw("Filled and stroked rounded rectangles should be drawn")
    assert_reference(probe, "round_rect", threshold=0.016)


async def test_fill(canvas, probe):
    "A fill can be drawn with primitives"
    # Draw a closed path
    canvas.begin_path()
    canvas.move_to(x=60, y=10)
    canvas.line_to(x=30, y=110)
    canvas.line_to(x=110, y=50)
    canvas.line_to(x=10, y=50)
    canvas.line_to(x=90, y=110)
    canvas.fill(color=REBECCAPURPLE)

    # Same path (slightly offset), but with EVENODD winding.
    canvas.begin_path()
    canvas.move_to(x=140, y=90)
    canvas.line_to(x=110, y=190)
    canvas.line_to(x=190, y=130)
    canvas.line_to(x=90, y=130)
    canvas.line_to(x=170, y=190)
    canvas.fill(color=CORNFLOWERBLUE, fill_rule=FillRule.EVENODD)

    await probe.redraw("Stars should be drawn")
    assert_reference(probe, "fill")


async def test_stroke(canvas, probe):
    "A stroke can be drawn with primitives"
    # Draw a closed path
    canvas.begin_path()
    canvas.move_to(x=20, y=20)
    canvas.line_to(x=100, y=20)
    canvas.line_to(x=180, y=180)
    canvas.line_to(x=100, y=180)
    canvas.close_path()
    canvas.stroke(color=REBECCAPURPLE)

    # Draw an open path inside it
    canvas.begin_path()
    # At the start of a path, line_to is equivalent to move_to.
    canvas.line_to(x=50, y=40)
    canvas.line_to(x=90, y=40)
    canvas.line_to(x=150, y=160)
    canvas.line_to(x=110, y=160)
    canvas.stroke(color=CORNFLOWERBLUE)

    await probe.redraw("Stroke should be drawn")
    assert_reference(probe, "stroke")


async def test_stroke_and_fill(canvas, probe):
    "A shape drawn with primitives can be stroked and filled."
    # Draw a closed path
    canvas.begin_path()
    canvas.move_to(x=20, y=20)
    canvas.line_to(x=100, y=20)
    canvas.line_to(x=180, y=180)
    canvas.line_to(x=100, y=180)
    canvas.close_path()
    canvas.stroke(color=REBECCAPURPLE)
    canvas.fill(color=CORNFLOWERBLUE)

    # Draw an open path inside it
    canvas.begin_path()
    # At the start of a path, line_to is equivalent to move_to.
    canvas.line_to(x=50, y=40)
    canvas.line_to(x=90, y=40)
    canvas.line_to(x=150, y=160)
    canvas.line_to(x=110, y=160)
    canvas.fill(color=GOLDENROD, fill_rule=FillRule.EVENODD)
    canvas.stroke(color=REBECCAPURPLE)

    await probe.redraw("Stroke should be drawn")
    assert_reference(probe, "stroke_and_fill")


async def test_closed_path_state(canvas, probe):
    "A closed path can be built with a state"

    # Build a parallelogram path
    with canvas.close_path(x=20, y=20):
        canvas.line_to(x=100, y=20)
        canvas.line_to(x=180, y=180)
        canvas.line_to(x=100, y=180)

    # Draw it with a thick dashed line
    canvas.stroke(color=REBECCAPURPLE, line_width=5, line_dash=[20, 30])

    await probe.redraw("Closed path should be drawn with state")
    assert_reference(probe, "closed_path_state")


async def test_fill_state(canvas, probe):
    "A fill path can be built with a state"

    # Build a filled parallelogram
    with canvas.fill(x=20, y=20, color=REBECCAPURPLE):
        canvas.line_to(x=100, y=20)
        canvas.line_to(x=180, y=180)
        canvas.line_to(x=100, y=180)

    await probe.redraw("Fill should be drawn with state")
    assert_reference(probe, "fill_state")


async def test_stroke_state(canvas, probe):
    "A stroke can be drawn with a state"
    # Draw a thin line
    with canvas.stroke(x=40, y=20, color=REBECCAPURPLE):
        canvas.line_to(x=80, y=180)

    # Draw a thick dashed line
    with canvas.stroke(
        x=80, y=20, line_width=20, line_dash=[20, 10], color=CORNFLOWERBLUE
    ):
        canvas.line_to(x=120, y=180)

    await probe.redraw("Stroke should be drawn with state")
    assert_reference(probe, "stroke_state")


async def test_stroke_and_fill_state(canvas, probe):
    "A shape can be stroked and filled using states"

    # Draw a filled parallelogram
    with canvas.fill(x=20, y=20, color=REBECCAPURPLE):
        with canvas.stroke(line_width=20, line_dash=[20, 10], color=CORNFLOWERBLUE):
            canvas.line_to(x=100, y=20)
            canvas.line_to(x=180, y=180)
            canvas.line_to(x=100, y=180)

    await probe.redraw("Stroke and Fill should be drawn with state")
    assert_reference(probe, "stroke_and_fill_state")


async def test_nested_stroke_and_fill_state(canvas, probe):
    """Inner states don't override unsupplied attributes."""
    with canvas.fill(color=GOLDENROD):
        with canvas.fill():
            # Should still be goldenrod
            canvas.rect(10, 10, 50, 50)

    with canvas.stroke(color=REBECCAPURPLE, line_width=15, line_dash=[15, 14]):
        with canvas.stroke():
            # Should still be wide, dashed, and purple
            canvas.move_to(100, 10)
            canvas.line_to(100, 150)

    await probe.redraw("Nested stroke and fill states should be drawn")
    assert_reference(probe, "nested_stroke_and_fill_state")


async def test_transforms(canvas, probe):
    "Transforms can be applied"

    # Draw a rectangle after a horizontal translation
    canvas.translate(160, 20)
    canvas.rect(0, 0, 20, 60)
    canvas.fill(color=CORNFLOWERBLUE)

    canvas.reset_transform()
    canvas.begin_path()
    canvas.rotate(pi / 4)
    canvas.rect(200, 0, 20, 60)
    canvas.fill(color=REBECCAPURPLE)

    canvas.reset_transform()
    canvas.begin_path()
    canvas.scale(2, 5)
    canvas.rect(10, 10, 10, 10)
    canvas.fill(color=GOLDENROD)

    canvas.reset_transform()
    canvas.begin_path()
    canvas.translate(100, 60)
    canvas.rotate(pi / 7 * 4)
    canvas.scale(5, 2)
    canvas.rect(2, 2, 10, 10)
    canvas.fill()

    await probe.redraw("Transforms can be applied")
    assert_reference(probe, "transforms")


async def test_transforms_mid_path(canvas, probe):
    "Transforms can be applied mid-path"

    # draw a series of rotated rectangles
    canvas.begin_path()
    canvas.translate(100, 100)
    with canvas.state():
        for _ in range(12):
            canvas.rect(50, 0, 10, 10)
            canvas.scale(1.1, 1)
            canvas.rotate(math.pi / 6)

    canvas.fill()
    canvas.stroke(GOLDENROD)

    # draw a series of line segments
    canvas.begin_path()
    canvas.move_to(25, 0)
    for _ in range(12):
        canvas.line_to(25, 0)
        canvas.rotate(math.pi / 6)
        canvas.translate(5, 3)
    canvas.close_path()
    canvas.reset_transform()
    canvas.move_to(110, 100)
    canvas.scale(5, 1)
    canvas.ellipse(20, 100, 2, 20, 0, 0, 2 * pi)
    canvas.stroke(CORNFLOWERBLUE)

    await probe.redraw("Transforms can be applied")
    assert_reference(probe, "transforms_mid_path", threshold=0.015)


async def test_singular_transforms(canvas, probe):
    "Singular transforms behave reasonably"
    canvas.begin_path()
    with canvas.state():
        # flip about the line x = y
        canvas.rotate(-pi / 2)
        canvas.scale(-1, 1)

        canvas.move_to(40, 20)
        canvas.line_to(80, 20)
        canvas.line_to(100, 30)

        with canvas.state():
            # Apply a scale factor of zero
            canvas.scale(0.9, 0)
            canvas.line_to(180, 20)

        canvas.rotate(pi / 4)
        canvas.line_to(180, 20)

        canvas.stroke(GOLDENROD, line_width=8)

    # Same shape, but not flipped, using reset_transform()
    canvas.begin_path()

    canvas.move_to(40, 20)
    canvas.line_to(80, 20)
    canvas.line_to(100, 30)

    # Apply a scale factor of zero
    canvas.scale(0.9, 0)
    canvas.line_to(180, 20)
    # Total transform is singular
    canvas.reset_transform()

    canvas.rotate(pi / 4)
    canvas.line_to(180, 20)

    canvas.stroke(CORNFLOWERBLUE, line_width=8)

    canvas.reset_transform()
    canvas.begin_path()
    canvas.scale(0, 0.9)
    canvas.translate(50, 50)

    canvas.rect(0, 0, 25, 25)

    # Should draw nothing.
    canvas.fill()
    canvas.stroke(line_width=10)

    await probe.redraw("Transforms can be applied")
    assert_reference(probe, "singular_transforms")


@pytest.mark.xfail(
    condition=os.environ.get("RUNNING_IN_CI") != "true",
    reason="Canvas tests are unstable outside of CI. Manual inspection may be required",
)
async def test_write_text(canvas, probe):
    "Text can be measured and written"

    # Use fonts which look different from the system fonts on all platforms.
    Font.register("Droid Serif", "resources/fonts/DroidSerif-Regular.ttf")
    Font.register("Droid Serif", "resources/fonts/DroidSerif-Bold.ttf", weight=BOLD)
    Font.register("Endor", "resources/fonts/ENDOR___.ttf")

    hello_text = "Hello"
    hello_font = Font("Droid Serif", 12)
    hello_size = canvas.measure_text(hello_text, hello_font)

    with canvas.stroke(color=CORNFLOWERBLUE):
        canvas.rect(
            100 - (hello_size[0] // 2),
            10,
            hello_size[0],
            hello_size[1],
        )
    with canvas.fill(color=REBECCAPURPLE):
        canvas.write_text(
            hello_text,
            100 - (hello_size[0] // 2),
            10,
            font=hello_font,
            baseline=Baseline.TOP,
        )

    world_text = "World!"
    world_font = Font("Endor", 22)
    world_size = canvas.measure_text(world_text, font=world_font)

    with canvas.stroke(color=CORNFLOWERBLUE):
        canvas.rect(
            100 - (world_size[0] // 2),
            100 - world_size[1],
            world_size[0],
            world_size[1],
        )
    with canvas.stroke(line_width=1):
        canvas.write_text(
            world_text,
            100 - (world_size[0] // 2),
            100,
            font=world_font,
            baseline=Baseline.BOTTOM,
        )

    toga_text = "Toga"
    toga_font = Font("Droid Serif", 45, weight=BOLD)
    toga_size = canvas.measure_text(toga_text, font=toga_font)

    with canvas.stroke(color=CORNFLOWERBLUE):
        canvas.rect(
            100 - (toga_size[0] // 2),
            150 - (toga_size[1] // 2),
            toga_size[0],
            toga_size[1],
        )
    with canvas.stroke(color=REBECCAPURPLE):
        with canvas.fill(color=CORNFLOWERBLUE):
            canvas.write_text(
                toga_text,
                100 - (toga_size[0] // 2),
                150,
                font=toga_font,
                baseline=Baseline.MIDDLE,
            )

    await probe.redraw("Text should be drawn")
    # 0.035 is equivalent to 49 pixels out of 4,000 being 100% the wrong color
    # (in premultiplied RGBa space). However, fonts are the worst case for evaluating
    # with RMSE, as they are 100% edges; and due to minor font rendering discrepancies
    # and antialiasing introduced by image scaling, edges are the source of error. Of
    # note, though: Gtk on Wayland is the only backend that needs it set this high.
    # Everything else falls below 0.02.
    assert_reference(probe, "write_text", threshold=0.035)


@pytest.mark.xfail(
    condition=os.environ.get("RUNNING_IN_CI") != "true",
    reason="may fail outside of a GitHub runner environment",
)
async def test_multiline_text(canvas, probe):
    "Multiline text can be measured and written"

    # Vertical guidelines
    X = [10, 75, 140]
    with canvas.stroke(color=RED):
        for x in X:
            canvas.move_to(x, 0)
            canvas.line_to(x, canvas.style.height)

    def caption(baseline):
        return f"{baseline.name.capitalize()}\nTwo\nThree"

    # ALPHABETIC baseline
    y = 30
    with canvas.stroke(color=RED):
        canvas.move_to(0, y)
        canvas.line_to(canvas.style.width, y)

    with canvas.fill():
        # Default baseline (ALPHABETIC), with default font and various sizes.
        x = X[0]
        for size in [8, 12, 16, 20]:
            text = f"{size:02d}"
            font = Font(SYSTEM, size)
            canvas.write_text(text, x, y, font)
            x += canvas.measure_text(text, font)[0] + 5

        # Empty text: this should have no effect on the image, but make sure it's
        # accepted.
        canvas.write_text("", X[1], y)

        # Explicit ALPHABETIC baseline, with default font and size but specified
        # line height. On most systems, this will go off the right edge of the canvas.
        line_height = 2.5
        canvas.write_text(
            caption(Baseline.ALPHABETIC), X[2], y, line_height=line_height
        )

    # Other baselines, with default font but specified size
    y = 130
    with canvas.stroke(color=RED):
        canvas.move_to(0, y)
        canvas.line_to(canvas.style.width, y)
    font = Font(SYSTEM, 12)

    for i, baseline in enumerate([Baseline.BOTTOM, Baseline.MIDDLE, Baseline.TOP]):
        text = caption(baseline)
        width, height = canvas.measure_text(text, font)
        left = X[i]
        if baseline == Baseline.TOP:
            top = y
        elif baseline == Baseline.MIDDLE:
            top = round(y - (height / 2))
        elif baseline == Baseline.BOTTOM:
            top = y - height

        with canvas.stroke(color=CORNFLOWERBLUE):
            canvas.rect(left, top, width, height)

        with canvas.fill():
            canvas.write_text(text, left, y, font, baseline)

    await probe.redraw("Multiple text blocks should be drawn")
    assert_reference(probe, "multiline_text")


@pytest.mark.xfail(
    condition=os.environ.get("RUNNING_IN_CI") != "true",
    reason="may fail outside of a GitHub runner environment",
)
async def test_write_text_and_path(canvas, probe):
    "Text doesn't affect the current path."

    # Use fonts which look different from the system fonts on all platforms.
    Font.register("Droid Serif", "resources/fonts/DroidSerif-Regular.ttf")

    hello_text = "Hello"
    hello_font = Font("Droid Serif", 24)
    hello_size = canvas.measure_text(hello_text, hello_font)

    with canvas.fill(BLACK):
        # start building a path
        canvas.begin_path()
        canvas.rect(
            100 - (hello_size[0] // 2),
            10,
            hello_size[0],
            hello_size[1],
        )

        # Draw some text independent of the path
        # Uses fill color of black.
        canvas.write_text(
            hello_text,
            100 - (hello_size[0] // 2),
            10,
            font=hello_font,
            baseline=Baseline.TOP,
        )

        # continue building the path
        canvas.move_to(
            100 - (hello_size[0] // 2),
            10,
        )
        canvas.line_to(
            100 + (hello_size[0] // 2),
            10 + hello_size[1],
        )

        # now stroke the path, but *not* the text
        canvas.stroke(CORNFLOWERBLUE)

        # start a new path so Fill state doesn't fill current path with black
        canvas.begin_path()

    await probe.redraw("Text and path should be drawn independently")
    assert_reference(probe, "write_text_and_path", 0.04)


async def test_draw_image_at_point(canvas, probe):
    "Images can be drawn at a point."

    image = TogaImage("resources/sample.png")
    canvas.begin_path()
    canvas.draw_image(image, 10, 10)

    await probe.redraw("Image should be drawn")
    assert_reference(probe, "draw_image", threshold=0.05)


async def test_draw_image_in_rect(canvas, probe):
    "Images can be drawn in a rectangle."

    image = TogaImage("resources/sample.png")
    canvas.begin_path()
    canvas.translate(82, 46)
    canvas.rotate(-pi / 6)
    canvas.translate(-82, -46)
    canvas.draw_image(image, 10, 10, 72, 144)
    canvas.rect(10, 10, 72, 144)
    canvas.stroke(REBECCAPURPLE)

    await probe.redraw("Image should be drawn")
    assert_reference(probe, "draw_image_in_rect", threshold=0.05)
