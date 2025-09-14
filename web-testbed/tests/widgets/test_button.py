from pytest import approx, fixture
from tests.data import TEXTS
from tests.tests_backend.proxies.button_proxy import ButtonProxy
from tests.tests_backend.proxies.mock_proxy import MockProxy


@fixture
async def widget():
    return ButtonProxy("Hello")


async def test_text(widget, probe):
    "The text displayed on a button can be changed"
    initial_height = probe.height

    for text in TEXTS:
        widget.text = text

        # no-op
        # await probe.redraw(f"Button text should be {text}")

        # Text after a newline will be stripped.
        assert isinstance(widget.text, str)
        expected = str(text).split("\n")[0]
        assert widget.text == expected
        assert probe.text == expected
        # GTK rendering can result in a very minor change in button height
        assert probe.height == approx(initial_height, abs=1)


async def test_press(widget, probe):
    # Press the button before installing a handler
    await probe.press()

    # Set up a mock handler, and press the button again.
    # Changed to MockProxy - objects created in test suite need a proxy
    # to one in the remote web app.
    handler = MockProxy()
    widget.on_press = handler
    await probe.press()  # Includes a no-op tick, not needed though

    # no-op
    # await probe.redraw("Button should be pressed")

    handler.assert_called_once_with(widget)


TRANSPARENT = "transparent"


async def test_background_color_transparent(widget, probe):
    "Buttons treat background transparency as a color reset."
    del widget.style.background_color
    original_background_color = probe.background_color

    widget.style.background_color = TRANSPARENT
    # await probe.redraw("Button background color should be reset to the default color")
    assert_background_color(probe.background_color, original_background_color)


def assert_background_color(actual, expected):
    # For platforms where alpha blending is manually implemented, the
    # probe.background_color property returns a tuple consisting of:
    #   - The widget's background color
    #   - The widget's parent's background color
    #   - The widget's original alpha value - Required for deblending
    if isinstance(actual, tuple):
        actual_widget_bg, actual_parent_bg, actual_widget_bg_alpha = actual
        if actual_widget_bg_alpha == 0:
            # Since a color having an alpha value of 0 cannot be deblended.
            # So, the deblended widget color would be equal to the parent color.
            deblended_actual_widget_bg = actual_parent_bg
        else:
            deblended_actual_widget_bg = actual_widget_bg.unblend_over(
                actual_parent_bg, actual_widget_bg_alpha
            )
        if isinstance(expected, tuple):
            expected_widget_bg, expected_parent_bg, expected_widget_bg_alpha = expected
            if expected_widget_bg_alpha == 0:
                # Since a color having an alpha value of 0 cannot be deblended.
                # So, the deblended widget color would be equal to the parent color.
                deblended_expected_widget_bg = expected_parent_bg
            else:
                deblended_expected_widget_bg = expected_widget_bg.unblend_over(
                    expected_parent_bg, expected_widget_bg_alpha
                )
            assert_color(deblended_actual_widget_bg, deblended_expected_widget_bg)
        # For comparison when expected is a single value object
        else:
            if (expected == TRANSPARENT) or (
                expected.a == 0
                # Since a color having an alpha value of 0 cannot be deblended to
                # get the exact original color, as deblending in such cases would
                # lead to a division by zero error. So, just check that widget and
                # parent have the same color.
            ):
                assert_color(actual_widget_bg, actual_parent_bg)
            elif expected.a != 1:
                assert_color(deblended_actual_widget_bg, expected)
            else:
                assert_color(actual_widget_bg, expected)
    # For other platforms
    else:
        assert_color(actual, expected)


def assert_color(actual, expected):
    if expected in {None, TRANSPARENT}:
        assert expected == actual
    else:
        if actual in {None, TRANSPARENT}:
            assert expected == actual
        else:
            assert (actual.r, actual.g, actual.b, actual.a) == (
                expected.r,
                expected.g,
                expected.b,
                approx(expected.a, abs=(1 / 255)),
            )
