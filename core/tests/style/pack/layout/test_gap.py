from travertino.size import at_least

from toga.style.pack import Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


class Box(ExampleNode):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("size", (at_least(0), at_least(0)))
        super().__init__(*args, **kwargs)


def test_gap():
    viewport = ExampleViewport(640, 480)
    root = Box(
        "app",
        style=Pack(direction="row"),
        children=[
            Box("fixed", style=Pack(width=100, height=100)),
            Box("flex-1", style=Pack(flex=1, margin=15)),
            Box("flex-3", style=Pack(flex=3)),
        ],
    )

    # No gap
    root.style.layout(viewport)
    assert_layout(
        root,
        (130, 100),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": (0, 0), "content": (100, 100)},
                {"origin": (115, 15), "content": (105, 450)},
                {"origin": (235, 0), "content": (405, 480)},
            ],
        },
    )

    # Add a gap, then test it in all 3 configurations.
    root.style.update(gap=20)

    # Row, LTR
    root.style.update(direction="row", text_direction="ltr")
    root.style.layout(viewport)
    assert_layout(
        root,
        (170, 100),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": (0, 0), "content": (100, 100)},
                {"origin": (135, 15), "content": (95, 450)},
                {"origin": (265, 0), "content": (375, 480)},
            ],
        },
    )

    # Row, RTL
    root.style.update(direction="row", text_direction="rtl")
    root.style.layout(viewport)
    assert_layout(
        root,
        (170, 100),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": (540, 0), "content": (100, 100)},
                {"origin": (410, 15), "content": (95, 450)},
                {"origin": (0, 0), "content": (375, 480)},
            ],
        },
    )

    # Column
    root.style.update(direction="column")
    root.style.layout(viewport)
    assert_layout(
        root,
        (100, 170),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": (0, 0), "content": (100, 100)},
                {"origin": (15, 135), "content": (610, 55)},
                {"origin": (0, 225), "content": (640, 255)},
            ],
        },
    )
