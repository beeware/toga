import pytest

from travertino.declaration import BaseStyle
from travertino.layout import BaseBox, Viewport
from travertino.node import Node
from travertino.size import BaseIntrinsicSize


class Style(BaseStyle):
    class IntrinsicSize(BaseIntrinsicSize):
        pass

    class Box(BaseBox):
        pass


def test_viewport_default():
    viewport = Viewport()

    assert viewport.width == 0
    assert viewport.height == 0
    assert viewport.dpi is None


def test_viewport_constructor():
    viewport = Viewport(width=640, height=480, dpi=96)

    assert viewport.width == 640
    assert viewport.height == 480
    assert viewport.dpi == 96


class TestBox:
    pass


@pytest.fixture
def box():
    box = TestBox()

    box.maxDiff = None

    box.grandchild1_1 = Node(style=Style())
    box.grandchild1_1.layout.min_content_width = 5
    box.grandchild1_1.layout.content_width = 10
    box.grandchild1_1.layout.min_content_height = 8
    box.grandchild1_1.layout.content_height = 16

    box.grandchild1_2 = Node(style=Style())

    box.child1 = Node(style=Style(), children=[box.grandchild1_1, box.grandchild1_2])
    box.child1.layout.min_content_width = 5
    box.child1.layout.content_width = 10
    box.child1.layout.min_content_height = 8
    box.child1.layout.content_height = 16
    box.child2 = Node(style=Style(), children=[])

    box.node = Node(style=Style(), children=[box.child1, box.child2])
    box.node.layout.min_content_width = 5
    box.node.layout.content_width = 10
    box.node.layout.min_content_height = 8
    box.node.layout.content_height = 16

    return box


def assert_layout(box, expected):
    actual = {
        "origin": (box._origin_left, box._origin_top),
        "min_size": (box.min_width, box.min_height),
        "size": (box.width, box.height),
        "content": (box.content_width, box.content_height),
        "relative": (
            box.content_top,
            box.content_right,
            box.content_bottom,
            box.content_left,
        ),
        "absolute": (
            box.absolute_content_top,
            box.absolute_content_right,
            box.absolute_content_bottom,
            box.absolute_content_left,
        ),
    }
    assert actual == expected


def test_repr(box):
    box.node.layout._origin_top = 1
    box.node.layout._origin_left = 2
    assert repr(box.node.layout) == "<Box (10x16 @ 2,1)>"


def test_initial(box):
    # Core attributes have been stored
    assert_layout(
        box.node.layout,
        {
            "origin": (0, 0),
            "min_size": (5, 8),
            "size": (10, 16),
            "content": (10, 16),
            "relative": (0, 0, 0, 0),
            "absolute": (0, 10, 16, 0),
        },
    )


@pytest.mark.parametrize(
    "dimension, val1, expected1, val2, expected2",
    [
        (
            "content_top",
            5,
            {
                "origin": (0, 0),
                "min_size": (5, 13),
                "size": (10, 21),
                "content": (10, 16),
                "relative": (5, 0, 0, 0),
                "absolute": (5, 10, 21, 0),
            },
            7,
            {
                "origin": (0, 0),
                "min_size": (5, 15),
                "size": (10, 23),
                "content": (10, 16),
                "relative": (7, 0, 0, 0),
                "absolute": (7, 10, 23, 0),
            },
        ),
        (
            "content_left",
            5,
            {
                "origin": (0, 0),
                "min_size": (10, 8),
                "size": (15, 16),
                "content": (10, 16),
                "relative": (0, 0, 0, 5),
                "absolute": (0, 15, 16, 5),
            },
            7,
            {
                "origin": (0, 0),
                "min_size": (12, 8),
                "size": (17, 16),
                "content": (10, 16),
                "relative": (0, 0, 0, 7),
                "absolute": (0, 17, 16, 7),
            },
        ),
        (
            "min_content_width",
            8,
            {
                "origin": (0, 0),
                "min_size": (8, 8),
                "size": (10, 16),
                "content": (10, 16),
                "relative": (0, 0, 0, 0),
                "absolute": (0, 10, 16, 0),
            },
            9,
            {
                "origin": (0, 0),
                "min_size": (9, 8),
                "size": (10, 16),
                "content": (10, 16),
                "relative": (0, 0, 0, 0),
                "absolute": (0, 10, 16, 0),
            },
        ),
        (
            "content_width",
            5,
            {
                "origin": (0, 0),
                "min_size": (5, 8),
                "size": (5, 16),
                "content": (5, 16),
                "relative": (0, 0, 0, 0),
                "absolute": (0, 5, 16, 0),
            },
            7,
            {
                "origin": (0, 0),
                "min_size": (5, 8),
                "size": (7, 16),
                "content": (7, 16),
                "relative": (0, 0, 0, 0),
                "absolute": (0, 7, 16, 0),
            },
        ),
        (
            "min_content_height",
            7,
            {
                "origin": (0, 0),
                "min_size": (5, 7),
                "size": (10, 16),
                "content": (10, 16),
                "relative": (0, 0, 0, 0),
                "absolute": (0, 10, 16, 0),
            },
            8,
            {
                "origin": (0, 0),
                "min_size": (5, 8),
                "size": (10, 16),
                "content": (10, 16),
                "relative": (0, 0, 0, 0),
                "absolute": (0, 10, 16, 0),
            },
        ),
        (
            "content_height",
            10,
            {
                "origin": (0, 0),
                "min_size": (5, 8),
                "size": (10, 10),
                "content": (10, 10),
                "relative": (0, 0, 0, 0),
                "absolute": (0, 10, 10, 0),
            },
            12,
            {
                "origin": (0, 0),
                "min_size": (5, 8),
                "size": (10, 12),
                "content": (10, 12),
                "relative": (0, 0, 0, 0),
                "absolute": (0, 10, 12, 0),
            },
        ),
    ],
)
def test_set_content_dimension(box, dimension, val1, expected1, val2, expected2):
    setattr(box.node.layout, dimension, val1)
    assert_layout(box.node.layout, expected1)

    # Set to a new value
    setattr(box.node.layout, dimension, val2)
    assert_layout(box.node.layout, expected2)


