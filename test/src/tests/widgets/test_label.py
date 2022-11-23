from pytest import approx, fixture

import toga

from ..test_data import COLORS, TEXTS
from ..test_utils import set_get


@fixture
async def new_widget():
    return toga.Label("")


async def test_text(widget, probe):
    for text in TEXTS:
        set_get(widget, "text", text)
        assert probe.text == text


async def test_color(widget, probe):
    for color in COLORS:
        widget.style.color = color
        for component in ["r", "g", "b"]:
            assert getattr(probe.color, component) == getattr(color, component)
        assert probe.color.a == approx(color.a, abs=(1 / 256))


async def test_multiline(widget, probe):
    def make_lines(n):
        return "\n".join(f"line{i}" for i in range(n))

    widget.text = make_lines(1)
    line_height = probe.height

    widget.text = make_lines(2)
    assert probe.height == approx(line_height * 2, rel=0.1)
    line_spacing = probe.height - (line_height * 2)

    for n in range(3, 10):
        widget.text = make_lines(n)
        assert probe.height == approx(
            (line_height * n) + (line_spacing * (n - 1)),
            rel=0.1,
        )
