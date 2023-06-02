from travertino.size import at_least

from toga.style.pack import (
    BOTTOM,
    CENTER,
    COLUMN,
    LEFT,
    RIGHT,
    ROW,
    RTL,
    TOP,
    Pack,
)

from .utils import ExampleNode, ExampleViewport


def assert_layout(node, size, layout):
    assert (node.layout.width, node.layout.height) == size, "final size doesn't match"
    _assert_layout(node, layout)


def _assert_layout(node, layout):
    assert (
        node.layout.absolute_content_left,
        node.layout.absolute_content_top,
    ) == layout["origin"], f"origin of {node} doesn't match"
    assert (node.layout.content_width, node.layout.content_height) == layout[
        "content"
    ], f"content of {node} doesn't match"

    assert len(node.children) == len(
        layout.get("children", [])
    ), f"number of children of {node} doesn't match"

    for child, sublayout in zip(node.children, layout.get("children", [])):
        _assert_layout(child, sublayout)


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

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (220, 130),
        {
            "origin": (0, 0),
            "content": (220, 130),
            "children": [{"origin": (50, 50), "content": (120, 30)}],
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
            "children": [{"origin": (50, 50), "content": (540, 30)}],
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
            "children": [{"origin": (75, 75), "content": (490, 30)}],
        },
    )


def test_tutorial_0_vertical():
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

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (130, 220),
        {
            "origin": (0, 0),
            "content": (130, 220),
            "children": [{"origin": (50, 50), "content": (30, 120)}],
        },
    )

    # Normal size
    root.style.layout(root, ExampleViewport(480, 640, dpi=96))
    assert_layout(
        root,
        (480, 640),
        {
            "origin": (0, 0),
            "content": (480, 640),
            "children": [{"origin": (50, 50), "content": (30, 540)}],
        },
    )

    # HiDPI normal size
    root.style.layout(root, ExampleViewport(480, 640, dpi=144))
    assert_layout(
        root,
        (480, 640),
        {
            "origin": (0, 0),
            "content": (480, 640),
            "children": [{"origin": (75, 75), "content": (30, 490)}],
        },
    )


def test_tutorial_0_high_baseline_dpi():
    root = ExampleNode(
        "app",
        style=Pack(),
        children=[
            ExampleNode(
                "button", style=Pack(flex=1, padding=50), size=(at_least(120), 30)
            ),
        ],
    )

    # Minimum size with high baseline DPI
    root.style.layout(root, ExampleViewport(0, 0, dpi=160, baseline_dpi=160))
    assert_layout(
        root,
        (220, 130),
        {
            "origin": (0, 0),
            "content": (220, 130),
            "children": [{"origin": (50, 50), "content": (120, 30)}],
        },
    )

    # Normal size with high DPI equal to high baseline DPI
    root.style.layout(root, ExampleViewport(640, 480, dpi=160, baseline_dpi=160))
    assert_layout(
        root,
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [{"origin": (50, 50), "content": (540, 30)}],
        },
    )

    # HiDPI -- 1.5x baseline -- with higher baseline DPI
    root.style.layout(root, ExampleViewport(640, 480, dpi=240, baseline_dpi=160))
    assert_layout(
        root,
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [{"origin": (75, 75), "content": (490, 30)}],
        },
    )


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

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (170, 125),
        {
            "origin": (0, 0),
            "content": (170, 125),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (170, 25),
                    "children": [
                        {"origin": (5, 5), "content": (100, 15)},
                        {"origin": (115, 5), "content": (50, 10)},
                    ],
                },
                {"origin": (0, 25), "content": (100, 100)},
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

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (640, 29),
                    "children": [
                        {"origin": (7, 7), "content": (537, 15)},
                        {"origin": (558, 7), "content": (75, 10)},
                    ],
                },
                {"origin": (0, 29), "content": (640, 451)},
            ],
        },
    )


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


