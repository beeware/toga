from ..utils import COLORS, TEXTS, assert_color, assert_set_get


async def test_text(widget, probe):
    for text in TEXTS:
        assert_set_get(widget, "text", text)
        assert probe.text == text


async def test_color(widget, probe):
    for color in COLORS:
        widget.style.color = color
        assert_color(probe.color, color)


async def test_background_color(widget, probe):
    for color in COLORS:
        widget.style.background_color = color
        assert_color(probe.background_color, color)
