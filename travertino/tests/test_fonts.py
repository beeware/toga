import pytest

from travertino.constants import (
    ABSOLUTE_FONT_SIZES,
    BOLD,
    ITALIC,
    LARGE,
    LARGER,
    MEDIUM,
    NORMAL,
    OBLIQUE,
    RELATIVE_FONT_SIZES,
    SMALL,
    SMALL_CAPS,
    SMALLER,
    SYSTEM_DEFAULT_FONT_SIZE,
    X_LARGE,
    X_SMALL,
    XX_LARGE,
    XX_SMALL,
)
from travertino.fonts import Font


def assert_font(font, family, size, style, variant, weight):
    assert font.family == family
    assert font.size == size
    assert font.style == style
    assert font.variant == variant
    assert font.weight == weight


@pytest.mark.parametrize(
    "font",
    [
        Font("Comic Sans", "12 pt"),
        Font("Comic Sans", 12),
        Font("Comic Sans", 12, NORMAL, NORMAL, NORMAL),
    ],
)
def test_equality(font):
    assert font == Font("Comic Sans", "12 pt")


@pytest.mark.parametrize(
    "font",
    [
        Font("Comic Sans", 13),
        Font("Comic Sans", 12, ITALIC),
        Font("Times New Roman", 12, NORMAL, NORMAL, NORMAL),
        "a string",
        5,
    ],
)
def test_inqequality(font):
    assert font != Font("Comic Sans", "12 pt")


def test_hash():
    assert hash(Font("Comic Sans", 12)) == hash(Font("Comic Sans", 12))

    assert hash(Font("Comic Sans", 12, weight=BOLD)) != hash(Font("Comic Sans", 12))


@pytest.mark.parametrize(
    "size, kwargs, string",
    [
        (12, {}, "12pt"),
        (12, {"style": ITALIC}, "italic 12pt"),
        (12, {"style": ITALIC, "variant": SMALL_CAPS}, "italic small-caps 12pt"),
        (
            12,
            {"style": ITALIC, "variant": SMALL_CAPS, "weight": BOLD},
            "italic small-caps bold 12pt",
        ),
        (12, {"variant": SMALL_CAPS, "weight": BOLD}, "small-caps bold 12pt"),
        (12, {"weight": BOLD}, "bold 12pt"),
        (12, {"style": ITALIC, "weight": BOLD}, "italic bold 12pt"),
        # Check system default size handling
        (SYSTEM_DEFAULT_FONT_SIZE, {}, "system default size"),
        (SYSTEM_DEFAULT_FONT_SIZE, {"style": ITALIC}, "italic system default size"),
    ],
)
def test_repr(size, kwargs, string):
    assert repr(Font("Comic Sans", size, **kwargs)) == f"<Font: {string} Comic Sans>"


@pytest.mark.parametrize("size", [12, "12", "12pt", "12 pt"])
def test_simple_construction(size):
    assert_font(Font("Comic Sans", size), "Comic Sans", 12, NORMAL, NORMAL, NORMAL)


@pytest.mark.parametrize(
    "size",
    [
        XX_SMALL,
        X_SMALL,
        SMALL,
        MEDIUM,
        LARGE,
        X_LARGE,
        XX_LARGE,
        LARGER,
        SMALLER,
    ],
)
def test_css_font_size_keywords(size):
    font = Font("Comic Sans", size)
    assert_font(font, "Comic Sans", size, NORMAL, NORMAL, NORMAL)
    assert isinstance(font.size, str)
    assert font.size in ABSOLUTE_FONT_SIZES or font.size in RELATIVE_FONT_SIZES


@pytest.mark.parametrize(
    "size, expected_repr",
    [
        (XX_SMALL, "<Font: xx-small Comic Sans>"),
        (X_SMALL, "<Font: x-small Comic Sans>"),
        (SMALL, "<Font: small Comic Sans>"),
        (MEDIUM, "<Font: medium Comic Sans>"),
        (LARGE, "<Font: large Comic Sans>"),
        (X_LARGE, "<Font: x-large Comic Sans>"),
        (XX_LARGE, "<Font: xx-large Comic Sans>"),
        (LARGER, "<Font: larger Comic Sans>"),
        (SMALLER, "<Font: smaller Comic Sans>"),
    ],
)
def test_css_font_size_repr(size, expected_repr):
    font = Font("Comic Sans", size)
    assert repr(font) == expected_repr