def test_row_alignment_top():
    root = ExampleNode(
        "root",
        style=Pack(direction=ROW, alignment=TOP, width=300),
        children=[
            ExampleNode("space_filler", style=Pack(width=100, height=540)),
            ExampleNode(
                "container",
                style=Pack(direction=COLUMN, padding_top=110, padding_bottom=120),
                children=[
                    ExampleNode(
                        "widget_a",
                        style=Pack(height=30, padding_top=32, padding_bottom=34),
                    ),
                    ExampleNode(
                        "widget_b",
                        style=Pack(height=36, padding_top=38, padding_bottom=40),
                    ),
                ],
            ),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (300, 540),
        {
            "origin": (0, 0),
            "content": (300, 540),
            "children": [
                {"origin": (0, 0), "content": (100, 540)},
                {
                    "origin": (100, 110),
                    "content": (200, 210),
                    "children": [
                        {"origin": (100, 142), "content": (200, 30)},
                        {"origin": (100, 244), "content": (200, 36)},
                    ],
                },
            ],
        },
    )

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
        (300, 540),
        {
            "origin": (0, 0),
            "content": (300, 540),
            "children": [
                {"origin": (0, 0), "content": (100, 540)},
                {
                    "origin": (100, 110),
                    "content": (200, 210),
                    "children": [
                        {"origin": (100, 142), "content": (200, 30)},
                        {"origin": (100, 244), "content": (200, 36)},
                    ],
                },
            ],
        },
    )

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
        (450, 810),
        {
            "origin": (0, 0),
            "content": (450, 810),
            "children": [
                {"origin": (0, 0), "content": (150, 810)},
                {
                    "origin": (150, 165),
                    "content": (300, 315),
                    "children": [
                        {"origin": (150, 213), "content": (300, 45)},
                        {"origin": (150, 366), "content": (300, 54)},
                    ],
                },
            ],
        },
    )


def test_row_alignment_center():
    root = ExampleNode(
        "root",
        style=Pack(direction=ROW, alignment=CENTER, width=300),
        children=[
            ExampleNode("space_filler", style=Pack(width=100, height=540)),
            ExampleNode(
                "container",
                style=Pack(direction=COLUMN, padding_top=110, padding_bottom=120),
                children=[
                    ExampleNode(
                        "widget_a",
                        style=Pack(height=30, padding_top=32, padding_bottom=34),
                    ),
                    ExampleNode(
                        "widget_b",
                        style=Pack(height=36, padding_top=38, padding_bottom=40),
                    ),
                ],
            ),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (300, 540),
        {
            "origin": (0, 0),
            "content": (300, 540),
            "children": [
                {"origin": (0, 0), "content": (100, 540)},
                {
                    "origin": (100, 160),
                    "content": (200, 210),
                    "children": [
                        {"origin": (100, 192), "content": (200, 30)},
                        {"origin": (100, 294), "content": (200, 36)},
                    ],
                },
            ],
        },
    )

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
        (300, 540),
        {
            "origin": (0, 0),
            "content": (300, 540),
            "children": [
                {"origin": (0, 0), "content": (100, 540)},
                {
                    "origin": (100, 160),
                    "content": (200, 210),
                    "children": [
                        {"origin": (100, 192), "content": (200, 30)},
                        {"origin": (100, 294), "content": (200, 36)},
                    ],
                },
            ],
        },
    )

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
        (450, 810),
        {
            "origin": (0, 0),
            "content": (450, 810),
            "children": [
                {"origin": (0, 0), "content": (150, 810)},
                {
                    "origin": (150, 240),
                    "content": (300, 315),
                    "children": [
                        {"origin": (150, 288), "content": (300, 45)},
                        {"origin": (150, 441), "content": (300, 54)},
                    ],
                },
            ],
        },
    )


def test_row_alignment_bottom():
    root = ExampleNode(
        "root",
        style=Pack(direction=ROW, alignment=BOTTOM, width=300),
        children=[
            ExampleNode("space_filler", style=Pack(width=100, height=540)),
            ExampleNode(
                "container",
                style=Pack(direction=COLUMN, padding_top=110, padding_bottom=120),
                children=[
                    ExampleNode(
                        "widget_a",
                        style=Pack(height=30, padding_top=32, padding_bottom=34),
                    ),
                    ExampleNode(
                        "widget_b",
                        style=Pack(height=36, padding_top=38, padding_bottom=40),
                    ),
                ],
            ),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (300, 540),
        {
            "origin": (0, 0),
            "content": (300, 540),
            "children": [
                {"origin": (0, 0), "content": (100, 540)},
                {
                    "origin": (100, 210),
                    "content": (200, 210),
                    "children": [
                        {"origin": (100, 242), "content": (200, 30)},
                        {"origin": (100, 344), "content": (200, 36)},
                    ],
                },
            ],
        },
    )

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
        (300, 540),
        {
            "origin": (0, 0),
            "content": (300, 540),
            "children": [
                {"origin": (0, 0), "content": (100, 540)},
                {
                    "origin": (100, 210),
                    "content": (200, 210),
                    "children": [
                        {"origin": (100, 242), "content": (200, 30)},
                        {"origin": (100, 344), "content": (200, 36)},
                    ],
                },
            ],
        },
    )

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
        (450, 810),
        {
            "origin": (0, 0),
            "content": (450, 810),
            "children": [
                {"origin": (0, 0), "content": (150, 810)},
                {
                    "origin": (150, 315),
                    "content": (300, 315),
                    "children": [
                        {"origin": (150, 363), "content": (300, 45)},
                        {"origin": (150, 516), "content": (300, 54)},
                    ],
                },
            ],
        },
    )


