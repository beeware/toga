import pytest

from travertino.colors import Color, color, hsl, rgb

from ..utils import assert_equal_color


def assert_parsed_equal_color(actual, expected):
    actual = Color.parse(actual)
    assert_equal_color(actual, expected, abs=0.001)


def test_noop():
    assert_parsed_equal_color(rgb(1, 2, 3, 0.5), rgb(1, 2, 3, 0.5))
    assert_parsed_equal_color(hsl(1, 0.2, 0.3), hsl(1, 0.2, 0.3))


@pytest.mark.parametrize(
    "value, expected",
    [
        ("#123", (0x11, 0x22, 0x33)),
        ("#112233", (0x11, 0x22, 0x33)),
        ("#abc", (0xAA, 0xBB, 0xCC)),
        ("#ABC", (0xAA, 0xBB, 0xCC)),
        ("#abcdef", (0xAB, 0xCD, 0xEF)),
        ("#ABCDEF", (0xAB, 0xCD, 0xEF)),
        #
        ("#1234", (0x11, 0x22, 0x33, 0.2666)),
        ("#11223344", (0x11, 0x22, 0x33, 0.2666)),
        ("#abcd", (0xAA, 0xBB, 0xCC, 0.8666)),
        ("#ABCD", (0xAA, 0xBB, 0xCC, 0.8666)),
        ("#abcdefba", (0xAB, 0xCD, 0xEF, 0.7294)),
        ("#ABCDEFBA", (0xAB, 0xCD, 0xEF, 0.7294)),
    ],
)
def test_hex_rgb(value, expected):
    assert_parsed_equal_color(value, rgb(*expected))


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
    assert_parsed_equal_color(value, rgb(*expected))


def test_named_color_invalid():
    with pytest.raises(ValueError):
        Color.parse("not a color")


@pytest.mark.parametrize(
    "num_digits",
    [1, 2, 5, 7, 9, 10],
)
def test_hash_mark_invalid_length(num_digits):
    """An invalid number of digts after # raises a ValueError."""
    with pytest.raises(ValueError):
        Color.parse(f"#{'1' * num_digits}")


def test_invalid_hex_rgb():
    """Digits out of the hex range raise an error."""
    with pytest.raises(ValueError):
        Color.parse("#aabbccddhh")


@pytest.mark.parametrize(
    "value",
    [None, 25, rgb],
)
def test_other_invalid_inputs(value):
    """Other random junk doesn't work either."""
    with pytest.raises(ValueError):
        Color.parse(value)


def test_deprecated():
    """The color() function is deprecated."""
    with pytest.warns(
        DeprecationWarning,
        match=r"The color\(\) function is deprecated\. Use Color\.parse\(\) instead\.",
    ):
        color("#FFF")
