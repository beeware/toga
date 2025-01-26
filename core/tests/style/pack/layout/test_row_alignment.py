from toga.style.pack import CENTER, COLUMN, END, ROW, START, Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


def test_top():
    root = ExampleNode(
        "root",
        style=Pack(direction=ROW, align_items=START, width=300),
        children=[
            ExampleNode("space_filler", style=Pack(width=100, height=540)),
            ExampleNode(
                "container",
                style=Pack(direction=COLUMN, margin_top=110, margin_bottom=120),
                children=[
                    ExampleNode(
                        "widget_a",
                        style=Pack(height=30, margin_top=32, margin_bottom=34),
                    ),
                    ExampleNode(
                        "widget_b",
                        style=Pack(height=36, margin_top=38, margin_bottom=40),
                    ),
                ],
            ),
        ],
    )

    root.style.layout(ExampleViewport(640, 480))
    assert_layout(
        root,
        (300, 540),
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


def test_center():
    root = ExampleNode(
        "root",
        style=Pack(direction=ROW, align_items=CENTER, width=300),
        children=[
            ExampleNode("space_filler", style=Pack(width=100, height=540)),
            ExampleNode(
                "container",
                style=Pack(direction=COLUMN, margin_top=110, margin_bottom=120),
                children=[
                    ExampleNode(
                        "widget_a",
                        style=Pack(height=30, margin_top=32, margin_bottom=34),
                    ),
                    ExampleNode(
                        "widget_b",
                        style=Pack(height=36, margin_top=38, margin_bottom=40),
                    ),
                ],
            ),
        ],
    )

    root.style.layout(ExampleViewport(640, 480))
    assert_layout(
        root,
        (300, 540),
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


def test_bottom():
    root = ExampleNode(
        "root",
        style=Pack(direction=ROW, align_items=END, width=300),
        children=[
            ExampleNode("space_filler", style=Pack(width=100, height=540)),
            ExampleNode(
                "container",
                style=Pack(direction=COLUMN, margin_top=110, margin_bottom=120),
                children=[
                    ExampleNode(
                        "widget_a",
                        style=Pack(height=30, margin_top=32, margin_bottom=34),
                    ),
                    ExampleNode(
                        "widget_b",
                        style=Pack(height=36, margin_top=38, margin_bottom=40),
                    ),
                ],
            ),
        ],
    )

    root.style.layout(ExampleViewport(640, 480))
    assert_layout(
        root,
        (300, 540),
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


def test_no_margin():
    root = ExampleNode(
        "root",
        style=Pack(direction=ROW, align_items=CENTER, width=300),
        children=[
            ExampleNode("space_filler", style=Pack(width=100, height=540)),
            ExampleNode("widget", style=Pack(height=440)),
        ],
    )

    root.style.layout(ExampleViewport(640, 480))
    assert_layout(
        root,
        (300, 540),
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


def test_row_box():
    root = ExampleNode(
        "root",
        style=Pack(direction=ROW, align_items=CENTER),
        children=[
            ExampleNode("space_filler", style=Pack(width=100, height=430)),
            ExampleNode(
                "container",
                style=Pack(direction=ROW, margin_top=110, margin_bottom=120),
                children=[
                    ExampleNode(
                        "widget_a",
                        style=Pack(
                            width=30, height=100, margin_left=32, margin_right=34
                        ),
                    ),
                    ExampleNode(
                        "widget_b",
                        style=Pack(
                            width=36, height=100, margin_left=38, margin_right=40
                        ),
                    ),
                ],
            ),
        ],
    )

    root.style.layout(ExampleViewport(640, 480))
    assert_layout(
        root,
        (310, 430),
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
