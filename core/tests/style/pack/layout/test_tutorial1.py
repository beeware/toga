from travertino.size import at_least

from toga.style.pack import COLUMN, ROW, Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


def test_tutorial_1():
    root = ExampleNode(
        "app",
        style=Pack(direction=COLUMN, padding_top=10),
        children=[
            ExampleNode(
                "f_box",
                style=Pack(direction=ROW, padding=5),
                children=[
                    ExampleNode(
                        "f_input",
                        style=Pack(flex=1, padding_left=160),
                        size=(at_least(100), 15),
                    ),
                    ExampleNode(
                        "f_label",
                        style=Pack(width=100, padding_left=10),
                        size=(at_least(40), 10),
                    ),
                ],
            ),
            ExampleNode(
                "c_box",
                style=Pack(direction=ROW, padding=5),
                children=[
                    ExampleNode(
                        "join_label",
                        style=Pack(width=150, padding_right=10),
                        size=(at_least(80), 10),
                    ),
                    ExampleNode(
                        "c_input", style=Pack(flex=1), size=(at_least(100), 15)
                    ),
                    ExampleNode(
                        "c_label",
                        style=Pack(width=100, padding_left=10),
                        size=(at_least(40), 10),
                    ),
                ],
            ),
            ExampleNode(
                "button", style=Pack(flex=1, padding=15), size=(at_least(120), 30)
            ),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (380, 120),
        {
            "origin": (0, 10),
            "content": (380, 110),
            "children": [
                {
                    "origin": (5, 15),
                    "content": (370, 15),
                    "children": [
                        {"origin": (165, 15), "content": (100, 15)},
                        {"origin": (275, 15), "content": (100, 10)},
                    ],
                },
                {
                    "origin": (5, 40),
                    "content": (370, 15),
                    "children": [
                        {"origin": (5, 40), "content": (150, 10)},
                        {"origin": (165, 40), "content": (100, 15)},
                        {"origin": (275, 40), "content": (100, 10)},
                    ],
                },
                {"origin": (15, 75), "content": (120, 30)},
            ],
        },
    )

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
        (640, 480),
        {
            "origin": (0, 10),
            "content": (640, 470),
            "children": [
                {
                    "origin": (5, 15),
                    "content": (630, 15),
                    "children": [
                        {"origin": (165, 15), "content": (360, 15)},
                        {"origin": (535, 15), "content": (100, 10)},
                    ],
                },
                {
                    "origin": (5, 40),
                    "content": (630, 15),
                    "children": [
                        {"origin": (5, 40), "content": (150, 10)},
                        {"origin": (165, 40), "content": (360, 15)},
                        {"origin": (535, 40), "content": (100, 10)},
                    ],
                },
                {"origin": (15, 75), "content": (610, 30)},
            ],
        },
    )
    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
        (640, 480),
        {
            "origin": (0, 15),
            "content": (640, 465),
            "children": [
                {
                    "origin": (7, 22),
                    "content": (626, 15),
                    "children": [
                        {"origin": (247, 22), "content": (221, 15)},
                        {"origin": (483, 22), "content": (150, 10)},
                    ],
                },
                {
                    "origin": (7, 51),
                    "content": (626, 15),
                    "children": [
                        {"origin": (7, 51), "content": (225, 10)},
                        {"origin": (247, 51), "content": (221, 15)},
                        {"origin": (483, 51), "content": (150, 10)},
                    ],
                },
                {"origin": (22, 95), "content": (596, 30)},
            ],
        },
    )
