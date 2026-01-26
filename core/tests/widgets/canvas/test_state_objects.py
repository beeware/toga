import pytest

from toga.colors import REBECCAPURPLE, rgb
from toga.constants import FillRule
from toga.widgets.canvas import (
    ClosedPathContext,
    FillContext,
    LineTo,
    State,
    StrokeContext,
)
from toga_dummy.utils import assert_action_performed

REBECCA_PURPLE_COLOR = rgb(102, 51, 153)


def test_sub_state(widget):
    """A state can produce a sub-state."""
    with widget.root_state.state() as sub_state:
        sub_state.line_to(30, 40)
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


@pytest.mark.parametrize(
    "kwargs, args_repr, has_move, properties",
    [
        # Defaults
        (
            {},
            "x=None, y=None",
            False,
            {"x": None, "y": None},
        ),
        # X only
        (
            {"x": 10},
            "x=10, y=None",
            False,
            {"x": 10, "y": None},
        ),
        # Y only
        (
            {"y": 20},
            "x=None, y=20",
            False,
            {"x": None, "y": 20},
        ),
        # X and Y
        (
            {"x": 10, "y": 20},
            "x=10, y=20",
            True,
            {"x": 10, "y": 20},
        ),
    ],
)
def test_closed_path(widget, kwargs, args_repr, has_move, properties):
    """A state can produce a ClosedPath sub-state."""
    with widget.root_state.ClosedPath(**kwargs) as closed_path:
        closed_path.line_to(30, 40)

    # A fresh state has been created as a sub-state of the canvas.
    assert isinstance(closed_path, ClosedPathContext)
    assert repr(closed_path) == f"ClosedPathContext({args_repr})"

    assert_action_performed(widget, "redraw")

    # All the attributes can be retrieved.
    for attr, value in properties.items():
        assert getattr(closed_path, attr) == value

    # The first and last instructions can be ignored; they're the root canvas state
    assert widget._impl.draw_instructions[1:-1] == [
        "save",
        "begin path",
    ] + ([("move to", {"x": 10, "y": 20})] if has_move else []) + [
        ("line to", {"x": 30, "y": 40}),
        "close path",
        "restore",
    ]


@pytest.mark.parametrize(
    "kwargs, args_repr, has_move, properties",
    [
        # Defaults
        (
            {},
            "x=None, y=None, color=None, fill_rule=FillRule.NONZERO",
            False,
            {
                "x": None,
                "y": None,
                "color": None,
                "fill_rule": FillRule.NONZERO,
            },
        ),
        # X only
        (
            {"x": 10},
            "x=10, y=None, color=None, fill_rule=FillRule.NONZERO",
            False,
            {"x": 10, "y": None, "color": None, "fill_rule": FillRule.NONZERO},
        ),
        # Y only
        (
            {"y": 20},
            "x=None, y=20, color=None, fill_rule=FillRule.NONZERO",
            False,
            {"x": None, "y": 20, "color": None, "fill_rule": FillRule.NONZERO},
        ),
        # X and Y
        (
            {"x": 10, "y": 20},
            "x=10, y=20, color=None, fill_rule=FillRule.NONZERO",
            True,
            {"x": 10, "y": 20, "color": None, "fill_rule": FillRule.NONZERO},
        ),
        # Color
        (
            {"color": REBECCAPURPLE},
            (
                f"x=None, y=None, color={REBECCA_PURPLE_COLOR!r}, "
                "fill_rule=FillRule.NONZERO"
            ),
            False,
            {
                "x": None,
                "y": None,
                "color": REBECCA_PURPLE_COLOR,
                "fill_rule": FillRule.NONZERO,
            },
        ),
        # Explicitly don't set color
        (
            {"color": None},
            "x=None, y=None, color=None, fill_rule=FillRule.NONZERO",
            False,
            {
                "x": None,
                "y": None,
                "color": None,
                "fill_rule": FillRule.NONZERO,
            },
        ),
        # Fill Rule
        (
            {"x": None, "y": None, "fill_rule": FillRule.EVENODD},
            "x=None, y=None, color=None, fill_rule=FillRule.EVENODD",
            False,
            {
                "x": None,
                "y": None,
                "color": None,
                "fill_rule": FillRule.EVENODD,
            },
        ),
        # All args
        (
            {"x": 10, "y": 20, "color": REBECCAPURPLE, "fill_rule": FillRule.EVENODD},
            f"x=10, y=20, color={REBECCA_PURPLE_COLOR!r}, fill_rule=FillRule.EVENODD",
            True,
            {
                "x": 10,
                "y": 20,
                "color": REBECCA_PURPLE_COLOR,
                "fill_rule": FillRule.EVENODD,
            },
        ),
    ],
)
def test_fill(widget, kwargs, args_repr, has_move, properties):
    """A state can produce a Fill sub-state."""
    with widget.root_state.Fill(**kwargs) as fill:
        fill.line_to(30, 40)

    # A fresh state has been created as a sub-state of the canvas.
    assert isinstance(fill, FillContext)
    assert repr(fill) == f"FillContext({args_repr})"

    # All the attributes can be retrieved.
    for attr, value in properties.items():
        assert getattr(fill, attr) == value

    # The first and last instructions can be ignored; they're the root canvas state
    commands = [
        "save",
        ("set fill style", color)
        if (color := properties["color"]) is not None
        else None,
        "begin path",
        ("move to", {"x": properties["x"], "y": properties["y"]}) if has_move else None,
        ("line to", {"x": 30, "y": 40}),
        ("fill", {"fill_rule": properties["fill_rule"]}),
        "restore",
    ]

    assert widget._impl.draw_instructions[1:-1] == [
        command for command in commands if command is not None
    ]