def test_descendent_offsets(box):
    box.node.layout.content_top = 7
    box.node.layout.content_left = 8

    box.child1.layout.content_top = 9
    box.child1.layout.content_left = 10

    box.grandchild1_1.layout.content_top = 11
    box.grandchild1_1.layout.content_left = 12

    assert_layout(
        box.node.layout,
        {
            "origin": (0, 0),
            "min_size": (13, 15),
            "size": (18, 23),
            "content": (10, 16),
            "relative": (7, 0, 0, 8),
            "absolute": (7, 18, 23, 8),
        },
    )

    assert_layout(
        box.child1.layout,
        {
            "origin": (8, 7),
            "min_size": (15, 17),
            "size": (20, 25),
            "content": (10, 16),
            "relative": (9, 0, 0, 10),
            "absolute": (16, 28, 32, 18),
        },
    )

    assert_layout(
        box.grandchild1_1.layout,
        {
            "origin": (18, 16),
            "min_size": (17, 19),
            "size": (22, 27),
            "content": (10, 16),
            "relative": (11, 0, 0, 12),
            "absolute": (27, 40, 43, 30),
        },
    )

    # Modify the grandchild position
    box.grandchild1_1.layout.content_top = 13
    box.grandchild1_1.layout.content_left = 14

    # Only the grandchild position has changed.
    assert_layout(
        box.node.layout,
        {
            "origin": (0, 0),
            "min_size": (13, 15),
            "size": (18, 23),
            "content": (10, 16),
            "relative": (7, 0, 0, 8),
            "absolute": (7, 18, 23, 8),
        },
    )

    assert_layout(
        box.child1.layout,
        {
            "origin": (8, 7),
            "min_size": (15, 17),
            "size": (20, 25),
            "content": (10, 16),
            "relative": (9, 0, 0, 10),
            "absolute": (16, 28, 32, 18),
        },
    )

    assert_layout(
        box.grandchild1_1.layout,
        {
            "origin": (18, 16),
            "min_size": (19, 21),
            "size": (24, 29),
            "content": (10, 16),
            "relative": (13, 0, 0, 14),
            "absolute": (29, 42, 45, 32),
        },
    )

    # Modify the child position
    box.child1.layout.content_top = 15
    box.child1.layout.content_left = 16

    # The child and grandchild positions have changed.
    assert_layout(
        box.node.layout,
        {
            "origin": (0, 0),
            "min_size": (13, 15),
            "size": (18, 23),
            "content": (10, 16),
            "relative": (7, 0, 0, 8),
            "absolute": (7, 18, 23, 8),
        },
    )

    assert_layout(
        box.child1.layout,
        {
            "origin": (8, 7),
            "min_size": (21, 23),
            "size": (26, 31),
            "content": (10, 16),
            "relative": (15, 0, 0, 16),
            "absolute": (22, 34, 38, 24),
        },
    )

    assert_layout(
        box.grandchild1_1.layout,
        {
            "origin": (24, 22),
            "min_size": (19, 21),
            "size": (24, 29),
            "content": (10, 16),
            "relative": (13, 0, 0, 14),
            "absolute": (35, 48, 51, 38),
        },
    )


def test_absolute_equalities(box):
    # Move the box around and set some borders.
    layout = box.node.layout

    layout.origin_top = 100
    layout.origin_left = 200

    layout.content_top = 50
    layout.content_left = 75
    layout.content_right = 42
    layout.content_bottom = 37

    assert (
        layout.absolute_content_left + layout.content_width
        == layout.absolute_content_right
    )
    assert (
        layout.absolute_content_top + layout.content_height
        == layout.absolute_content_bottom
    )

    assert (
        layout.content_left + layout.content_width + layout.content_right
        == layout.width
    )
    assert (
        layout.content_top + layout.content_height + layout.content_bottom
        == layout.height
    )
