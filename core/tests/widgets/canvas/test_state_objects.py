import pytest

from toga.colors import REBECCAPURPLE, rgb
from toga.constants import FillRule
from toga.widgets.canvas import (
    ClosePath,
    Fill,
    Scale,
    State,
    Stroke,
)
from toga_dummy.utils import assert_action_performed

REBECCA_PURPLE_COLOR = rgb(102, 51, 153)


def test_sub_state(widget):
    """A state can produce a sub-state."""
    with widget.state() as sub_state:
        widget.line_to(30, 40)
    # A fresh state has been created as a sub-state of the canvas.
    assert isinstance(sub_state, State)
    assert sub_state is not widget.root_state

    assert_action_performed(widget, "redraw")
    assert repr(sub_state) == "State()"

    # The first and last instructions can be ignored; they're the root canvas state
    assert widget._impl.draw_instructions[1:-1] == [
        "save",
        ("line to", {"x": 30, "y": 40}),
        "restore",
    ]


def test_closed_path(widget):
    """A state can produce a ClosedPath sub-state."""
    with widget.close_path() as closed_path:
        widget.line_to(30, 40)

    # A fresh state has been created as a sub-state of the canvas.
    assert isinstance(closed_path, ClosePath)
    assert repr(closed_path) == "ClosePath()"

    assert_action_performed(widget, "redraw")

    # No attributes to test.

    # The first and last instructions can be ignored; they're the root canvas state
    assert widget._impl.draw_instructions[1:-1] == [
        "save",
        "begin path",
        ("line to", {"x": 30, "y": 40}),
        "close path",
        "restore",
    ]


@pytest.mark.parametrize(
    "kwargs, args_repr, properties",
    [
        # Defaults
        (
            {},
            "fill_rule=FillRule.NONZERO, fill_style=None",
            {
                "fill_rule": FillRule.NONZERO,
                "fill_style": None,
            },
        ),
        # Fill style
        (
            {"fill_style": REBECCAPURPLE},
            (f"fill_rule=FillRule.NONZERO, fill_style={REBECCA_PURPLE_COLOR!r}"),
            {"fill_rule": FillRule.NONZERO, "fill_style": REBECCA_PURPLE_COLOR},
        ),
        # Explicitly don't set fill style
        (
            {"fill_style": None},
            "fill_rule=FillRule.NONZERO, fill_style=None",
            {"fill_rule": FillRule.NONZERO, "fill_style": None},
        ),
        # Fill Rule
        (
            {"fill_rule": FillRule.EVENODD},
            "fill_rule=FillRule.EVENODD, fill_style=None",
            {"fill_style": None, "fill_rule": FillRule.EVENODD},
        ),
        # All args
        (
            {"fill_rule": FillRule.EVENODD, "fill_style": REBECCAPURPLE},
            f"fill_rule=FillRule.EVENODD, fill_style={REBECCA_PURPLE_COLOR!r}",
            {"fill_rule": FillRule.EVENODD, "fill_style": REBECCA_PURPLE_COLOR},
        ),
    ],
)
def test_fill(widget, kwargs, args_repr, properties):
    """A state can produce a Fill sub-state."""
    with widget.fill(**kwargs) as fill:
        widget.line_to(30, 40)

    # A fresh state has been created as a sub-state of the canvas.
    assert isinstance(fill, Fill)
    assert repr(fill) == f"Fill({args_repr})"

    # All the attributes can be retrieved.
    for attr, value in properties.items():
        assert getattr(fill, attr) == value

    commands = [
        "save",
        (
            ("set fill style", fill_style)
            if (fill_style := properties["fill_style"]) is not None
            else None
        ),
        "begin path",
        ("line to", {"x": 30, "y": 40}),
        ("fill", {"fill_rule": properties["fill_rule"]}),
        "restore",
    ]

    # The first and last instructions can be ignored; they're the root canvas state
    assert widget._impl.draw_instructions[1:-1] == [
        command for command in commands if command is not None
    ]


