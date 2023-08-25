from travertino.size import at_least

from toga.style.pack import COLUMN, Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


def test_tutorial_3():
    root = ExampleNode(
        "app",
        style=Pack(direction=COLUMN),
        children=[
            ExampleNode(
                "box",
                style=Pack(),
                children=[
                    ExampleNode(
                        "input",
                        style=Pack(flex=1, padding=5),
                        size=(at_least(100), 15),
                    ),
                    ExampleNode(
                        "button",
                        style=Pack(width=50, padding=5),
                        size=(at_least(40), 10),
                    ),
                ],
            ),
            ExampleNode("web", style=Pack(flex=1), size=(at_least(100), at_least(100))),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (170, 125),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (640, 25),
                    "children": [
                        {"origin": (5, 5), "content": (570, 15)},
                        {"origin": (585, 5), "content": (50, 10)},
                    ],
                },
                {"origin": (0, 25), "content": (640, 455)},
            ],
        },
    )
