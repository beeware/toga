from pytest import approx, fixture, mark

import toga

from .properties import (  # noqa: F401
    test_background_color,
    test_color,
    test_text,
)


@fixture
async def widget():
    return toga.Label("")


# TODO: a `width` test, for any widget whose width depends on its text.
@mark.skip("Fails on Windows, probably because of #1289")
async def test_multiline(widget, probe):
    def make_lines(n):
        return "\n".join(f"line{i}" for i in range(n))

    widget.text = make_lines(1)
    # TODO: Android at least will need an `await` after each text change, to give the
    # native layout a chance to update.
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