def test_column_alignment_left():
    root = ExampleNode(
        "root",
        style=Pack(direction=COLUMN, alignment=LEFT, height=300),
        children=[
            ExampleNode("space_filler", style=Pack(width=540, height=100)),
            ExampleNode(
                "container",
                style=Pack(direction=ROW, padding_left=110, padding_right=120),
                children=[
                    ExampleNode(
                        "widget_a",
                        style=Pack(width=30, padding_left=32, padding_right=34),
                    ),
                    ExampleNode(
                        "widget_b",
                        style=Pack(width=36, padding_left=38, padding_right=40),
                    ),
                ],
            ),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (540, 300),
        {
            "origin": (0, 0),
            "content": (540, 300),
            "children": [
                {"origin": (0, 0), "content": (540, 100)},
                {
                    "origin": (110, 100),
                    "content": (210, 200),
                    "children": [
                        {"origin": (142, 100), "content": (30, 200)},
                        {"origin": (244, 100), "content": (36, 200)},
                    ],
                },
            ],
        },
    )

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
        (640, 300),
        {
            "origin": (0, 0),
            "content": (640, 300),
            "children": [
                {"origin": (0, 0), "content": (540, 100)},
                {
                    "origin": (110, 100),
                    "content": (210, 200),
                    "children": [
                        {"origin": (142, 100), "content": (30, 200)},
                        {"origin": (244, 100), "content": (36, 200)},
                    ],
                },
            ],
        },
    )

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
        (810, 450),
        {
            "origin": (0, 0),
            "content": (810, 450),
            "children": [
                {"origin": (0, 0), "content": (810, 150)},
                {
                    "origin": (165, 150),
                    "content": (315, 300),
                    "children": [
                        {"origin": (213, 150), "content": (45, 300)},
                        {"origin": (366, 150), "content": (54, 300)},
                    ],
                },
            ],
        },
    )


def test_column_alignment_center():
    root = ExampleNode(
        "root",
        style=Pack(direction=COLUMN, alignment=CENTER, height=300),
        children=[
            ExampleNode("space_filler", style=Pack(width=540, height=100)),
            ExampleNode(
                "container",
                style=Pack(direction=ROW, padding_left=110, padding_right=120),
                children=[
                    ExampleNode(
                        "widget_a",
                        style=Pack(width=30, padding_left=32, padding_right=34),
                    ),
                    ExampleNode(
                        "widget_b",
                        style=Pack(width=36, padding_left=38, padding_right=40),
                    ),
                ],
            ),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (540, 300),
        {
            "origin": (0, 0),
            "content": (540, 300),
            "children": [
                {"origin": (0, 0), "content": (540, 100)},
                {
                    "origin": (160, 100),
                    "content": (210, 200),
                    "children": [
                        {"origin": (192, 100), "content": (30, 200)},
                        {"origin": (294, 100), "content": (36, 200)},
                    ],
                },
            ],
        },
    )

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
        (640, 300),
        {
            "origin": (0, 0),
            "content": (640, 300),
            "children": [
                {"origin": (0, 0), "content": (540, 100)},
                {
                    "origin": (160, 100),
                    "content": (210, 200),
                    "children": [
                        {"origin": (192, 100), "content": (30, 200)},
                        {"origin": (294, 100), "content": (36, 200)},
                    ],
                },
            ],
        },
    )

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
        (810, 450),
        {
            "origin": (0, 0),
            "content": (810, 450),
            "children": [
                {"origin": (0, 0), "content": (810, 150)},
                {
                    "origin": (240, 150),
                    "content": (315, 300),
                    "children": [
                        {"origin": (288, 150), "content": (45, 300)},
                        {"origin": (441, 150), "content": (54, 300)},
                    ],
                },
            ],
        },
    )


