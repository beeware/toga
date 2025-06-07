from toga.style.pack import COLUMN, NONE, PACK, Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


def test_display_none():
    """Setting a node to display=NONE removes it from the layout."""
    root = ExampleNode(
        "app",
        style=Pack(direction=COLUMN),
        children=[
            ExampleNode(
                "first",
                style=Pack(width=100, height=110),
            ),
            rabbit := ExampleNode(
                "second",
                style=Pack(width=100, height=120),
            ),
            ExampleNode(
                "third",
                style=Pack(width=100, height=130),
            ),
        ],
    )

    root.style.layout(ExampleViewport(640, 480))
    initial = (
        root,
        (100, 360),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (100, 110),
                },
                {
                    "origin": (0, 110),
                    "content": (100, 120),
                },
                {
                    "origin": (0, 230),
                    "content": (100, 130),
                },
            ],
        },
    )
    assert_layout(*initial)

    # Turn off display for the middle child.
    rabbit.style.display = NONE

    root.style.layout(ExampleViewport(640, 480))
    assert_layout(
        root,
        (100, 240),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (100, 110),
                },
                # As far as the vanished node knows, its values haven't changed, because
                # its layout hasn't been refreshed.
                {
                    "origin": (0, 110),
                    "content": (100, 120),
                },
                # But the third child has slid upward to take its place.
                {
                    "origin": (0, 110),
                    "content": (100, 130),
                },
            ],
        },
    )

    rabbit.style.display = PACK

    # Everything's back to normal.
    root.style.layout(ExampleViewport(640, 480))
    assert_layout(*initial)
