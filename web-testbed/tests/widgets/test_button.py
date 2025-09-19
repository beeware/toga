from pytest import approx, fixture
from tests.assertions import assert_background_color
from tests.data import TEXTS
from tests.tests_backend.proxies.button_proxy import ButtonProxy
from tests.tests_backend.proxies.mock_proxy import MockProxy

TRANSPARENT = "transparent"


@fixture
async def widget():
    return ButtonProxy("Hello")


async def test_text(widget, probe):
    "The text displayed on a button can be changed"
    initial_height = probe.height

    for text in TEXTS:
        widget.text = text

        await probe.redraw(f"Button text should be {text}")

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
    await probe.press()

    await probe.redraw("Button should be pressed")

    handler.assert_called_once_with(widget)


async def test_background_color_transparent(widget, probe):
    "Buttons treat background transparency as a color reset."
    del widget.style.background_color
    original_background_color = probe.background_color

    widget.style.background_color = TRANSPARENT
    await probe.redraw("Button background color should be reset to the default color")
    assert_background_color(probe.background_color, original_background_color)
