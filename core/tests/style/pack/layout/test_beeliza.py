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

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (160, 125),
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
