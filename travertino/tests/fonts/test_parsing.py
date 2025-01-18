import pytest

from tests.fonts.test_constructor import assert_font
from travertino.constants import (
    BOLD,
    ITALIC,
    NORMAL,
    OBLIQUE,
    SMALL_CAPS,
)
from travertino.fonts import Font, font


def test_font_instance():
    f = Font("Comic Sans", 12)

    parsed = font(f)

    assert f == parsed
    assert f is parsed


@pytest.mark.parametrize(
    "string, style, variant, weight",
    [
        ("12pt Comic Sans", NORMAL, NORMAL, NORMAL),
        ("italic 12pt Comic Sans", ITALIC, NORMAL, NORMAL),
        ("italic small-caps 12pt Comic Sans", ITALIC, SMALL_CAPS, NORMAL),
        ("italic small-caps bold 12pt Comic Sans", ITALIC, SMALL_CAPS, BOLD),
        ("small-caps bold 12pt Comic Sans", NORMAL, SMALL_CAPS, BOLD),
        ("italic bold 12 pt Comic Sans", ITALIC, NORMAL, BOLD),
        ("bold 12 pt Comic Sans", NORMAL, NORMAL, BOLD),
    ],
)
def test_successful_combinations(string, style, variant, weight):
    assert_font(font(string), "Comic Sans", 12, style, variant, weight)


@pytest.mark.parametrize(
    "string",
    [
        "12pt Comic Sans",
        "12 pt Comic Sans",
        "12 Comic Sans",
    ],
)
def test_font_sizes(string):
    assert_font(font(string), "Comic Sans", 12, NORMAL, NORMAL, NORMAL)


def test_invalid_size():
    with pytest.raises(ValueError):
        font("12quatloo Comic Sans")


@pytest.mark.parametrize("string", ["12pt 'Comic Sans'", '12pt "Comic Sans"'])
def test_font_family(string):
    assert_font(font(string), "Comic Sans", 12, NORMAL, NORMAL, NORMAL)


@pytest.mark.parametrize(
    "string, style, variant",
    [
        ("normal 12pt Comic Sans", NORMAL, NORMAL),
        ("italic normal 12pt Comic Sans", ITALIC, NORMAL),
        ("italic small-caps normal 12pt Comic Sans", ITALIC, SMALL_CAPS),
    ],
)
def test_normal(string, style, variant):
    assert_font(font(string), "Comic Sans", 12, style, variant, NORMAL)


@pytest.mark.parametrize(
    "string, style",
    [
        ("italic 12pt Comic Sans", ITALIC),
        ("oblique 12pt Comic Sans", OBLIQUE),
    ],
)
def test_style(string, style):
    assert_font(font(string), "Comic Sans", 12, style, NORMAL, NORMAL)


def test_invalid_style():
    with pytest.raises(ValueError):
        font("wiggly small-caps bold 12pt Comic Sans")


def test_variant():
    assert_font(
        font("italic small-caps 12pt Comic Sans"),
        "Comic Sans",
        12,
        ITALIC,
        SMALL_CAPS,
        NORMAL,
    )

    with pytest.raises(ValueError):
        font("italic wiggly bold 12pt Comic Sans")


def test_weight():
    assert_font(
        font("italic small-caps bold 12pt Comic Sans"),
        "Comic Sans",
        12,
        ITALIC,
        SMALL_CAPS,
        BOLD,
    )

    with pytest.raises(ValueError):
        font("italic small-caps wiggly 12pt Comic Sans")


@pytest.mark.parametrize(
    "string",
    [
        "oblique italic 12pt Comic Sans",
        "italic small-caps oblique 12pt Comic Sans",
        "italic small-caps bold small-caps 12pt Comic Sans",
        "bold bold 12pt Comic Sans",
    ],
)
def test_duplicates(string):
    with pytest.raises(ValueError):
        font(string)


def test_invaid():
    with pytest.raises(ValueError):
        font(42)
