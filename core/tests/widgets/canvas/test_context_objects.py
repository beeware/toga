import pytest

from toga.colors import REBECCAPURPLE, rgb
from toga.constants import FillRule
from toga.widgets.canvas import (
    ClosedPathContext,
    Context,
    FillContext,
    LineTo,
    StrokeContext,
)
from toga_dummy.utils import assert_action_performed

REBECCA_PURPLE_COLOR = rgb(102, 51, 153)


def test_subcontext(widget):
    """A context can produce a subcontext."""
    with widget.context.Context() as subcontext:
        subcontext.line_to(30, 40)
    # A fresh context has been created as a subcontext of the canvas.
    assert isinstance(subcontext, Context)
    assert subcontext != widget.context

    assert_action_performed(widget, "redraw")
    assert repr(subcontext) == "Context()"

    # The first and last instructions can be ignored; they're the root canvas context
    assert widget._impl.draw_instructions[1:-1] == [
        ("push context", {}),
        ("line to", {"x": 30, "y": 40}),
        ("pop context", {}),
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
    """A context can produce a ClosedPath subcontext."""
    with widget.context.ClosedPath(**kwargs) as closed_path:
        closed_path.line_to(30, 40)

    # A fresh context has been created as a subcontext of the canvas.
    assert isinstance(closed_path, ClosedPathContext)
    assert repr(closed_path) == f"ClosedPathContext({args_repr})"

    assert_action_performed(widget, "redraw")

    # All the attributes can be retrieved.
    for attr, value in properties.items():
        assert getattr(closed_path, attr) == value

    # The first and last instructions can be ignored; they're the root canvas context
    assert widget._impl.draw_instructions[1:-1] == [
        ("push context", {}),
        ("begin path", {}),
    ] + ([("move to", {"x": 10, "y": 20})] if has_move else []) + [
        ("line to", {"x": 30, "y": 40}),
        ("close path", {}),
        ("pop context", {}),
    ]


@pytest.mark.parametrize(
    "kwargs, args_repr, has_move, properties",
    [
        # Defaults
        (
            {},
            "x=None, y=None, color=rgb(0, 0, 0), fill_rule=FillRule.NONZERO",
            False,
            {
                "x": None,
                "y": None,
                "color": rgb(0, 0, 0),
                "fill_rule": FillRule.NONZERO,
            },
        ),
        # X only
        (
            {"x": 10},
            "x=10, y=None, color=rgb(0, 0, 0), fill_rule=FillRule.NONZERO",
            False,
            {"x": 10, "y": None, "color": rgb(0, 0, 0), "fill_rule": FillRule.NONZERO},
        ),
        # Y only
        (
            {"y": 20},
            "x=None, y=20, color=rgb(0, 0, 0), fill_rule=FillRule.NONZERO",
            False,
            {"x": None, "y": 20, "color": rgb(0, 0, 0), "fill_rule": FillRule.NONZERO},
        ),
        # X and Y
        (
            {"x": 10, "y": 20},
            "x=10, y=20, color=rgb(0, 0, 0), fill_rule=FillRule.NONZERO",
            True,
            {"x": 10, "y": 20, "color": rgb(0, 0, 0), "fill_rule": FillRule.NONZERO},
        ),
        # Color
        (
            {"color": REBECCAPURPLE},
            f"x=None, y=None, color={REBECCA_PURPLE_COLOR}, fill_rule=FillRule.NONZERO",
            False,
            {
                "x": None,
                "y": None,
                "color": REBECCA_PURPLE_COLOR,
                "fill_rule": FillRule.NONZERO,
            },
        ),
        # Reset color with None
        (
            {"color": None},
            "x=None, y=None, color=rgb(0, 0, 0), fill_rule=FillRule.NONZERO",
            False,
            {
                "x": None,
                "y": None,
                "color": rgb(0, 0, 0),
                "fill_rule": FillRule.NONZERO,
            },
        ),
        # Fill Rule
        (
            {"x": None, "y": None, "fill_rule": FillRule.EVENODD},
            "x=None, y=None, color=rgb(0, 0, 0), fill_rule=FillRule.EVENODD",
            False,
            {
                "x": None,
                "y": None,
                "color": rgb(0, 0, 0),
                "fill_rule": FillRule.EVENODD,
            },
        ),
        # All args
        (
            {"x": 10, "y": 20, "color": REBECCAPURPLE, "fill_rule": FillRule.EVENODD},
            f"x=10, y=20, color={REBECCA_PURPLE_COLOR}, fill_rule=FillRule.EVENODD",
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
    """A context can produce a Fill subcontext."""
    with widget.context.Fill(**kwargs) as fill:
        fill.line_to(30, 40)

    # A fresh context has been created as a subcontext of the canvas.
    assert isinstance(fill, FillContext)
    assert repr(fill) == f"FillContext({args_repr})"

    # All the attributes can be retrieved.
    for attr, value in properties.items():
        assert getattr(fill, attr) == value

    # x and y aren't part of the fill instruction
    x = properties.pop("x")
    y = properties.pop("y")

    # The first and last instructions can be ignored; they're the root canvas context
    assert widget._impl.draw_instructions[1:-1] == [
        ("push context", {}),
        ("begin path", {}),
    ] + ([("move to", {"x": x, "y": y})] if has_move else []) + [
        (
            "line to",
            {
                "x": 30,
                "y": 40,
                "fill_color": properties["color"],
                "fill_rule": properties["fill_rule"],
            },
        ),
        ("fill", properties),
        ("pop context", {}),
    ]


@pytest.mark.parametrize(
    "kwargs, args_repr, has_move, properties",
    [
        # Defaults
        (
            {},
            "x=None, y=None, color=rgb(0, 0, 0), line_width=2.0, line_dash=None",
            False,
            {
                "x": None,
                "y": None,
                "color": rgb(0, 0, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        # X only
        (
            {"x": 10},
            "x=10, y=None, color=rgb(0, 0, 0), line_width=2.0, line_dash=None",
            False,
            {
                "x": 10,
                "y": None,
                "color": rgb(0, 0, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        # Y only
        (
            {"y": 20},
            "x=None, y=20, color=rgb(0, 0, 0), line_width=2.0, line_dash=None",
            False,
            {
                "x": None,
                "y": 20,
                "color": rgb(0, 0, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        # X and Y
        (
            {"x": 10, "y": 20},
            "x=10, y=20, color=rgb(0, 0, 0), line_width=2.0, line_dash=None",
            True,
            {
                "x": 10,
                "y": 20,
                "color": rgb(0, 0, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        # Color
        (
            {"color": REBECCAPURPLE},
            f"x=None, y=None, color={REBECCA_PURPLE_COLOR}, line_width=2.0, line_dash=None",
            False,
            {
                "x": None,
                "y": None,
                "color": REBECCA_PURPLE_COLOR,
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        # Reset color with None
        (
            {"color": None},
            "x=None, y=None, color=rgb(0, 0, 0), line_width=2.0, line_dash=None",
            False,
            {
                "x": None,
                "y": None,
                "color": rgb(0, 0, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        # Line width
        (
            {"x": None, "y": None, "line_width": 4.5},
            "x=None, y=None, color=rgb(0, 0, 0), line_width=4.5, line_dash=None",
            False,
            {
                "x": None,
                "y": None,
                "color": rgb(0, 0, 0),
                "line_width": 4.5,
                "line_dash": None,
            },
        ),
        # Line dash
        (
            {"x": None, "y": None, "line_dash": [2, 7]},
            "x=None, y=None, color=rgb(0, 0, 0), line_width=2.0, line_dash=[2, 7]",
            False,
            {
                "x": None,
                "y": None,
                "color": rgb(0, 0, 0),
                "line_width": 2.0,
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
            f"x=10, y=20, color={REBECCA_PURPLE_COLOR}, line_width=4.5, line_dash=[2, 7]",
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
    """A context can produce a Stroke subcontext."""
    with widget.context.Stroke(**kwargs) as stroke:
        stroke.line_to(30, 40)

    # A fresh context has been created as a subcontext of the canvas.
    assert isinstance(stroke, StrokeContext)
    assert repr(stroke) == f"StrokeContext({args_repr})"

    # All the attributes can be retrieved.
    for attr, value in properties.items():
        assert getattr(stroke, attr) == value

    # x and y aren't part of the stroke instruction
    x = properties.pop("x")
    y = properties.pop("y")

    # The first and last instructions can be ignored; they're the root canvas context
    assert widget._impl.draw_instructions[1:-1] == [
        ("push context", {}),
        ("begin path", {}),
    ] + ([("move to", {"x": x, "y": y})] if has_move else []) + [
        (
            "line to",
            {
                "x": 30,
                "y": 40,
                "stroke_color": properties["color"],
                "line_width": properties["line_width"],
                "line_dash": properties["line_dash"],
            },
        ),
        ("stroke", properties),
        ("pop context", {}),
    ]


def test_deprecated_drawing_operations(widget):
    """Deprecated simple drawing operations raise a warning."""

    with pytest.warns(
        DeprecationWarning,
        match=r"Context.new_path\(\) has been renamed Context.begin_path\(\)",
    ):
        widget.context.new_path()

    with pytest.warns(
        DeprecationWarning,
        match=r"Context.context\(\) has been renamed Context.Context\(\)",
    ):
        with widget.context.context() as subcontext:
            subcontext.line_to(20, 30)
            subcontext.line_to(30, 20)

    with pytest.warns(
        DeprecationWarning,
        match=r"Context.closed_path\(\) has been renamed Context.ClosedPath\(\)",
    ):
        with widget.context.closed_path(10, 20) as closed_path:
            closed_path.line_to(20, 30)
            closed_path.line_to(30, 20)

    # Assert the deprecated draw instructions rendered as expected
    assert widget._impl.draw_instructions == [
        ("push context", {}),
        ("begin path", {}),
        # Context
        ("push context", {}),
        ("line to", {"x": 20, "y": 30}),
        ("line to", {"x": 30, "y": 20}),
        ("pop context", {}),
        # ClosedPath
        ("push context", {}),
        ("begin path", {}),
        ("move to", {"x": 10, "y": 20}),
        ("line to", {"x": 20, "y": 30}),
        ("line to", {"x": 30, "y": 20}),
        ("close path", {}),
        ("pop context", {}),
        ("pop context", {}),
    ]


def test_order_change(widget):
    """The order of context objects can be changed."""
    # Initially nothing on the context.
    assert len(widget.context) == 0

    # Set up an inner context that has contained operations, including a subcontext
    widget.context.line_to(0, 0)
    with widget.Context() as context:
        context.line_to(10, 20)
        second = context.line_to(20, 30)
        with context.Fill() as fill:
            fill.line_to(25, 25)
        context.line_to(30, 40)
        context.line_to(40, 50)
    widget.context.line_to(99, 99)

    # Counts are as expected
    assert len(widget.context) == 3
    assert len(context) == 5
    assert len(fill) == 1

    # Initial draw instructions are as expected
    assert widget._impl.draw_instructions == [
        ("push context", {}),
        ("line to", {"x": 0, "y": 0}),
        ("push context", {}),
        ("line to", {"x": 10, "y": 20}),
        ("line to", {"x": 20, "y": 30}),
        # Begin fill
        ("push context", {}),
        ("begin path", {}),
        (
            "line to",
            {
                "x": 25,
                "y": 25,
                "fill_color": rgb(0, 0, 0),
                "fill_rule": FillRule.NONZERO,
            },
        ),
        ("fill", {"color": rgb(0, 0, 0), "fill_rule": FillRule.NONZERO}),
        ("pop context", {}),
        # End fill
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 40, "y": 50}),
        ("pop context", {}),
        ("line to", {"x": 99, "y": 99}),
        ("pop context", {}),
    ]

    # Remove the second draw instruction
    context.remove(second)

    # Drawing objects are as expected
    assert len(widget.context) == 3
    for i, cls in enumerate([LineTo, Context, LineTo]):
        assert isinstance(widget.context[i], cls)
    with pytest.raises(IndexError):
        widget.context[3]

    assert len(context) == 4
    assert len(fill) == 1

    # Draw instructions no longer have the second
    assert widget._impl.draw_instructions == [
        ("push context", {}),
        ("line to", {"x": 0, "y": 0}),
        ("push context", {}),
        ("line to", {"x": 10, "y": 20}),
        # Begin fill
        ("push context", {}),
        ("begin path", {}),
        (
            "line to",
            {
                "x": 25,
                "y": 25,
                "fill_color": rgb(0, 0, 0),
                "fill_rule": FillRule.NONZERO,
            },
        ),
        ("fill", {"color": rgb(0, 0, 0), "fill_rule": FillRule.NONZERO}),
        ("pop context", {}),
        # End fill
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 40, "y": 50}),
        ("pop context", {}),
        ("line to", {"x": 99, "y": 99}),
        ("pop context", {}),
    ]

    # Insert the second draw instruction at index 3
    context.insert(3, second)

    # Counts are as expected
    assert len(widget.context) == 3
    assert len(context) == 5
    assert len(fill) == 1

    # Draw instructions show the new position
    assert widget._impl.draw_instructions == [
        ("push context", {}),
        ("line to", {"x": 0, "y": 0}),
        ("push context", {}),
        ("line to", {"x": 10, "y": 20}),
        # Begin fill
        ("push context", {}),
        ("begin path", {}),
        (
            "line to",
            {
                "x": 25,
                "y": 25,
                "fill_color": rgb(0, 0, 0),
                "fill_rule": FillRule.NONZERO,
            },
        ),
        ("fill", {"color": rgb(0, 0, 0), "fill_rule": FillRule.NONZERO}),
        ("pop context", {}),
        # End fill
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 20, "y": 30}),
        ("line to", {"x": 40, "y": 50}),
        ("pop context", {}),
        ("line to", {"x": 99, "y": 99}),
        ("pop context", {}),
    ]

    # Remove the fill context
    context.remove(fill)

    # Counts are as expected
    assert len(widget.context) == 3
    assert len(context) == 4
    assert len(fill) == 1

    # Draw instructions show the new position
    assert widget._impl.draw_instructions == [
        ("push context", {}),
        ("line to", {"x": 0, "y": 0}),
        ("push context", {}),
        ("line to", {"x": 10, "y": 20}),
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 20, "y": 30}),
        ("line to", {"x": 40, "y": 50}),
        ("pop context", {}),
        ("line to", {"x": 99, "y": 99}),
        ("pop context", {}),
    ]

    # Insert the fill context at a negative index
    context.insert(-1, fill)
    # Draw instructions show the new position
    assert widget._impl.draw_instructions == [
        ("push context", {}),
        ("line to", {"x": 0, "y": 0}),
        ("push context", {}),
        ("line to", {"x": 10, "y": 20}),
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 20, "y": 30}),
        # Begin fill
        ("push context", {}),
        ("begin path", {}),
        (
            "line to",
            {
                "x": 25,
                "y": 25,
                "fill_color": rgb(0, 0, 0),
                "fill_rule": FillRule.NONZERO,
            },
        ),
        ("fill", {"color": rgb(0, 0, 0), "fill_rule": FillRule.NONZERO}),
        ("pop context", {}),
        # End fill
        ("line to", {"x": 40, "y": 50}),
        ("pop context", {}),
        ("line to", {"x": 99, "y": 99}),
        ("pop context", {}),
    ]

    # Clear the context
    context.clear()

    # Counts are as expected
    assert len(widget.context) == 3
    assert len(context) == 0

    # No draw instructions other than the outer context.
    assert widget._impl.draw_instructions == [
        ("push context", {}),
        ("line to", {"x": 0, "y": 0}),
        ("push context", {}),
        ("pop context", {}),
        ("line to", {"x": 99, "y": 99}),
        ("pop context", {}),
    ]


def test_stacked_kwargs(widget):
    """If contexts are stacked, kwargs for sub operations don't leak."""
    widget.context.line_to(0, 0)
    with widget.Fill(color=rgb(255, 0, 0)) as fill1:
        fill1.line_to(10, 20)
        with fill1.Stroke(color=rgb(0, 255, 0)) as stroke1:
            stroke1.line_to(20, 30)
            with stroke1.Fill(color=rgb(0, 0, 255)) as fill2:
                fill2.line_to(100, 200)
                with fill2.Stroke(color=rgb(255, 255, 0)) as stroke2:
                    stroke2.line_to(200, 300)
                fill2.line_to(300, 400)
            stroke1.line_to(70, 80)
        fill1.line_to(80, 90)
    widget.context.line_to(99, 99)

    assert widget._impl.draw_instructions == [
        ("push context", {}),
        ("line to", {"x": 0, "y": 0}),
        # begin fill1
        ("push context", {}),
        ("begin path", {}),
        (
            "line to",
            {
                "x": 10,
                "y": 20,
                "fill_color": rgb(255, 0, 0),
                "fill_rule": FillRule.NONZERO,
            },
        ),
        # begin stroke 1
        ("push context", {"fill_color": rgb(255, 0, 0), "fill_rule": FillRule.NONZERO}),
        ("begin path", {"fill_color": rgb(255, 0, 0), "fill_rule": FillRule.NONZERO}),
        (
            "line to",
            {
                "x": 20,
                "y": 30,
                "fill_color": rgb(255, 0, 0),
                "fill_rule": FillRule.NONZERO,
                "stroke_color": rgb(0, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        # begin fill 2
        (
            "push context",
            {
                "fill_color": rgb(255, 0, 0),
                "fill_rule": FillRule.NONZERO,
                "stroke_color": rgb(0, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        (
            "begin path",
            {
                "fill_color": rgb(255, 0, 0),
                "fill_rule": FillRule.NONZERO,
                "stroke_color": rgb(0, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        (
            "line to",
            {
                "x": 100,
                "y": 200,
                "fill_color": rgb(0, 0, 255),
                "fill_rule": FillRule.NONZERO,
                "stroke_color": rgb(0, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        # stroke 2
        (
            "push context",
            {
                "fill_color": rgb(0, 0, 255),
                "fill_rule": FillRule.NONZERO,
                "stroke_color": rgb(0, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        (
            "begin path",
            {
                "fill_color": rgb(0, 0, 255),
                "fill_rule": FillRule.NONZERO,
                "stroke_color": rgb(0, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        (
            "line to",
            {
                "x": 200,
                "y": 300,
                "fill_color": rgb(0, 0, 255),
                "fill_rule": FillRule.NONZERO,
                "stroke_color": rgb(255, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        (
            "stroke",
            {
                "color": rgb(255, 255, 0),
                "fill_color": rgb(0, 0, 255),
                "fill_rule": FillRule.NONZERO,
                "stroke_color": rgb(0, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        (
            "pop context",
            {
                "fill_color": rgb(0, 0, 255),
                "fill_rule": FillRule.NONZERO,
                "stroke_color": rgb(0, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        # # end stroke 2
        (
            "line to",
            {
                "x": 300,
                "y": 400,
                "fill_color": rgb(0, 0, 255),
                "fill_rule": FillRule.NONZERO,
                "stroke_color": rgb(0, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        (
            "fill",
            {
                "color": rgb(0, 0, 255),
                "fill_rule": FillRule.NONZERO,
                "fill_color": rgb(255, 0, 0),
                "stroke_color": rgb(0, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        (
            "pop context",
            {
                "fill_color": rgb(255, 0, 0),
                "fill_rule": FillRule.NONZERO,
                "stroke_color": rgb(0, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        # end fill 2
        (
            "line to",
            {
                "x": 70,
                "y": 80,
                "fill_color": rgb(255, 0, 0),
                "fill_rule": FillRule.NONZERO,
                "stroke_color": rgb(0, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
            },
        ),
        (
            "stroke",
            {
                "color": rgb(0, 255, 0),
                "line_width": 2.0,
                "line_dash": None,
                "fill_color": rgb(255, 0, 0),
                "fill_rule": FillRule.NONZERO,
            },
        ),
        ("pop context", {"fill_color": rgb(255, 0, 0), "fill_rule": FillRule.NONZERO}),
        # end stroke 1
        (
            "line to",
            {
                "x": 80,
                "y": 90,
                "fill_color": rgb(255, 0, 0),
                "fill_rule": FillRule.NONZERO,
            },
        ),
        ("fill", {"color": rgb(255, 0, 0), "fill_rule": FillRule.NONZERO}),
        ("pop context", {}),
        # end fill 1
        ("line to", {"x": 99, "y": 99}),
        ("pop context", {}),
    ]


def test_deprecated_args(widget):
    """Deprecated arguments to canvas functions raise warnings."""

    # fill() raises a warning about preserve being deprecated, then raises an error when
    # it's used as a context manager.
    with pytest.raises(
        RuntimeError,
        match=r"Context\.fill\(\) has been renamed Context\.Fill\(\)\.",
    ):
        with pytest.warns(
            DeprecationWarning,
            match=r"The `preserve` argument on fill\(\) has been deprecated.",
        ):
            with widget.context.fill(
                "rebeccapurple", FillRule.EVENODD, preserve=False
            ) as fill:
                fill.line_to(20, 30)
                fill.line_to(30, 20)