def test_invalid_construction():
    with pytest.raises(ValueError):
        Font("Comic Sans", "12 quatloos")

    with pytest.raises(ValueError):
        Font("Comic Sans", "invalid-size")

    with pytest.raises(ValueError):
        Font("Comic Sans", "")

    try:
        Font("Comic Sans", None)
        assert False, "Should have raised TypeError"
    except TypeError:
        pass


@pytest.mark.parametrize(
    "family",
    [
        "Comics Sans",
        "Wingdings",
        "'Comic Sans'",
        '"Comic Sans"',
    ],
)
def test_family(family):
    normalized_family = family.replace("'", "").replace('"', "")
    assert_font(Font(family, 12), normalized_family, 12, NORMAL, NORMAL, NORMAL)


@pytest.mark.parametrize(
    "style, result_style",
    [
        (ITALIC, ITALIC),
        ("italic", ITALIC),
        (OBLIQUE, OBLIQUE),
        ("oblique", OBLIQUE),
        ("something else", NORMAL),
    ],
)
def test_style(style, result_style):
    assert_font(
        Font("Comic Sans", 12, style=style),
        "Comic Sans",
        12,
        result_style,
        NORMAL,
        NORMAL,
    )


@pytest.mark.parametrize(
    "kwargs",
    [
        {},
        {"style": ITALIC},
    ],
)
def test_make_normal_style(kwargs):
    f = Font("Comic Sans", 12, **kwargs)
    assert_font(f.normal_style(), "Comic Sans", 12, NORMAL, NORMAL, NORMAL)


@pytest.mark.parametrize(
    "method, result",
    [
        ("italic", ITALIC),
        ("oblique", OBLIQUE),
    ],
)
def test_make_slanted(method, result):
    f = Font("Comic Sans", 12)
    assert_font(getattr(f, method)(), "Comic Sans", 12, result, NORMAL, NORMAL)


@pytest.mark.parametrize(
    "variant, result",
    [
        (SMALL_CAPS, SMALL_CAPS),
        ("small-caps", SMALL_CAPS),
        ("something else", NORMAL),
    ],
)
def test_variant(variant, result):
    assert_font(
        Font("Comic Sans", 12, variant=variant),
        "Comic Sans",
        12,
        NORMAL,
        result,
        NORMAL,
    )


@pytest.mark.parametrize("kwargs", [{}, {"variant": SMALL_CAPS}])
def test_make_normal_variant(kwargs):
    f = Font("Comic Sans", 12, **kwargs)
    assert_font(f.normal_variant(), "Comic Sans", 12, NORMAL, NORMAL, NORMAL)


def test_make_small_caps():
    f = Font("Comic Sans", 12)
    assert_font(f.small_caps(), "Comic Sans", 12, NORMAL, SMALL_CAPS, NORMAL)


@pytest.mark.parametrize(
    "weight, result",
    [
        (BOLD, BOLD),
        ("bold", BOLD),
        ("something else", NORMAL),
    ],
)
def test_weight(weight, result):
    assert_font(
        Font("Comic Sans", 12, weight=weight),
        "Comic Sans",
        12,
        NORMAL,
        NORMAL,
        result,
    )


@pytest.mark.parametrize("kwargs", [{}, {"weight": BOLD}])
def test_make_normal_weight(kwargs):
    f = Font("Comic Sans", 12, **kwargs)
    assert_font(f.normal_weight(), "Comic Sans", 12, NORMAL, NORMAL, NORMAL)


def test_make_bold():
    f = Font("Comic Sans", 12)
    assert_font(f.bold(), "Comic Sans", 12, NORMAL, NORMAL, BOLD)
