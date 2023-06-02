from travertino.size import at_least

from toga.style.pack import Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


def test_fixed_size():
    root = ExampleNode(
        "app",
        style=Pack(),
        children=[
            ExampleNode(
                "first",
                style=Pack(width=100, height=100),
                size=(at_least(0), at_least(0)),
            ),
            ExampleNode(
                "second",
                style=Pack(width=100, height=100),
                size=(at_least(50), at_least(50)),
                children=[
                    ExampleNode(
                        "child",
                        style=Pack(width=50, height=50),
                        size=(at_least(0), at_least(0)),
                    ),
                ],
            ),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (200, 100),
        {
            "origin": (0, 0),
            "content": (200, 100),
            "children": [
                {"origin": (0, 0), "content": (100, 100)},
                {
                    "origin": (100, 0),
                    "content": (100, 100),
                    "children": [
                        {"origin": (100, 0), "content": (50, 50)},
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
                {"origin": (0, 0), "content": (100, 100)},
                {
                    "origin": (100, 0),
                    "content": (100, 100),
                    "children": [
                        {"origin": (100, 0), "content": (50, 50)},
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
                {"origin": (0, 0), "content": (150, 150)},
                {
                    "origin": (150, 0),
                    "content": (150, 150),
                    "children": [
                        {"origin": (150, 0), "content": (75, 75)},
                    ],
                },
            ],
        },
    )
