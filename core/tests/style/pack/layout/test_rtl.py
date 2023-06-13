from toga.style.pack import BOTTOM, COLUMN, LEFT, RIGHT, ROW, RTL, TOP, Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


def test_row_box_child_layout():
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
                {"origin": (576, 0), "content": (30, 100)},
                {"origin": (468, 0), "content": (36, 100)},
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
                {"origin": (544, 0), "content": (45, 150)},
                {"origin": (382, 0), "content": (54, 150)},
            ],
        },
    )


def test_column_box_child_layout():
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


def test_alignment_top():
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
                {"origin": (610, 0), "content": (30, 100)},
                {"origin": (580, 0), "content": (30, 30)},
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
                {"origin": (595, 0), "content": (45, 150)},
                {"origin": (550, 0), "content": (45, 45)},
            ],
        },
    )


def test_alignment_bottom():
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
                {"origin": (610, 380), "content": (30, 100)},
                {"origin": (580, 450), "content": (30, 30)},
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
                {"origin": (595, 330), "content": (45, 150)},
                {"origin": (550, 435), "content": (45, 45)},
            ],
        },
    )


def test_alignment_left():
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


def test_alignment_right():
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
                {"origin": (540, 0), "content": (100, 30)},
                {"origin": (610, 30), "content": (30, 30)},
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
                {"origin": (490, 0), "content": (150, 45)},
                {"origin": (595, 45), "content": (45, 45)},
            ],
        },
    )
