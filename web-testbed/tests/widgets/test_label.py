from pytest import approx, fixture

import toga


@fixture
async def widget():
    return toga.Label("hello, this is a label")


async def test_multiline(widget, probe):
    """If the label contains multiline text, it resizes vertically."""

    def make_lines(n):
        return "\n".join(f"This is line {i}" for i in range(n))

    widget.text = make_lines(1)
    await probe.redraw("Label should be resized vertically")
    line_height = probe.height
    print(probe.height)

    # Label should have a significant width.
    assert probe.width > 50

    # Empty text should not cause the widget to collapse.
    widget.text = ""
    print(probe.height)

    await probe.redraw("Label text should be empty")
    assert probe.height == line_height
    # Label should have almost 0 width
    assert probe.width < 10

    widget.text = make_lines(2)
    await probe.redraw("Label text should be changed to 2 lines")
    assert probe.height == approx(line_height * 2, rel=0.1)
    line_spacing = probe.height - (line_height * 2)

    for n in range(3, 6):
        widget.text = make_lines(n)
        await probe.redraw(f"Label text should be changed to {n} lines")
        # Label height should reflect the number of lines
        assert probe.height == approx(
            (line_height * n) + (line_spacing * (n - 1)),
            rel=0.1,
        )
        # Label should have a significant width.
        assert probe.width > 50
