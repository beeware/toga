import pytest

from travertino.constants import (
    BOLD,
    ITALIC,
    NORMAL,
    OBLIQUE,
    SMALL_CAPS,
    SYSTEM_DEFAULT_FONT_SIZE,
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


def test_invalid_construction():
    with pytest.raises(ValueError):
        Font("Comic Sans", "12 quatloos")


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
