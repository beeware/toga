from decimal import Decimal
from fractions import Fraction

import pytest

from travertino.colors import hsl, hsla, rgb, rgba


@pytest.mark.parametrize(
    "constructors, value, expected_repr, expected_str",
    [
        ((rgb, rgba), (10, 20, 30), "rgb(10, 20, 30, 1.0)", "rgb(10 20 30 / 1.0)"),
        ((rgb, rgba), (10, 20, 30, 0.5), "rgb(10, 20, 30, 0.5)", "rgb(10 20 30 / 0.5)"),
        (
            (hsl, hsla),
            (10, 0.2, 0.3),
            "hsl(10, 0.2, 0.3, 1.0)",
            "hsl(10 20% 30% / 1.0)",
        ),
        (
            (hsl, hsla),
            (10, 0.2, 0.3, 0.5),
            "hsl(10, 0.2, 0.3, 0.5)",
            "hsl(10 20% 30% / 0.5)",
        ),
    ],
)
@pytest.mark.parametrize("use_alias", [True, False])
def test_repr_and_str(constructors, value, expected_repr, expected_str, use_alias):
    """Colors' __str__ and __repr__ methods work properly."""
    constructor = constructors[use_alias]
    color = constructor(*value)
    assert repr(color) == expected_repr
    assert str(color) == expected_str


def test_aliases():
    """rgba and hsl should be direct aliases."""
    assert rgba is rgb
    assert hsla is hsl


def test_rgb_hash():
    """Hashes are consistent for the same color and unequal otherwise."""
    assert hash(rgb(10, 20, 30)) == hash(rgb(10, 20, 30))
    assert hash(rgb(10, 20, 30)) != hash(rgb(30, 20, 10))
    assert hash(rgb(10, 20, 30, 0.5)) == hash(rgb(10, 20, 30, 0.5))
    assert hash(rgb(10, 20, 30, 1.0)) == hash(rgb(10, 20, 30))
    assert hash(rgb(10, 20, 30)) != hash(rgb(30, 20, 10))


def test_hsl_hash():
    """Hashes are consistent for the same color and unequal otherwise."""
    assert hash(hsl(10, 0.2, 0.3)) == hash(hsl(10, 0.2, 0.3))
    assert hash(hsl(10, 0.3, 0.2)) != hash(hsl(10, 0.2, 0.3))
    assert hash(hsl(10, 0.2, 0.3, 0.5)) == hash(hsl(10, 0.2, 0.3, 0.5))
    assert hash(hsl(10, 0.2, 0.3, 1.0)) == hash(hsl(10, 0.2, 0.3))
    assert hash(hsl(10, 0.3, 0.2, 0.5)) != hash(hsl(10, 0.2, 0.3, 0.5))
    assert hash(hsl(10, 0, 0, 0.5)) != hash(rgb(10, 0, 0, 0.5))


@pytest.mark.parametrize(
    "constructor, value, name, actual",
    [
        (rgb, ("a", 120, 10, 0.5), "red", "a"),
        (rgb, (None, 120, 10, 0.5), "red", None),
        (rgb, (120, "a", 10, 0.5), "green", "a"),
        (rgb, (120, None, 10, 0.5), "green", None),
        (rgb, (120, 10, "a", 0.5), "blue", "a"),
        (rgb, (120, 10, None, 0.5), "blue", None),
        (rgb, (120, 10, 60, "a"), "alpha", "a"),
        (rgb, (120, 10, 60, None), "alpha", None),
        #
        (hsl, ("a", 0.5, 0.8, 0.5), "hue", "a"),
        (hsl, (None, 0.5, 0.8, 0.5), "hue", None),
        (hsl, (120, "a", 0.8, 0.5), "saturation", "a"),
        (hsl, (120, None, 0.8, 0.5), "saturation", None),
        (hsl, (120, 0.8, "a", 0.5), "lightness", "a"),
        (hsl, (120, 0.8, None, 0.5), "lightness", None),
        (hsl, (120, 0.8, 0.5, "a"), "alpha", "a"),
        (hsl, (120, 0.8, 0.5, None), "alpha", None),
    ],
)
def test_invalid_color_constructor(constructor, value, name, actual):
    """Invalid types are rejected."""
    with pytest.raises(
        TypeError,
        match=rf"^Value for {name} must be a number; got {actual!r}$",
    ):
        constructor(*value)


@pytest.mark.parametrize(
    "value, expected",
    [
        (25, 25),
        (100.0, 100),
        (50.3, 50),
        (50.8, 51),
        (Decimal("1"), 1),
        (Decimal("10.7"), 11),
        (Fraction(2, 3), 1),
        (Fraction(1, 16), 0),
        (-1, 0),
        (-100, 0),
        (300, 255),
    ],
)
@pytest.mark.parametrize("band", ["r", "g", "b"])
def test_rgb_normalization(value, expected, band):
    """Values are clipped and/or converted appropriately."""
    args = {"r": 10, "g": 10, "b": 10} | {band: value}
    color = rgb(**args)
    actual = getattr(color, band)
    assert isinstance(actual, int)
    assert actual == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (25, 25),
        (100.0, 100),
        (50.3, 50),
        (50.8, 51),
        (Decimal("1"), 1),
        (Decimal("10.7"), 11),
        (Fraction(2, 3), 1),
        (Fraction(1, 16), 0),
        (-1, 359),
        (-100, 260),
        (380, 20),
        (800, 80),
    ],
)
def test_hue_normalization(value, expected):
    """Values are wrapped and/or converted appropriately."""
    color = hsl(h=value, s=0.5, l=0.5)
    actual = color.h
    assert isinstance(actual, int)
    assert actual == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0.5, 0.5),
        (1.0, 1.0),
        (1, 1.0),
        (-1, 0.0),
        (-100, 0.0),
        (10, 1.0),
        (Decimal(".2"), 0.2),
        (Fraction(3, 16), 0.1875),
    ],
)
@pytest.mark.parametrize(
    "constructor, attribute",
    [
        (rgb, "a"),
        (hsl, "s"),
        (hsl, "l"),
        (hsl, "a"),
    ],
)
def test_zero_to_one_normalization(value, expected, constructor, attribute):
    """Values are clipped and/or converted appropriately."""
    if constructor is rgb:
        args = {"r": 10, "g": 10, "b": 10}
    else:
        args = {"h": 10, "s": 0.5, "l": 0.5}

    args |= {attribute: value}
    color = constructor(**args)
    actual = getattr(color, attribute)
    assert isinstance(actual, float)
    assert actual == expected


@pytest.mark.parametrize(
    "color, attributes",
    [
        (rgb(10, 10, 10), ["r", "g", "b", "a", "rgb", "rgba", "hsl", "hsla"]),
        (hsl(10, 1, 1), ["h", "s", "l", "a", "rgb", "rgba", "hsl", "hsla"]),
    ],
)
def test_read_only(color, attributes):
    """A color's attributes cannot be changed."""
    for attribute in attributes:
        with pytest.raises(AttributeError):
            setattr(color, attribute, 0)
