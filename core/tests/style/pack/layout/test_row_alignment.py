from toga.style.pack import BOTTOM, CENTER, COLUMN, ROW, TOP, Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


def test_top():
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


def test_center():
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


def test_bottom():
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


def test_no_padding():
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


def test_row_box():
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
                {"origin": (0, 25), "content": (100, 430)},
                {
                    "origin": (100, 110),
                    "content": (210, 250),
                    "children": [
                        {"origin": (132, 110), "content": (30, 100)},
                        {"origin": (234, 110), "content": (36, 100)},
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
