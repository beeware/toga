from pathlib import Path

import pytest

import toga
from toga.fonts import (
    _REGISTERED_FONT_CACHE,
    BOLD,
    ITALIC,
    NORMAL,
    SANS_SERIF,
    SMALL_CAPS,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
)


@pytest.fixture
def app():
    return toga.App("Fonts Test", "org.beeware.toga.fonts")


@pytest.mark.parametrize(
    "family, size, weight, style, variant, as_str",
    [
        # No modifiers
        (
            SANS_SERIF,
            12,
            NORMAL,
            NORMAL,
            NORMAL,
            "sans-serif 12pt",
        ),
        # Weight modifier
        (
            SANS_SERIF,
            13,
            BOLD,
            NORMAL,
            NORMAL,
            "sans-serif 13pt bold",
        ),
        # Style modifier
        (
            SANS_SERIF,
            14,
            NORMAL,
            ITALIC,
            NORMAL,
            "sans-serif 14pt italic",
        ),
        # Variant modifier
        (
            SANS_SERIF,
            15,
            NORMAL,
            NORMAL,
            SMALL_CAPS,
            "sans-serif 15pt small-caps",
        ),
        # All modifiers
        (
            SANS_SERIF,
            37,
            BOLD,
            ITALIC,
            SMALL_CAPS,
            "sans-serif 37pt bold small-caps italic",
        ),
        # System font, fixed size
        (
            SYSTEM,
            42,
            NORMAL,
            NORMAL,
            NORMAL,
            "system 42pt",
        ),
        # Custom font, default size
        (
            "Custom Font",
            SYSTEM_DEFAULT_FONT_SIZE,
            NORMAL,
            NORMAL,
            NORMAL,
            "Custom Font default size",
        ),
        # System font, default size
        (
            SYSTEM,
            SYSTEM_DEFAULT_FONT_SIZE,
            NORMAL,
            NORMAL,
            NORMAL,
            "system default size",
        ),
    ],
)
def test_builtin_font(family, size, weight, style, variant, as_str):
    """A builtin font can be constructed."""
    font = toga.Font(
        family=family,
        size=size,
        style=style,
        weight=weight,
        variant=variant,
    )

    assert font.family == family
    assert font.size == size
    assert font.style == style
    assert font.weight == weight
    assert font.variant == variant
    assert str(font) == as_str


@pytest.mark.parametrize(
    "family, weight, style, variant, key",
    [
        ("Helvetica", NORMAL, NORMAL, NORMAL, ("Helvetica", NORMAL, NORMAL, NORMAL)),
        (
            "Times New Roman",
            BOLD,
            ITALIC,
            SMALL_CAPS,
            ("Times New Roman", BOLD, ITALIC, SMALL_CAPS),
        ),
        # Unknown style/weight/variants are normalized to "NORMAL"
        ("Wonky", "unknown", ITALIC, SMALL_CAPS, ("Wonky", NORMAL, ITALIC, SMALL_CAPS)),
        ("Wonky", BOLD, "unknown", SMALL_CAPS, ("Wonky", BOLD, NORMAL, SMALL_CAPS)),
        ("Wonky", BOLD, ITALIC, "unknown", ("Wonky", BOLD, ITALIC, NORMAL)),
    ],
)
def test_registered_font_key(app, family, style, weight, variant, key):
    """Registered font keys can be generated."""
    assert (
        toga.Font._registered_font_key(
            family, style=style, weight=weight, variant=variant
        )
        == key
    )


@pytest.mark.parametrize(
    "path, registered",
    [
        # Absolute path
        (Path("/path/to/custom/font.otf"), Path("/path/to/custom/font.otf")),
        (str(Path("/path/to/custom/font.otf")), Path("/path/to/custom/font.otf")),
        # Relative path
        (
            Path("path/to/custom/font.otf"),
            Path(toga.__file__).parent / "path/to/custom/font.otf",
        ),
        (
            "path/to/custom/font.otf",
            Path(toga.__file__).parent / "path/to/custom/font.otf",
        ),
    ],
)
def test_register_font(app, path, registered):
    """A custom font can be registered."""
    toga.Font.register("Custom Font", path)

    # Test fixture has paths in Path format; fully resolve for test comparison. This
    # gets around Windows path separator and absolute path discrepancies.
    assert (
        Path(_REGISTERED_FONT_CACHE[("Custom Font", NORMAL, NORMAL, NORMAL)]).resolve()
        == registered.resolve()
    )


@pytest.mark.parametrize(
    "path, registered",
    [
        # Absolute path
        (Path("/path/to/custom/font.otf"), Path("/path/to/custom/font.otf")),
        (str(Path("/path/to/custom/font.otf")), Path("/path/to/custom/font.otf")),
        # Relative path
        (
            Path("path/to/custom/font.otf"),
            Path(toga.__file__).parent / "path/to/custom/font.otf",
        ),
        (
            str(Path("path/to/custom/font.otf")),
            Path(toga.__file__).parent / "path/to/custom/font.otf",
        ),
    ],
)
def test_register_font_variant(app, path, registered):
    """A custom font can be registered as a variant."""
    toga.Font.register("Custom Font", path, weight=BOLD)

    # Test fixture has paths in Path format; fully resolve for test comparison. This
    # gets around Windows path separator and absolute path discrepancies.
    assert (
        Path(_REGISTERED_FONT_CACHE[("Custom Font", BOLD, NORMAL, NORMAL)]).resolve()
        == registered.resolve()
    )
