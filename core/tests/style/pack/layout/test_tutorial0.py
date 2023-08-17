from travertino.size import at_least

from toga.style.pack import COLUMN, Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


def test_tutorial_0():
    root = ExampleNode(
        "app",
        style=Pack(),
        children=[
            ExampleNode(
                "button", style=Pack(flex=1, padding=50), size=(at_least(120), 30)
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (220, 130),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [{"origin": (50, 50), "content": (540, 30)}],
        },
    )


def test_vertical():
    root = ExampleNode(
        "app",
        style=Pack(direction=COLUMN),
        children=[
            # ExampleNode('button', style=Pack(flex=1), size=(30, at_least(120))),
            ExampleNode(
                "button", style=Pack(flex=1, padding=50), size=(30, at_least(120))
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(480, 640))
    assert_layout(
        root,
        (130, 220),
        (480, 640),
        {
            "origin": (0, 0),
            "content": (480, 640),
            "children": [{"origin": (50, 50), "content": (30, 540)}],
        },
    )
