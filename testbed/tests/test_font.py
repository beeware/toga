import sys
from pathlib import Path
from typing import Any

import pytest

import toga
from toga.fonts import BOLD, ITALIC, SYSTEM, Font

from .conftest import skip_on_platforms


@pytest.fixture
async def widget() -> toga.Label:
    skip_on_platforms("android", "iOS", "macOS")
    return toga.Label("hello, this is a label")


@pytest.fixture
async def app_path(app):
    # This *should* be app.paths.app, but under test conditions,
    # the mainline is the test module, which confuses the app path.
    return Path(sys.modules[app.__module__].__file__).parent


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
    for font_weight in widget_probe.FONT_WEIGHTS:
        for font_style in widget_probe.FONT_STYLES:
            for font_variant in widget_probe.FONT_VARIANTS:
                widget.style.font_style = font_style
                widget.style.font_variant = font_variant
                widget.style.font_weight = font_weight
                await widget_probe.redraw(
                    f"Using a {font_weight} {font_style} {font_variant} font"
                )

                assert widget_probe.font.weight == font_weight
                assert widget_probe.font.style == font_style
                assert widget_probe.font.variant == font_variant


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
    widget: toga.Label,
    widget_probe: Any,
    font_family: str,
    font_path: str,
    font_kwargs,
    capsys: pytest.CaptureFixture[str],
    app_path: Path,
):
    """Custom fonts can be loaded and used."""
    Font.register(
        family=font_family,
        path=app_path / font_path,
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
    assert "could not be found" not in capsys.readouterr().out


async def test_non_existent_font_file(widget: toga.Label, app_path: Path):
    "Invalid font files fail registration"
    Font.register(
        family="non-existent",
        path=app_path / "resources" / "fonts" / "nonexistent.ttf",
    )
    with pytest.raises(
        ValueError, match=r"Font file .*nonexistent.ttf could not be found"
    ):
        widget.style.font_family = "non-existent"


async def test_corrupted_font_file(widget: toga.Label, app_path: Path):
    "Corrupted font files fail registration"
    Font.register(
        family="corrupted",
        path=app_path / "resources" / "fonts" / "Corrupted.ttf",
    )
    with pytest.raises(ValueError, match=r"Unable to load font file .*Corrupted.ttf"):
        widget.style.font_family = "corrupted"
