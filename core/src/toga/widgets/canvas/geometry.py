from math import cos, pi, sin, tan


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


def transform(x: float, y: float, matrix: list[int]) -> tuple[float, float]:
    return (
        x * matrix[0] + y * matrix[1],
        x * matrix[2] + y * matrix[3],
    )
