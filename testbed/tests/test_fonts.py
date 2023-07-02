from typing import Any

import pytest

import toga
from toga.fonts import (
    BOLD,
    FONT_STYLES,
    FONT_VARIANTS,
    FONT_WEIGHTS,
    ITALIC,
    SYSTEM,
    SYSTEM_DEFAULT_FONTS,
    Font,
)

from .conftest import skip_on_platforms


@pytest.fixture
async def widget() -> toga.Label:
    skip_on_platforms("android", "iOS")
    return toga.Label("hello, this is a label")


async def test_use_system_font_fallback(
    widget: toga.Label,
    widget_probe: Any,
    capsys: pytest.CaptureFixture[str],
):
    """If an unknown font is requested, the system font is used as a fallback."""
    widget_probe.assert_font_family(SYSTEM)
    widget.style.font_family = "unknown"
    await widget_probe.redraw("Falling back to system font")

    assert "using system font as a fallback" in capsys.readouterr().out


async def test_font_options(widget: toga.Label, widget_probe: Any):
    """Every combination of weight, style and variant can be used on a font."""
    for font_family in SYSTEM_DEFAULT_FONTS:
        for font_weight in FONT_WEIGHTS:
            for font_style in FONT_STYLES:
                for font_variant in FONT_VARIANTS:
                    widget.style.font_family = font_family
                    widget.style.font_style = font_style
                    widget.style.font_variant = font_variant
                    widget.style.font_weight = font_weight
                    await widget_probe.redraw(
                        f"Using a {font_family} {font_weight} {font_style} {font_variant} font"
                    )

                    widget_probe.assert_font_family(font_family)

                    widget_probe.assert_font_options(
                        font_weight, font_style, font_variant
                    )


@pytest.mark.parametrize(
    "font_family,font_path,font_kwargs",
    [
        # OpenType font, no options
        (
            "Font Awesome 5 Free Solid",
            "resources/fonts/Font Awesome 5 Free-Solid-900.otf",
            {},
        ),
        # TrueType font, no options
        ("Endor", "resources/fonts/ENDOR___.ttf", {}),
        # Font with weight property
        ("Roboto", "resources/fonts/Roboto-Bold.ttf", {"weight": BOLD}),
        # Font with style property
        ("Roboto", "resources/fonts/Roboto-Italic.ttf", {"style": ITALIC}),
        # Font with multiple properties
        (
            "Roboto",
            "resources/fonts/Roboto-BoldItalic.ttf",
            {"weight": BOLD, "style": ITALIC},
        ),
    ],
)
async def test_font_file_loaded(
    app: toga.App,
    widget: toga.Label,
    widget_probe: Any,
    font_family: str,
    font_path: str,
    font_kwargs,
    capsys: pytest.CaptureFixture[str],
):
    """Custom fonts can be loaded and used."""
    if not widget_probe.supports_custom_fonts:
        pytest.skip("Platform doesn't support registering and loading custom fonts")

    Font.register(
        family=font_family,
        path=app.paths.app / font_path,
        **font_kwargs,
    )

    # Update widget font family and other options if needed
    widget.style.font_family = font_family
    for prop, value in font_kwargs.items():
        widget.style.update(
            **{f"font_{kwarg}": value for kwarg, value in font_kwargs.items()}
        )
    await widget_probe.redraw(f"Using {font_family} {' '.join(font_kwargs.values())}")

    # Check that font properties are updated
    widget_probe.assert_font_family(font_family)
    for prop, value in font_kwargs.items():
        assert getattr(widget_probe.font, prop) == value

    # Ensure the font was actually loaded.
    stdout = capsys.readouterr().out

    # Setting the font to "Roboto something" involves setting the font to
    # "Roboto" as an intermediate step. However, we haven't registered "Roboto
    # regular", so this will raise an warning about the missing "regular" font.
    # Ignore this message.
    stdout = stdout.replace(
        "Unknown font 'Roboto default size'; using system font as a fallback\n",
        "",
    )

    assert "; using system font as a fallback" not in stdout
    assert "could not be found" not in stdout


async def test_non_existent_font_file(widget: toga.Label, app: toga.App):
    "Invalid font files fail registration"
    Font.register(
        family="non-existent",
        path=app.paths.app / "resources" / "fonts" / "nonexistent.ttf",
    )
    with pytest.raises(
        ValueError, match=r"Font file .*nonexistent.ttf could not be found"
    ):
        widget.style.font_family = "non-existent"


async def test_corrupted_font_file(
    widget: toga.Label,
    widget_probe: Any,
    app: toga.App,
):
    "Corrupted font files fail registration"
    if not widget_probe.supports_custom_fonts:
        pytest.skip("Platform doesn't support registering and loading custom fonts")

    Font.register(
        family="corrupted",
        path=app.paths.app / "resources" / "fonts" / "Corrupted.ttf",
    )
    with pytest.raises(ValueError, match=r"Unable to load font file .*Corrupted.ttf"):
        widget.style.font_family = "corrupted"
