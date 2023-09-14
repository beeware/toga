from toga.style.pack import CENTER, COLUMN, LEFT, RIGHT, ROW, Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


def test_left():
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

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (540, 300),
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


def test_center():
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

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (540, 300),
        (640, 300),
        {
            "origin": (0, 0),
            "content": (640, 300),
            "children": [
                {"origin": (50, 0), "content": (540, 100)},
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


def test_right():
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

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (540, 300),
        (640, 300),
        {
            "origin": (0, 0),
            "content": (640, 300),
            "children": [
                {"origin": (100, 0), "content": (540, 100)},
                {
                    "origin": (310, 100),
                    "content": (210, 200),
                    "children": [
                        {"origin": (342, 100), "content": (30, 200)},
                        {"origin": (444, 100), "content": (36, 200)},
                    ],
                },
            ],
        },
    )


def test_no_padding():
    root = ExampleNode(
        "root",
        style=Pack(direction=COLUMN, alignment=CENTER, height=300),
        children=[
            ExampleNode("space_filler", style=Pack(width=540, height=100)),
            ExampleNode("widget", style=Pack(width=440)),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (540, 300),
        (640, 300),
        {
            "origin": (0, 0),
            "content": (640, 300),
            "children": [
                {"origin": (50, 0), "content": (540, 100)},
                {"origin": (100, 100), "content": (440, 200)},
            ],
        },
    )


def test_column_box():
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

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (430, 310),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": (105, 0), "content": (430, 100)},
                {
                    "origin": (110, 100),
                    "content": (410, 210),
                    "children": [
                        {"origin": (110, 132), "content": (100, 30)},
                        {"origin": (110, 234), "content": (100, 36)},
                    ],
                },
            ],
        },
    )