@pytest.mark.parametrize(
    "kwargs, args_repr, properties",
    [
        # Defaults
        (
            {},
            "stroke_style=None, line_width=None, line_dash=None",
            {"stroke_style": None, "line_width": None, "line_dash": None},
        ),
        # Color
        (
            {"stroke_style": REBECCAPURPLE},
            f"stroke_style={REBECCA_PURPLE_COLOR!r}, line_width=None, line_dash=None",
            {
                "stroke_style": REBECCA_PURPLE_COLOR,
                "line_width": None,
                "line_dash": None,
            },
        ),
        # Explicitly don't set stroke_style
        (
            {"stroke_style": None},
            "stroke_style=None, line_width=None, line_dash=None",
            {"stroke_style": None, "line_width": None, "line_dash": None},
        ),
        # Line width
        (
            {"line_width": 4.5},
            "stroke_style=None, line_width=4.500, line_dash=None",
            {"stroke_style": None, "line_width": 4.5, "line_dash": None},
        ),
        # Line dash
        (
            {"line_dash": [2, 7]},
            "stroke_style=None, line_width=None, line_dash=[2, 7]",
            {"stroke_style": None, "line_width": None, "line_dash": [2, 7]},
        ),
        # All args
        (
            {"stroke_style": REBECCAPURPLE, "line_width": 4.5, "line_dash": [2, 7]},
            (
                f"stroke_style={REBECCA_PURPLE_COLOR!r}, line_width=4.500, "
                "line_dash=[2, 7]"
            ),
            {
                "stroke_style": REBECCA_PURPLE_COLOR,
                "line_width": 4.5,
                "line_dash": [2, 7],
            },
        ),
    ],
)
def test_stroke(widget, kwargs, args_repr, properties):
    """A state can produce a Stroke sub-state."""
    with widget.stroke(**kwargs) as stroke:
        widget.line_to(30, 40)

    # A fresh state has been created as a sub-state of the canvas.
    assert isinstance(stroke, Stroke)
    assert repr(stroke) == f"Stroke({args_repr})"

    # All the attributes can be retrieved.
    for attr, value in properties.items():
        assert getattr(stroke, attr) == value

    commands = [
        "save",
        (
            ("set stroke style", stroke_style)
            if (stroke_style := properties["stroke_style"]) is not None
            else None
        ),
        (
            ("set line width", line_width)
            if (line_width := properties["line_width"]) is not None
            else None
        ),
        (
            ("set line dash", line_dash)
            if (line_dash := properties["line_dash"]) is not None
            else None
        ),
        "begin path",
        ("line to", {"x": 30, "y": 40}),
        "stroke",
        "restore",
    ]

    # The first and last instructions can be ignored; they're the root canvas state
    assert widget._impl.draw_instructions[1:-1] == [
        command for command in commands if command is not None
    ]


def assert_contents(container, contains: list, doesnt_contain: list):
    """Assert that the container contains (and doesn't contain) specified objects."""
    for item in contains:
        assert item in container

    for item in doesnt_contain:
        assert item not in container


def test_contains(widget):
    """Whether a drawing action is in a state can be tested."""
    with widget.stroke() as stroke:
        reset_transform = widget.reset_transform()
        with widget.fill() as fill:
            line_to = widget.line_to(0, 0)
        close_path = widget.close_path()

    scale = Scale(1, 1)

    # Assign a couple of shorthands for testing
    root = widget.root_state
    everything = [root, stroke, reset_transform, fill, line_to, close_path, scale]

    assert_contents(
        widget.root_state,
        contains=[stroke, reset_transform, fill, line_to, close_path],
        doesnt_contain=[root, scale],
    )

    assert_contents(
        stroke,
        contains=[reset_transform, fill, line_to, close_path],
        doesnt_contain=[root, stroke, scale],
    )

    assert_contents(
        reset_transform,
        contains=[],
        doesnt_contain=everything,
    )

    assert_contents(
        fill,
        contains=[line_to],
        doesnt_contain=[root, stroke, reset_transform, fill, close_path, scale],
    )

    assert_contents(
        close_path,
        contains=[],
        doesnt_contain=everything,
    )

    assert_contents(
        scale,
        contains=[],
        doesnt_contain=everything,
    )


NON_REENTRANT_MATCH = (
    r"A Canvas context manager can only be entered once, and only before any "
    r"subsequent drawing actions are added\."
)


def test_enter_open_context(widget):
    """Attempting to enter a currently open context is an error."""
    with widget.stroke() as stroke:
        with pytest.raises(RuntimeError, match=NON_REENTRANT_MATCH):
            with stroke:
                pass


def test_enter_closed_context(widget):
    """Attempting to enter a previously open (now closed) context is an error."""
    with widget.stroke() as stroke:
        pass

    with pytest.raises(RuntimeError, match=NON_REENTRANT_MATCH):
        with stroke:
            pass


def test_enter_context_out_of_order(widget):
    """Attempting to enter a context manager after making other actions is an error."""
    stroke = widget.stroke()
    widget.rect(0, 0, 0, 0)

    with pytest.raises(RuntimeError, match=NON_REENTRANT_MATCH):
        with stroke:
            pass