def test_column_alignment_right():
    root = ExampleNode(
        "root",
        style=Pack(direction=COLUMN, alignment=RIGHT, height=300),
        children=[
            ExampleNode("space_filler", style=Pack(width=540, height=100)),
            ExampleNode(
                "container",
                style=Pack(direction=ROW, padding_left=110, padding_right=120),
                children=[
                    ExampleNode(
                        "widget_a",
                        style=Pack(width=30, padding_left=32, padding_right=34),
                    ),
                    ExampleNode(
                        "widget_b",
                        style=Pack(width=36, padding_left=38, padding_right=40),
                    ),
                ],
            ),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (540, 300),
        {
            "origin": (0, 0),
            "content": (540, 300),
            "children": [
                {"origin": (0, 0), "content": (540, 100)},
                {
                    "origin": (210, 100),
                    "content": (210, 200),
                    "children": [
                        {"origin": (242, 100), "content": (30, 200)},
                        {"origin": (344, 100), "content": (36, 200)},
                    ],
                },
            ],
        },
    )

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
        (640, 300),
        {
            "origin": (0, 0),
            "content": (640, 300),
            "children": [
                {"origin": (0, 0), "content": (540, 100)},
                {
                    "origin": (210, 100),
                    "content": (210, 200),
                    "children": [
                        {"origin": (242, 100), "content": (30, 200)},
                        {"origin": (344, 100), "content": (36, 200)},
                    ],
                },
            ],
        },
    )

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
        (810, 450),
        {
            "origin": (0, 0),
            "content": (810, 450),
            "children": [
                {"origin": (0, 0), "content": (810, 150)},
                {
                    "origin": (315, 150),
                    "content": (315, 300),
                    "children": [
                        {"origin": (363, 150), "content": (45, 300)},
                        {"origin": (516, 150), "content": (54, 300)},
                    ],
                },
            ],
        },
    )


def test_row_alignment_no_padding():
    root = ExampleNode(
        "root",
        style=Pack(direction=ROW, alignment=CENTER, width=300),
        children=[
            ExampleNode("space_filler", style=Pack(width=100, height=540)),
            ExampleNode("widget", style=Pack(height=440)),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (300, 540),
        {
            "origin": (0, 0),
            "content": (300, 540),
            "children": [
                {"origin": (0, 0), "content": (100, 540)},
                {"origin": (100, 50), "content": (200, 440)},
            ],
        },
    )

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
        (300, 540),
        {
            "origin": (0, 0),
            "content": (300, 540),
            "children": [
                {"origin": (0, 0), "content": (100, 540)},
                {"origin": (100, 50), "content": (200, 440)},
            ],
        },
    )

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
        (450, 810),
        {
            "origin": (0, 0),
            "content": (450, 810),
            "children": [
                {"origin": (0, 0), "content": (150, 810)},
                {"origin": (150, 75), "content": (300, 660)},
            ],
        },
    )


def test_column_alignment_no_padding():
    root = ExampleNode(
        "root",
        style=Pack(direction=COLUMN, alignment=CENTER, height=300),
        children=[
            ExampleNode("space_filler", style=Pack(width=540, height=100)),
            ExampleNode("widget", style=Pack(width=440)),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (540, 300),
        {
            "origin": (0, 0),
            "content": (540, 300),
            "children": [
                {"origin": (0, 0), "content": (540, 100)},
                {"origin": (50, 100), "content": (440, 200)},
            ],
        },
    )

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
        (640, 300),
        {
            "origin": (0, 0),
            "content": (640, 300),
            "children": [
                {"origin": (0, 0), "content": (540, 100)},
                {"origin": (50, 100), "content": (440, 200)},
            ],
        },
    )

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
        (810, 450),
        {
            "origin": (0, 0),
            "content": (810, 450),
            "children": [
                {"origin": (0, 0), "content": (810, 150)},
                {"origin": (75, 150), "content": (660, 300)},
            ],
        },
    )


