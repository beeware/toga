import warnings

from .canvas import Canvas, OnResizeHandler, OnTouchHandler
from .context import ClosedPathContext, Context, FillContext, StrokeContext
from .drawingaction import (
    Arc,
    BeginPath,
    BezierCurveTo,
    ClosePath,
    DrawingAction,
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
from .geometry import arc_to_bezier, sweepangle

# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)

_deprecated_names = {
    # Jan 2026: DrawingAction was named DrawingObject in Toga 0.5.3 and earlier
    "DrawingObject": DrawingAction
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
