import pytest

from travertino.colors import color, hsl, hsla, rgb, rgba


def assert_equal_hsl(value, expected):
    # Nothing fancy - a color is equal if the attributes are all the same
    actual = color(value)
    assert actual.h == expected.h
    assert actual.s == expected.s
    assert actual.l == expected.l
    assert actual.a == pytest.approx(expected.a, abs=0.001)


def assert_equal_rgb(value, expected):
    # Nothing fancy - a color is equal if the attributes are all the same
    actual = color(value)
    assert actual.r == expected.r
    assert actual.g == expected.g
    assert actual.b == expected.b
    assert actual.a == pytest.approx(expected.a, abs=0.001)


def test_noop():
    assert_equal_rgb(rgba(1, 2, 3, 0.5), rgba(1, 2, 3, 0.5))
    assert_equal_hsl(hsl(1, 0.2, 0.3), hsl(1, 0.2, 0.3))


@pytest.mark.parametrize(
    "value, expected",
    [
        ("rgb(1,2,3)", (1, 2, 3)),
        ("rgb(1, 2, 3)", (1, 2, 3)),
        ("rgb( 1 , 2 , 3)", (1, 2, 3)),
        ("#123", (0x11, 0x22, 0x33)),
        ("#112233", (0x11, 0x22, 0x33)),
        ("#abc", (0xAA, 0xBB, 0xCC)),
        ("#ABC", (0xAA, 0xBB, 0xCC)),
        ("#abcdef", (0xAB, 0xCD, 0xEF)),
        ("#ABCDEF", (0xAB, 0xCD, 0xEF)),
    ],
)
def test_rgb(value, expected):
    assert_equal_rgb(value, rgb(*expected))


@pytest.mark.parametrize(
    "value",
    [
        "10, 20",
        "a, 10, 20",
        "10, b, 20",
        "10, 20, c",
        "10, 20, 30, 0.5",
    ],
)
def test_rgb_invalid(value):
    with pytest.raises(ValueError):
        color(f"rgb({value})")


@pytest.mark.parametrize(
    "value, expected",
    [
        ("rgba(1,2,3,0.5)", (1, 2, 3, 0.5)),
        ("rgba(1, 2, 3, 0.5)", (1, 2, 3, 0.5)),
        ("rgba( 1 , 2 , 3 , 0.5)", (1, 2, 3, 0.5)),
        ("#1234", (0x11, 0x22, 0x33, 0.2666)),
        ("#11223344", (0x11, 0x22, 0x33, 0.2666)),
        ("#abcd", (0xAA, 0xBB, 0xCC, 0.8666)),
        ("#ABCD", (0xAA, 0xBB, 0xCC, 0.8666)),
        ("#abcdefba", (0xAB, 0xCD, 0xEF, 0.7294)),
        ("#ABCDEFBA", (0xAB, 0xCD, 0xEF, 0.7294)),
    ],
)
def test_rgba(value, expected):
    assert_equal_rgb(value, rgba(*expected))


@pytest.mark.parametrize(
    "value",
    [
        "10, 20, 30",
        "a, 10, 20, 0.5",
        "10, b, 20, 0.5",
        "10, 20, c, 0.5",
        "10, 20, 30, c",
        "10, 20, 30, 0.5, 5",
    ],
)
def test_rgba_invalid(value):
    with pytest.raises(ValueError):
        color(f"rgba({value})")


@pytest.mark.parametrize(
    "value",
    [
        "1,20%,30%",
        "1, 20%, 30%",
        "1, 20% , 30%",
    ],
)
def test_hsl(value):
    assert_equal_hsl(f"hsl({value})", hsl(1, 0.2, 0.3))


@pytest.mark.parametrize(
    "value",
    [
        "1, 20%",
        "a, 20%, 30%",
        "1, a, 30%",
        "1, 20%, a)",
        "1, 20%, 30%, 0.5)",
    ],
)
def test_hsl_invalid(value):
    with pytest.raises(ValueError):
        color(value)


@pytest.mark.parametrize(
    "value",
    [
        "1,20%,30%,0.5",
        "1, 20%, 30%, 0.5",
        " 1, 20% , 30% , 0.5",
    ],
)
def test_hsla(value):
    assert_equal_hsl(f"hsla({value})", hsla(1, 0.2, 0.3, 0.5))


@pytest.mark.parametrize(
    "value",
    [
        "1, 20%, 30%",
        "a, 20%, 30%, 0.5",
        "1, a, 30%, 0.5",
        "1, 20%, a, 0.5",
        "1, 20%, 30%, a",
        "1, 20%, 30%, 0.5, 5",
    ],
)
def test_hsla_invalid(value):
    with pytest.raises(ValueError):
        color(f"hsla({value})")


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Red", (0xFF, 0, 0)),
        ("RED", (0xFF, 0, 0)),
        ("red", (0xFF, 0, 0)),
        ("rEd", (0xFF, 0, 0)),
        ("CornflowerBlue", (0x64, 0x95, 0xED)),
        ("cornflowerblue", (0x64, 0x95, 0xED)),
        ("CORNFLOWERBLUE", (0x64, 0x95, 0xED)),
        ("Cornflowerblue", (0x64, 0x95, 0xED)),
        ("CoRnFlOwErBlUe", (0x64, 0x95, 0xED)),
    ],
)
def test_named_color(value, expected):
    assert_equal_rgb(value, rgb(*expected))


def test_named_color_invalid():
    with pytest.raises(ValueError):
        color("not a color")
