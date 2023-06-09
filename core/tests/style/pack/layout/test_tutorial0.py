from travertino.size import at_least

from toga.style.pack import COLUMN, Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


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


def test_vertical():
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


def test_high_baseline_dpi():
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
