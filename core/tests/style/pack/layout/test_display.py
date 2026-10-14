from toga.style.pack import COLUMN, NONE, PACK, ROW, Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


def test_display_none_row():
    """A child that isn't displayed takes no space, and doesn't add a gap."""
    root = ExampleNode(
        "app",
        style=Pack(direction=ROW, gap=10),
        children=[
            ExampleNode("first", style=Pack(width=100, height=100)),
            ExampleNode(
                "none", style=Pack(width=100, height=100, margin=20, display=NONE)
            ),
            ExampleNode("last", style=Pack(width=100, height=100)),
        ],
    )

    root.style.layout(ExampleViewport(640, 480))
    assert_layout(
        root,
        (210, 100),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": (0, 0), "content": (100, 100)},
                {"origin": (0, 0), "content": (0, 0)},
                {"origin": (110, 0), "content": (100, 100)},
            ],
        },
    )


def test_display_none_flex():
    """A flexible child that isn't displayed doesn't consume any flexible space."""
    root = ExampleNode(
        "app",
        style=Pack(direction=ROW),
        children=[
            ExampleNode("flex", style=Pack(flex=1)),
            ExampleNode("none", style=Pack(flex=1, display=NONE)),
        ],
    )

    root.style.layout(ExampleViewport(640, 480))
    assert_layout(
        root,
        (0, 0),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": (0, 0), "content": (640, 480)},
                {"origin": (0, 0), "content": (0, 0)},
            ],
        },
    )


def test_display_toggle():
    """A node and its descendants can be removed from, and restored to, the layout."""
    inner = ExampleNode("inner", style=Pack(width=50, height=50))
    middle = ExampleNode(
        "middle", style=Pack(direction=ROW, height=100), children=[inner]
    )
    root = ExampleNode(
        "app",
        style=Pack(direction=COLUMN),
        children=[
            ExampleNode("top", style=Pack(width=100, height=100)),
            middle,
            ExampleNode("bottom", style=Pack(width=100, height=100)),
        ],
    )
    viewport = ExampleViewport(640, 480)

    displayed_layout = {
        "origin": (0, 0),
        "content": (640, 480),
        "children": [
            {"origin": (0, 0), "content": (100, 100)},
            {
                "origin": (0, 100),
                "content": (50, 100),
                "children": [{"origin": (0, 100), "content": (50, 50)}],
            },
            {"origin": (0, 200), "content": (100, 100)},
        ],
    }

    root.style.layout(viewport)
    assert_layout(root, (100, 300), (640, 480), displayed_layout)

    # Remove the middle node from the layout. It and its child collapse to nothing,
    # and the bottom node moves up to take its place.
    middle.style.display = NONE
    root.style.layout(viewport)
    assert_layout(
        root,
        (100, 200),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": (0, 0), "content": (100, 100)},
                {
                    "origin": (0, 0),
                    "content": (0, 0),
                    "children": [{"origin": (0, 0), "content": (0, 0)}],
                },
                {"origin": (0, 100), "content": (100, 100)},
            ],
        },
    )

    # Restore the middle node; the original layout is restored.
    middle.style.display = PACK
    root.style.layout(viewport)
    assert_layout(root, (100, 300), (640, 480), displayed_layout)


def test_all_children_display_none():
    """A node whose children are all undisplayed is laid out as if it had none."""
    root = ExampleNode(
        "app",
        style=Pack(direction=ROW),
        children=[
            ExampleNode("sibling", style=Pack(width=100)),
            ExampleNode(
                "box",
                style=Pack(direction=COLUMN),
                children=[
                    ExampleNode(
                        "none", style=Pack(width=100, height=100, display=NONE)
                    ),
                ],
            ),
        ],
    )

    root.style.layout(ExampleViewport(640, 480))
    # Like an empty box, the box consumes all the remaining space, rather than being
    # sized to fit the child that isn't displayed.
    assert_layout(
        root,
        (100, 0),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": (0, 0), "content": (100, 480)},
                {
                    "origin": (100, 0),
                    "content": (540, 480),
                    "children": [{"origin": (100, 0), "content": (0, 0)}],
                },
            ],
        },
    )
