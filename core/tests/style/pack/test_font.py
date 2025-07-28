import pytest

from toga.style.pack import (
    BOLD,
    ITALIC,
    NORMAL,
    SANS_SERIF,
    SMALL_CAPS,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    Pack,
)


def assert_font(style, expected):
    # Test against retrieving the composite property
    assert style.font == expected

    # Also test against the underlying individual properties
    (font_style, font_variant, font_weight, font_size, font_family) = expected

    assert style.font_style == font_style
    assert style.font_variant == font_variant
    assert style.font_weight == font_weight
    assert style.font_size == font_size
    assert style.font_family == font_family


def test_default_values():
    """A blank Pack instance has the correct default values."""
    assert_font(Pack(), (NORMAL, NORMAL, NORMAL, SYSTEM_DEFAULT_FONT_SIZE, [SYSTEM]))


@pytest.mark.parametrize(
    "values",
    [
        (ITALIC, SMALL_CAPS, BOLD, 12, ["Comic Sans", SANS_SERIF]),
        # Should also work with optionals reordered
        (SMALL_CAPS, BOLD, ITALIC, 12, ["Comic Sans", SANS_SERIF]),
        (BOLD, SMALL_CAPS, ITALIC, 12, ["Comic Sans", SANS_SERIF]),
    ],
)
def test_assign_all_non_default(values):
    """Assigning all three optionals works, regardless of order."""
    style = Pack(font=values)

    assert_font(style, (ITALIC, SMALL_CAPS, BOLD, 12, ["Comic Sans", SANS_SERIF]))


ONE_NON_DEFAULT_PARAMS = pytest.mark.parametrize(
    "values",
    [
        # Full assignment, in order and out of order
        (NORMAL, SMALL_CAPS, NORMAL, 12, ["Comic Sans", SANS_SERIF]),
        (NORMAL, NORMAL, SMALL_CAPS, 12, ["Comic Sans", SANS_SERIF]),
        # Only the non-default
        (SMALL_CAPS, 12, ["Comic Sans", SANS_SERIF]),
        # One NORMAL
        (SMALL_CAPS, NORMAL, 12, ["Comic Sans", SANS_SERIF]),
        (NORMAL, SMALL_CAPS, 12, ["Comic Sans", SANS_SERIF]),
    ],
)


@ONE_NON_DEFAULT_PARAMS
def test_assign_one_non_default(values):
    """NORMAL values stay NORMAL when set explicitly or omitted, in any order"""
    style = Pack(font=values)

    assert_font(style, (NORMAL, SMALL_CAPS, NORMAL, 12, ["Comic Sans", SANS_SERIF]))


@ONE_NON_DEFAULT_PARAMS
def test_assign_one_non_default_after_setting(values):
    """Non-NORMAL optionals reset to when set explicitly or omitted, in any order."""
    style = Pack(font_weight=BOLD, font_style=ITALIC)
    style.font = values

    assert_font(style, (NORMAL, SMALL_CAPS, NORMAL, 12, ["Comic Sans", SANS_SERIF]))


@pytest.mark.parametrize(
    "value",
    [
        "Comic Sans",
        (NORMAL, SMALL_CAPS, NORMAL, 12, ["Comic Sans", SANS_SERIF], "extra"),
        None,
        12,
    ],
)
def test_assign_invalid_font(value):
    """Invalid assignment raises a TypeError."""
    with pytest.raises(
        TypeError,
        match=(
            r"Composite property 'font' assignment must provide 'font_size' and "
            r"'font_family', optionally preceded by 'font_style', 'font_variant', "
            r"and/or 'font_weight'\."
        ),
    ):
        _ = Pack(font=value)
