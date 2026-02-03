import warnings

from .canvas import Canvas, OnResizeHandler, OnTouchHandler
from .drawingaction import (
    Arc,
    BeginPath,
    BezierCurveTo,
    DrawImage,
    DrawingAction,
    Ellipse,
    LineTo,
    MoveTo,
    QuadraticCurveTo,
    Rect,
    ResetTransform,
    Rotate,
    Scale,
    Translate,
    WriteText,
)
from .geometry import arc_to_bezier, sweepangle
from .state import ClosePath, Fill, State, Stroke

# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)

_deprecated_names = {
    # 2026-02: The following have different names than they did in Toga 0.5.3 and
    # earlier.
    "DrawingObject": DrawingAction,
    "Context": State,
    # No one should be using these directly anyway, but just in case...
    "ClosedPathContext": ClosePath,
    "FillContext": Fill,
    "StrokeContext": Stroke,
}


def __getattr__(name):
    if cls := _deprecated_names.get(name):
        warnings.warn(
            f"{name} has been renamed to {cls.__name__}",
            DeprecationWarning,
            stacklevel=2,
        )
        return cls
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Canvas",
    "OnResizeHandler",
    "OnTouchHandler",
    # Drawing Actions
    "DrawingAction",
    "Arc",
    "BeginPath",
    "BezierCurveTo",
    "DrawImage",
    "Ellipse",
    "LineTo",
    "MoveTo",
    "QuadraticCurveTo",
    "Rect",
    "ResetTransform",
    "Rotate",
    "Scale",
    "Translate",
    "WriteText",
    # States
    "State",
    "Fill",
    "Stroke",
    "ClosePath",
    # Geometry
    "arc_to_bezier",
    "sweepangle",
]
