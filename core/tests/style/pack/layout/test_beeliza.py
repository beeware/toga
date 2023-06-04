from travertino.size import at_least

from toga.style.pack import COLUMN, ROW, Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


def test_beeliza():
    root = ExampleNode(
        "app",
        style=Pack(direction=COLUMN),
        children=[
            ExampleNode(
                "detailedlist",
                style=Pack(flex=1),
                size=(at_least(100), at_least(100)),
            ),
            ExampleNode(
                "box",
                style=Pack(direction=ROW),
                children=[
                    ExampleNode(
                        "input",
                        style=Pack(flex=1, padding=5),
                        size=(at_least(100), 15),
                    ),
                    ExampleNode(
                        "button", style=Pack(padding=5), size=(at_least(40), 10)
                    ),
                ],
            ),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (160, 125),
        {
            "origin": (0, 0),
            "content": (160, 125),
            "children": [
                {"origin": (0, 0), "content": (100, 100)},
                {
                    "origin": (0, 100),
                    "content": (160, 25),
                    "children": [
                        {"origin": (5, 105), "content": (100, 15)},
                        {"origin": (115, 105), "content": (40, 10)},
                    ],
                },
            ],
        },
    )

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": (0, 0), "content": (640, 455)},
                {
                    "origin": (0, 455),
                    "content": (640, 25),
                    "children": [
                        {"origin": (5, 460), "content": (580, 15)},
                        {"origin": (595, 460), "content": (40, 10)},
                    ],
                },
            ],
        },
    )

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": (0, 0), "content": (640, 451)},
                {
                    "origin": (0, 451),
                    "content": (640, 29),
                    "children": [
                        {"origin": (7, 458), "content": (572, 15)},
                        {"origin": (593, 458), "content": (40, 10)},
                    ],
                },
            ],
        },
    )