@pytest.mark.parametrize(
    "kwargs, args_repr, has_move, properties",
    [
        # Defaults
        (
            {},
            "x=None, y=None, color=None, line_width=None, line_dash=None",
            False,
            {
                "x": None,
                "y": None,
                "color": None,
                "line_width": None,
                "line_dash": None,
            },
        ),
        # X only
        (
            {"x": 10},
            "x=10, y=None, color=None, line_width=None, line_dash=None",
            False,
            {
                "x": 10,
                "y": None,
                "color": None,
                "line_width": None,
                "line_dash": None,
            },
        ),
        # Y only
        (
            {"y": 20},
            "x=None, y=20, color=None, line_width=None, line_dash=None",
            False,
            {
                "x": None,
                "y": 20,
                "color": None,
                "line_width": None,
                "line_dash": None,
            },
        ),
        # X and Y
        (
            {"x": 10, "y": 20},
            "x=10, y=20, color=None, line_width=None, line_dash=None",
            True,
            {
                "x": 10,
                "y": 20,
                "color": None,
                "line_width": None,
                "line_dash": None,
            },
        ),
        # Color
        (
            {"color": REBECCAPURPLE},
            (
                f"x=None, y=None, color={REBECCA_PURPLE_COLOR!r}, "
                f"line_width=None, line_dash=None"
            ),
            False,
            {
                "x": None,
                "y": None,
                "color": REBECCA_PURPLE_COLOR,
                "line_width": None,
                "line_dash": None,
            },
        ),
        # Explicitly don't set color
        (
            {"color": None},
            "x=None, y=None, color=None, line_width=None, line_dash=None",
            False,
            {
                "x": None,
                "y": None,
                "color": None,
                "line_width": None,
                "line_dash": None,
            },
        ),
        # Line width
        (
            {"x": None, "y": None, "line_width": 4.5},
            "x=None, y=None, color=None, line_width=4.5, line_dash=None",
            False,
            {
                "x": None,
                "y": None,
                "color": None,
                "line_width": 4.5,
                "line_dash": None,
            },
        ),
        # Line dash
        (
            {"x": None, "y": None, "line_dash": [2, 7]},
            "x=None, y=None, color=None, line_width=None, line_dash=[2, 7]",
            False,
            {
                "x": None,
                "y": None,
                "color": None,
                "line_width": None,
                "line_dash": [2, 7],
            },
        ),
        # All args
        (
            {
                "x": 10,
                "y": 20,
                "color": REBECCAPURPLE,
                "line_width": 4.5,
                "line_dash": [2, 7],
            },
            (
                f"x=10, y=20, color={REBECCA_PURPLE_COLOR!r}, "
                f"line_width=4.5, line_dash=[2, 7]"
            ),
            True,
            {
                "x": 10,
                "y": 20,
                "color": REBECCA_PURPLE_COLOR,
                "line_width": 4.5,
                "line_dash": [2, 7],
            },
        ),
    ],
)
def test_stroke(widget, kwargs, args_repr, has_move, properties):
    """A state can produce a Stroke sub-state."""
    with widget.root_state.Stroke(**kwargs) as stroke:
        stroke.line_to(30, 40)

    # A fresh state has been created as a sub-state of the canvas.
    assert isinstance(stroke, StrokeContext)
    assert repr(stroke) == f"StrokeContext({args_repr})"

    # All the attributes can be retrieved.
    for attr, value in properties.items():
        assert getattr(stroke, attr) == value

    commands = [
        "save",
        ("set stroke style", color)
        if (color := properties["color"]) is not None
        else None,
        ("set line width", line_width)
        if (line_width := properties["line_width"]) is not None
        else None,
        ("set line dash", line_dash)
        if (line_dash := properties["line_dash"]) is not None
        else None,
        "begin path",
        ("move to", {"x": properties["x"], "y": properties["y"]}) if has_move else None,
        ("line to", {"x": 30, "y": 40}),
        "stroke",
        "restore",
    ]

    # The first and last instructions can be ignored; they're the root canvas state
    assert widget._impl.draw_instructions[1:-1] == [
        command for command in commands if command is not None
    ]


