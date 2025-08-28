# Handled differently in real testing with get_module()
from tests.tests_backend.widgets.button import ButtonProbe
from tests.tests_backend.proxies.button_proxy import ButtonProxy
#from ..tests_backend.widgets.button import ButtonProbe
#from ..tests_backend.proxies.button_proxy import ButtonProxy

from tests.data import TEXTS

from pytest import approx, fixture

@fixture
async def widget():
    return ButtonProxy()

async def test_text(widget, probe):
    "The text displayed on a button can be changed"
    initial_height = probe.height

    for text in TEXTS:
        widget.text = text

        # no-op
        #await probe.redraw(f"Button text should be {text}")

        # Text after a newline will be stripped.
        assert isinstance(widget.text, str)
        expected = str(text).split("\n")[0]
        assert widget.text == expected
        assert probe.text == expected
        # GTK rendering can result in a very minor change in button height
        assert probe.height == approx(initial_height, abs=1)



"""
async def test_text_change(widget, probe):
    initial_height = probe.height

    widget.text = "new text"

    assert isinstance(widget.text, str)
    expected = str("new text").split("\n")[0]

    assert widget.text == expected
    assert probe.text == expected

    assert probe.height == approx(initial_height, abs=1)
"""