import pytest
from travertino.size import at_least

from toga.style.pack import Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


class Box(ExampleNode):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("size", (at_least(0), at_least(0)))
        super().__init__(*args, **kwargs)


@pytest.fixture
def viewport():
    return ExampleViewport(640, 480)


@pytest.fixture
def root():
    return Box(
        "parent",
        style=Pack(gap=20),
        children=[
            Box("child_0", style=Pack(width=100, height=100, margin=10)),
            Box("child_1", style=Pack(width=100, height=100)),
        ],
    )


@pytest.mark.parametrize(
    "direction, text_direction, justify_content, origin_0, origin_1",
    [
        ("row", "ltr", "start", (10, 10), (140, 0)),
        ("row", "ltr", "center", (210, 10), (340, 0)),
        ("row", "ltr", "end", (410, 10), (540, 0)),
        #
        ("row", "rtl", "start", (530, 10), (400, 0)),
        ("row", "rtl", "center", (330, 10), (200, 0)),
        ("row", "rtl", "end", (130, 10), (0, 0)),
        #
        ("column", None, "start", (10, 10), (0, 140)),
        ("column", None, "center", (10, 130), (0, 260)),
        ("column", None, "end", (10, 250), (0, 380)),
    ],
)
def test_justify_content(
    viewport, root, direction, text_direction, justify_content, origin_0, origin_1
):
    root.style.update(direction=direction, justify_content=justify_content)
    if text_direction:
        root.style.text_direction = text_direction

    root.style.layout(viewport)
    assert_layout(
        root,
        (240, 120) if direction == "row" else (120, 240),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": origin_0, "content": (100, 100)},
                {"origin": origin_1, "content": (100, 100)},
            ],
        },
    )


@pytest.mark.parametrize(
    "direction, text_direction, origin_0, origin_1, content_1",
    [
        ("row", "ltr", (10, 10), (140, 0), (500, 100)),
        ("row", "rtl", (530, 10), (0, 0), (500, 100)),
        ("column", None, (10, 10), (0, 140), (100, 340)),
    ],
)
@pytest.mark.parametrize("justify_content", ["start", "center", "end"])
def test_justify_content_flex(
    viewport,
    root,
    direction,
    text_direction,
    justify_content,
    origin_0,
    origin_1,
    content_1,
):
    """justify_content has no effect when a child is flexible."""
    root.style.update(direction=direction, justify_content=justify_content)
    if text_direction:
        root.style.text_direction = text_direction

    child_style = root.children[1].style
    delattr(child_style, "width" if direction == "row" else "height")
    child_style.flex = 1

    root.style.layout(viewport)
    assert_layout(
        root,
        (140, 120) if direction == "row" else (120, 140),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": origin_0, "content": (100, 100)},
                {"origin": origin_1, "content": content_1},
            ],
        },
    )
