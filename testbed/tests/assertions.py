from pytest import approx

from toga.colors import TRANSPARENT
from toga.fonts import (
    CURSIVE,
    FANTASY,
    MONOSPACE,
    SANS_SERIF,
    SERIF,
    SYSTEM,
)


def assert_color(actual, expected):
    if expected in {None, TRANSPARENT}:
        assert expected == actual
    else:
        if actual in {None, TRANSPARENT}:
            assert expected == actual
        else:
            assert (actual.r, actual.g, actual.b, actual.a) == (
                expected.r,
                expected.g,
                expected.b,
                approx(expected.a, abs=(1 / 255)),
            )


GENERIC_FONTS = {
    CURSIVE: ["Apple Chancery"],
    FANTASY: ["Papyrus"],
    MONOSPACE: ["Courier New"],
    SANS_SERIF: ["Helvetica"],
    SERIF: ["Times", "Times New Roman"],
    SYSTEM: [
        SANS_SERIF,
        ".AppleSystemUIFont",
        "sans-serif-medium",  # Android buttons
    ],
}


def assert_font_family(actual, expected):
    assert actual in ([expected] + GENERIC_FONTS.get(expected, []))
