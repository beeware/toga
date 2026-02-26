from collections.abc import Iterable
from math import cos, pi, sin, tan
from typing import Protocol, runtime_checkable


@runtime_checkable
class CornerRadiusT(Protocol):
    """Protocol for objects that can be used as a corner radius."""

    x: float
    y: float


def sweepangle(startangle: float, endangle: float, counterclockwise: bool) -> float:
    """Returns an arc length in the range [-2 * pi, 2 * pi], where positive numbers are
    clockwise. Based on the "ellipse method steps" in the HTML spec."""

    if counterclockwise:
        if endangle - startangle <= -2 * pi:
            return -2 * pi
    else:
        if endangle - startangle >= 2 * pi:
            return 2 * pi

    startangle %= 2 * pi
    endangle %= 2 * pi
    sweepangle = endangle - startangle
    if counterclockwise:
        if sweepangle > 0:
            sweepangle -= 2 * pi
    else:
        if sweepangle < 0:
            sweepangle += 2 * pi

    return sweepangle


# Based on https://stackoverflow.com/a/30279817
def arc_to_bezier(sweepangle: float) -> list[tuple[float, float]]:
    """Approximates an arc of a unit circle as a sequence of Bezier segments.

    :param sweepangle: Length of the arc in radians, where positive numbers are
        clockwise.
    :returns: [(1, 0), (cp1x, cp1y), (cp2x, cp2y), (x, y), ...], where each group of 3
        points has the same meaning as in the bezier_curve_to method, and there are
        between 1 and 4 groups."""

    matrices = [
        [1, 0, 0, 1],  # 0 degrees
        [0, -1, 1, 0],  # 90
        [-1, 0, 0, -1],  # 180
        [0, 1, -1, 0],  # 270
    ]

    if sweepangle < 0:  # Counterclockwise
        sweepangle *= -1
        for matrix in matrices:
            matrix[2] *= -1
            matrix[3] *= -1

    result = [(1.0, 0.0)]
    for matrix in matrices:
        if sweepangle < 0:
            break

        phi = min(sweepangle, pi / 2)
        k = 4 / 3 * tan(phi / 4)
        result += [
            transform(x, y, matrix)
            for x, y in [
                (1, k),
                (cos(phi) + k * sin(phi), sin(phi) - k * cos(phi)),
                (cos(phi), sin(phi)),
            ]
        ]

        sweepangle -= pi / 2

    return result


def get_round_rect_radii(
    w: float,
    h: float,
    radii: float | CornerRadiusT | Iterable[float | CornerRadiusT],
) -> list[tuple[int | float, int | float]]:
    """Determine the corner radii for a rounded rectangle.

    This implements the procedure described here:
    https://html.spec.whatwg.org/multipage/canvas.html#dom-context-2d-roundrect

    Corner radii can be provided as:
    - a single numerical radius for both x and y radius for all corners
    - an object with attributes "x" and "y" for the x and y radius for all corners
    - a list of 1 to 4 of the above

    If the list has:
    - length 1, then the item gives the radius of all corners
    - length 2, then the upper left and lower right corners use the first radius,
        and upper right and lower left use the second radius
    - length 3, then the upper left corner uses the first radius, the upper right
        and lower left use the second radius, and the lower right corner uses the
        third radius
    - length 4, then the radii are given in order upper left, upper right, lower
        left, lower right

    If the radii are too large for the width or height, then they will be scaled.

    :param w: The width of the rounded rectangle.
    :param h: The height of the rounded rectangle.
    :param radii: The corner radii of the rounded rectangle.
    :returns: list of radii [ul, ur, ll, lr] for upper and lower left and right
        where each item is a 2-tuple of (rx, ry), the radius for x and y
        directions.
    """
    if isinstance(radii, (int, float, CornerRadiusT)):
        radii = [radii]
    else:
        radii = list(radii)
    if len(radii) == 1:
        radii *= 4
    elif len(radii) == 2:
        radii = [radii[0], radii[1], radii[1], radii[0]]
    elif len(radii) == 3:
        radii = [radii[0], radii[1], radii[1], radii[2]]
    elif len(radii) != 4:
        raise ValueError(
            f"Invalid radii: {radii!r}, expected length between 1 and 4 items"
        )
    # get corners
    corners = [(r, r) if isinstance(r, (int, float)) else (r.x, r.y) for r in radii]
    ul, ur, ll, lr = corners

    # ensure radii are smaller than sides
    top = ul[0] + ur[0]
    bottom = ll[0] + lr[0]
    horizontal = max(top, bottom, abs(w))
    left = ul[1] + ll[1]
    right = ur[1] + lr[1]
    vertical = max(left, right, abs(h))

    scale = min(abs(w) / horizontal, abs(h) / vertical)
    sign_x = w / abs(w) if w != 0 else 1
    sign_y = h / abs(h) if h != 0 else 1
    corners = [(sign_x * x * scale, sign_y * y * scale) for x, y in corners]
    return corners


def round_rect(context, x, y, w, h, radii):
    """Given a native context draw a rounded rectangle.

    This implements the procedure described here:
    https://html.spec.whatwg.org/multipage/canvas.html#dom-context-2d-roundrect

    The native context needs to implement at least move_to, line_to and ellipse.

    Corner radii can be provided as:
    - a single numerical radius for both x and y radius for all corners
    - an object with attributes "x" and "y" for the x and y radius for all corners
    - a list of 1 to 4 of the above

    If the list has:
    - length 1, then the item gives the radius of all corners
    - length 2, then the upper left and lower right corners use the first radius,
        and upper right and lower left use the second radius
    - length 3, then the upper left corner uses the first radius, the upper right
        and lower left use the second radius, and the lower right corner uses the
        third radius
    - length 4, then the radii are given in order upper left, upper right, lower
        left, lower right

    If the radii are too large for the width or height, then they will be scaled.

    :param x: The width of the rounded rectangle.
    :param y: The height of the rounded rectangle.
    :param w: The width of the rounded rectangle.
    :param h: The height of the rounded rectangle.
    :param radii: The corner radii of the rounded rectangle.
    """
    ul, ur, ll, lr = get_round_rect_radii(w, h, radii)
    context.move_to(x + ul[0], y)
    context.line_to(x + w - ur[0], y)
    context.ellipse(x + w - ur[0], y + ur[1], *ur, 0, -pi / 2, 0, False)
    context.line_to(x + w, y + h - lr[1])
    context.ellipse(x + w - lr[0], y + h - lr[1], *lr, 0, 0, pi / 2, False)
    context.line_to(x + ll[0], y + h)
    context.ellipse(x + ll[0], y + h - ll[1], *ll, 0, pi / 2, pi, False)
    context.line_to(x, y + ul[1])
    context.ellipse(x + ul[0], y + ul[1], *ul, 0, pi, 3 * pi / 2, False)
    context.move_to(x, y)


def transform(x: float, y: float, matrix: list[int]) -> tuple[float, float]:
    return (
        x * matrix[0] + y * matrix[1],
        x * matrix[2] + y * matrix[3],
    )