def test_order_change(widget):
    """The order of state objects can be changed."""
    # Initially nothing on the state.
    assert len(widget.root_state) == 0

    # Set up an inner state that has contained operations, including a sub-state
    widget.root_state.line_to(0, 0)
    with widget.root_state.state() as state:
        state.line_to(10, 20)
        second = state.line_to(20, 30)
        with state.Fill() as fill:
            fill.line_to(25, 25)
        state.line_to(30, 40)
        state.line_to(40, 50)
    widget.root_state.line_to(99, 99)

    # Counts are as expected
    assert len(widget.root_state) == 3
    assert len(state) == 5
    assert len(fill) == 1

    # Initial draw instructions are as expected
    assert widget._impl.draw_instructions == [
        "save",
        ("line to", {"x": 0, "y": 0}),
        "save",
        ("line to", {"x": 10, "y": 20}),
        ("line to", {"x": 20, "y": 30}),
        # Begin fill
        "save",
        "begin path",
        ("line to", {"x": 25, "y": 25}),
        ("fill", {"fill_rule": FillRule.NONZERO}),
        "restore",
        # End fill
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 40, "y": 50}),
        "restore",
        ("line to", {"x": 99, "y": 99}),
        "restore",
    ]

    # Remove the second draw instruction
    state.remove(second)

    # Drawing objects are as expected
    assert len(widget.root_state) == 3
    for i, cls in enumerate([LineTo, State, LineTo]):
        assert isinstance(widget.root_state[i], cls)
    with pytest.raises(IndexError):
        widget.root_state[3]

    assert len(state) == 4
    assert len(fill) == 1

    # Draw instructions no longer have the second
    assert widget._impl.draw_instructions == [
        "save",
        ("line to", {"x": 0, "y": 0}),
        "save",
        ("line to", {"x": 10, "y": 20}),
        # Begin fill
        "save",
        "begin path",
        ("line to", {"x": 25, "y": 25}),
        ("fill", {"fill_rule": FillRule.NONZERO}),
        "restore",
        # End fill
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 40, "y": 50}),
        "restore",
        ("line to", {"x": 99, "y": 99}),
        "restore",
    ]

    # Insert the second draw instruction at index 3
    state.insert(3, second)

    # Counts are as expected
    assert len(widget.root_state) == 3
    assert len(state) == 5
    assert len(fill) == 1

    # Draw instructions show the new position
    assert widget._impl.draw_instructions == [
        "save",
        ("line to", {"x": 0, "y": 0}),
        "save",
        ("line to", {"x": 10, "y": 20}),
        # Begin fill
        "save",
        "begin path",
        ("line to", {"x": 25, "y": 25}),
        ("fill", {"fill_rule": FillRule.NONZERO}),
        "restore",
        # End fill
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 20, "y": 30}),
        ("line to", {"x": 40, "y": 50}),
        "restore",
        ("line to", {"x": 99, "y": 99}),
        "restore",
    ]

    # Remove the fill state
    state.remove(fill)

    # Counts are as expected
    assert len(widget.root_state) == 3
    assert len(state) == 4
    assert len(fill) == 1

    # Draw instructions show the new position
    assert widget._impl.draw_instructions == [
        "save",
        ("line to", {"x": 0, "y": 0}),
        "save",
        ("line to", {"x": 10, "y": 20}),
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 20, "y": 30}),
        ("line to", {"x": 40, "y": 50}),
        "restore",
        ("line to", {"x": 99, "y": 99}),
        "restore",
    ]

    # Insert the fill state at a negative index
    state.insert(-1, fill)
    # Draw instructions show the new position
    assert widget._impl.draw_instructions == [
        "save",
        ("line to", {"x": 0, "y": 0}),
        "save",
        ("line to", {"x": 10, "y": 20}),
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 20, "y": 30}),
        # Begin fill
        "save",
        "begin path",
        ("line to", {"x": 25, "y": 25}),
        ("fill", {"fill_rule": FillRule.NONZERO}),
        "restore",
        # End fill
        ("line to", {"x": 40, "y": 50}),
        "restore",
        ("line to", {"x": 99, "y": 99}),
        "restore",
    ]

    # Clear the state
    state.clear()

    # Counts are as expected
    assert len(widget.root_state) == 3
    assert len(state) == 0

    # No draw instructions other than the outer state.
    assert widget._impl.draw_instructions == [
        "save",
        ("line to", {"x": 0, "y": 0}),
        "save",
        "restore",
        ("line to", {"x": 99, "y": 99}),
        "restore",
    ]