def test_row_alignment_row_box():
    root = ExampleNode(
        "root",
        style=Pack(direction=ROW, alignment=CENTER),
        children=[
            ExampleNode("space_filler", style=Pack(width=100, height=430)),
            ExampleNode(
                "container",
                style=Pack(direction=ROW, padding_top=110, padding_bottom=120),
                children=[
                    ExampleNode(
                        "widget_a",
                        style=Pack(
                            width=30, height=100, padding_left=32, padding_right=34
                        ),
                    ),
                    ExampleNode(
                        "widget_b",
                        style=Pack(
                            width=36, height=100, padding_left=38, padding_right=40
                        ),
                    ),
                ],
            ),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (310, 430),
        {
            "origin": (0, 0),
            "content": (310, 430),
            "children": [
                {"origin": (0, 0), "content": (100, 430)},
                {
                    "origin": (100, 160),
                    "content": (210, 100),
                    "children": [
                        {"origin": (132, 160), "content": (30, 100)},
                        {"origin": (234, 160), "content": (36, 100)},
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
                {"origin": (0, 0), "content": (100, 430)},
                {
                    "origin": (100, 160),
                    "content": (210, 100),
                    "children": [
                        {"origin": (132, 160), "content": (30, 100)},
                        {"origin": (234, 160), "content": (36, 100)},
                    ],
                },
            ],
        },
    )

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
        (640, 645),
        {
            "origin": (0, 0),
            "content": (640, 645),
            "children": [
                {"origin": (0, 0), "content": (150, 645)},
                {
                    "origin": (150, 240),
                    "content": (315, 150),
                    "children": [
                        {"origin": (198, 240), "content": (45, 150)},
                        {"origin": (351, 240), "content": (54, 150)},
                    ],
                },
            ],
        },
    )


def test_column_alignment_column_box():
    root = ExampleNode(
        "root",
        style=Pack(direction=COLUMN, alignment=CENTER),
        children=[
            ExampleNode("space_filler", style=Pack(width=430, height=100)),
            ExampleNode(
                "container",
                style=Pack(direction=COLUMN, padding_left=110, padding_right=120),
                children=[
                    ExampleNode(
                        "widget_a",
                        style=Pack(
                            width=100, height=30, padding_top=32, padding_bottom=34
                        ),
                    ),
                    ExampleNode(
                        "widget_b",
                        style=Pack(
                            width=100, height=36, padding_top=38, padding_bottom=40
                        ),
                    ),
                ],
            ),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (430, 310),
        {
            "origin": (0, 0),
            "content": (430, 310),
            "children": [
                {"origin": (0, 0), "content": (430, 100)},
                {
                    "origin": (160, 100),
                    "content": (100, 210),
                    "children": [
                        {"origin": (160, 132), "content": (100, 30)},
                        {"origin": (160, 234), "content": (100, 36)},
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
                {"origin": (0, 0), "content": (430, 100)},
                {
                    "origin": (160, 100),
                    "content": (100, 210),
                    "children": [
                        {"origin": (160, 132), "content": (100, 30)},
                        {"origin": (160, 234), "content": (100, 36)},
                    ],
                },
            ],
        },
    )

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
        (645, 480),
        {
            "origin": (0, 0),
            "content": (645, 480),
            "children": [
                {"origin": (0, 0), "content": (645, 150)},
                {
                    "origin": (240, 150),
                    "content": (150, 315),
                    "children": [
                        {"origin": (240, 198), "content": (150, 45)},
                        {"origin": (240, 351), "content": (150, 54)},
                    ],
                },
            ],
        },
    )


def test_rtl_row_box_child_layout():
    root = ExampleNode(
        "container",
        style=Pack(text_direction=RTL, direction=ROW),
        children=[
            ExampleNode(
                "widget_a",
                style=Pack(width=30, height=100, padding_left=32, padding_right=34),
            ),
            ExampleNode(
                "widget_b",
                style=Pack(width=36, height=100, padding_left=38, padding_right=40),
            ),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (210, 100),
        {
            "origin": (0, 0),
            "content": (210, 100),
            "children": [
                {"origin": (146, 0), "content": (30, 100)},
                {"origin": (38, 0), "content": (36, 100)},
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
                {"origin": (146, 0), "content": (30, 100)},
                {"origin": (38, 0), "content": (36, 100)},
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
                {"origin": (219, 0), "content": (45, 150)},
                {"origin": (57, 0), "content": (54, 150)},
            ],
        },
    )


def test_rtl_column_box_child_layout():
    root = ExampleNode(
        "container",
        style=Pack(text_direction=RTL, direction=COLUMN),
        children=[
            ExampleNode(
                "widget_a",
                style=Pack(width=100, height=30, padding_top=32, padding_bottom=34),
            ),
            ExampleNode(
                "widget_b",
                style=Pack(width=100, height=36, padding_top=38, padding_bottom=40),
            ),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (100, 210),
        {
            "origin": (0, 0),
            "content": (100, 210),
            "children": [
                {"origin": (0, 32), "content": (100, 30)},
                {"origin": (0, 134), "content": (100, 36)},
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
                {"origin": (0, 32), "content": (100, 30)},
                {"origin": (0, 134), "content": (100, 36)},
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
                {"origin": (0, 48), "content": (150, 45)},
                {"origin": (0, 201), "content": (150, 54)},
            ],
        },
    )


def test_rtl_alignment_top():
    root = ExampleNode(
        "root",
        style=Pack(text_direction=RTL, direction=ROW, alignment=TOP),
        children=[
            ExampleNode("space_filler", style=Pack(width=30, height=100)),
            ExampleNode("widget", style=Pack(width=30, height=30)),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (60, 100),
        {
            "origin": (0, 0),
            "content": (60, 100),
            "children": [
                {"origin": (30, 0), "content": (30, 100)},
                {"origin": (0, 0), "content": (30, 30)},
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
                {"origin": (30, 0), "content": (30, 100)},
                {"origin": (0, 0), "content": (30, 30)},
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
                {"origin": (45, 0), "content": (45, 150)},
                {"origin": (0, 0), "content": (45, 45)},
            ],
        },
    )


def test_rtl_alignment_bottom():
    root = ExampleNode(
        "root",
        style=Pack(text_direction=RTL, direction=ROW, alignment=BOTTOM),
        children=[
            ExampleNode("space_filler", style=Pack(width=30, height=100)),
            ExampleNode("widget", style=Pack(width=30, height=30)),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (60, 100),
        {
            "origin": (0, 0),
            "content": (60, 100),
            "children": [
                {"origin": (30, 0), "content": (30, 100)},
                {"origin": (0, 70), "content": (30, 30)},
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
                {"origin": (30, 0), "content": (30, 100)},
                {"origin": (0, 70), "content": (30, 30)},
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
                {"origin": (45, 0), "content": (45, 150)},
                {"origin": (0, 105), "content": (45, 45)},
            ],
        },
    )


def test_rtl_alignment_left():
    root = ExampleNode(
        "root",
        style=Pack(text_direction=RTL, direction=COLUMN, alignment=LEFT),
        children=[
            ExampleNode("space_filler", style=Pack(width=100, height=30)),
            ExampleNode("widget", style=Pack(width=30, height=30)),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (100, 60),
        {
            "origin": (0, 0),
            "content": (100, 60),
            "children": [
                {"origin": (0, 0), "content": (100, 30)},
                {"origin": (0, 30), "content": (30, 30)},
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
                {"origin": (0, 0), "content": (100, 30)},
                {"origin": (0, 30), "content": (30, 30)},
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
                {"origin": (0, 0), "content": (150, 45)},
                {"origin": (0, 45), "content": (45, 45)},
            ],
        },
    )


def test_rtl_alignment_right():
    root = ExampleNode(
        "root",
        style=Pack(text_direction=RTL, direction=COLUMN, alignment=RIGHT),
        children=[
            ExampleNode("space_filler", style=Pack(width=100, height=30)),
            ExampleNode("widget", style=Pack(width=30, height=30)),
        ],
    )

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (100, 60),
        {
            "origin": (0, 0),
            "content": (100, 60),
            "children": [
                {"origin": (0, 0), "content": (100, 30)},
                {"origin": (70, 30), "content": (30, 30)},
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
                {"origin": (0, 0), "content": (100, 30)},
                {"origin": (70, 30), "content": (30, 30)},
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
                {"origin": (0, 0), "content": (150, 45)},
                {"origin": (105, 45), "content": (45, 45)},
            ],
        },
    )


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
