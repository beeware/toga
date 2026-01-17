import warnings

from .action import (
    Action,
    Arc,
    BeginPath,
    BezierCurveTo,
    ClosePath,
    Ellipse,
    Fill,
    LineTo,
    MoveTo,
    QuadraticCurveTo,
    Rect,
    ResetTransform,
    Rotate,
    Scale,
    Stroke,
    Translate,
    WriteText,
)
from .canvas import Canvas, OnResizeHandler, OnTouchHandler
from .context import ClosedPathContext, Context, FillContext, StrokeContext
from .geometry import arc_to_bezier, sweepangle

# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)

_deprecated_names = {"DrawingObject": "Action"}


def __getattr__(name):
    if new_name := _deprecated_names.get(name):
        warnings.warn(
            f"{name} has been renamed to {new_name}",
            DeprecationWarning,
            stacklevel=2,
        )
        return globals()[new_name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Canvas",
    "OnResizeHandler",
    "OnTouchHandler",
    # Actions,
    "Action",
    "Arc",
    "BeginPath",
    "BezierCurveTo",
    "ClosePath",
    "Ellipse",
    "Fill",
    "LineTo",
    "MoveTo",
    "QuadraticCurveTo",
    "Rect",
    "ResetTransform",
    "Rotate",
    "Scale",
    "Stroke",
    "Translate",
    "WriteText",
    # Context
    "ClosedPathContext",
    "Context",
    "FillContext",
    "StrokeContext",
    # Geometry
    "arc_to_bezier",
    "sweepangle",
]
