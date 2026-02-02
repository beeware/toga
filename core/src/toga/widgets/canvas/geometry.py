from math import acos, cos, hypot, pi, sin, sqrt, tan
from typing import TypeAlias

point: TypeAlias = tuple[float, float]


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
def arc_to_bezier(sweepangle: float) -> list[point]:
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


def normalize_vector(x, y):
    """Given a vector, return its unit length representation."""
    length = hypot(x, y)
    return (x / length, y / length)


# Based on Kiva source code, BSD Licensed from Enthought
# https://github.com/enthought/enable/blob/5db2be21cce1198929011dc56a7edc7f8b0dcde5/kiva/arc_conversion.py#L41
# extended to generate curves for 2 quad bezier curves rather than 1
def arc_to_quad_points(
    start: point,
    p1: point,
    p2: point,
    radius: float,
) -> tuple[point, ...]:
    """Calculate the tangents and control points to turn arc_to() into cubic bezier.

    Given a starting point, two endpoints of a line segment, and a radius,
    calculate the control points that approximate arc_to() with two quadratic
    Bezier curves.

    :param start: The current point on the path.
    :p1: The intersection point of the two tangent lines.
    :p2: A point on the second tangent line.
    :returns: points (t1, [cp1, t2, cp2, t3]), where t1, t2, and t3 are tangent points
        on the circle, and cp1, cp2 are the control points for the quadratic Bezier
        curves.
    """
    if radius == 0 or start == p1 or p1 == p2:
        return (p1,)

    # calculate the angle between the two line segments
    v1 = normalize_vector(start[0] - p1[0], start[1] - p1[1])
    v2 = normalize_vector(p2[0] - p1[0], p2[1] - p1[1])
    angle = acos(v1[0] * v2[0] + v1[1] * v2[1])

    # punt if the half angle is zero or a multiple of pi
    sin_half_angle = sin(angle / 2.0)
    if abs(sin_half_angle) <= 0.00001:
        # 180 turn
        return (p1,)

    # calculate the distance from p1 to the center of the arc
    dist_to_center = radius / sin_half_angle
    # calculate the distance from p1 to each tangent point
    dist_to_tangent = sqrt(dist_to_center**2 - radius**2)

    if abs(dist_to_tangent) <= 0.00001:
        # straight line
        return (p1,)

    # calculate the tangent points
    t1 = (p1[0] + v1[0] * dist_to_tangent, p1[1] + v1[1] * dist_to_tangent)
    t3 = (p1[0] + v2[0] * dist_to_tangent, p1[1] + v2[1] * dist_to_tangent)

    # control points live on the tangent lines and the segment between them should
    # also be a tangent to the circle perpendicular to line from center to p1
    # Can calculate with similar right triangles (start, c, p1) and (b, cp1, p1)
    # where b is the point where the segment between the center and p1 intersects
    # the circle.
    distance_to_control = (dist_to_center - radius) / dist_to_tangent * dist_to_center
    cp1 = (p1[0] + v1[0] * distance_to_control, p1[1] + v1[1] * distance_to_control)
    cp2 = (p1[0] + v2[0] * distance_to_control, p1[1] + v2[1] * distance_to_control)

    # calculate tangent point where line from p1 to center intersects the arc
    # - normalized direction vector from p1 to center
    v = normalize_vector(v1[0] + v2[0], v1[1] + v2[1])
    # - distance along vector
    distance_to_arc = dist_to_center - radius
    t2 = (p1[0] + v[0] * distance_to_arc, p1[1] + v[1] * distance_to_arc)

    return (t1, cp1, t2, cp2, t3)


def transform(x: float, y: float, matrix: list[int]) -> tuple[float, float]:
    return (
        x * matrix[0] + y * matrix[1],
        x * matrix[2] + y * matrix[3],
    )
