from typing import Any
from unittest.mock import patch

import pytest

import toga
from toga.fonts import BOLD, ITALIC, OBLIQUE, SANS_SERIF, SMALL_CAPS, SYSTEM, Font

app_path = toga.App.app.paths.app


@pytest.fixture
async def widget() -> toga.Label:
    return toga.Label("hello, this is a label")


@patch("toga_gtk.fonts.Pango", None)
def test_no_pango():
    with pytest.raises(RuntimeError):
        Font(family=SANS_SERIF, size=14)


async def test_use_system_font_fallback(
    widget: toga.Label, widget_probe: Any, capsys: pytest.CaptureFixture[str]
):
    widget_probe.assert_font_family(SYSTEM)
    widget.style.font_family = "unknown"
    await widget_probe.redraw()

    assert "using system font as a fallback" in capsys.readouterr().out


@pytest.mark.parametrize("font_style", [ITALIC, OBLIQUE])
@pytest.mark.parametrize("font_variant", [SMALL_CAPS])
async def test_font_options(
    widget: toga.Label, widget_probe: Any, font_style: str, font_variant: str
):
    widget.style.font_style = font_style
    widget.style.font_variant = font_variant
    await widget_probe.redraw()

    assert widget_probe.font.style == font_style
    assert widget_probe.font.variant == font_variant


@pytest.mark.parametrize(
    "font_family,font_path,font_kwargs",
    [
        # OpenType font, no options
        (
            "Font Awesome 5 Free",
            "resources/fonts/Font Awesome 5 Free-Solid-900.otf",
            {},
        ),
        # TrueType font, no options
        ("ENDOR", "resources/fonts/ENDOR___.ttf", {}),
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
    widget: toga.Label, widget_probe: Any, font_family: str, font_path: str, font_kwargs
):
    Font.register(
        family=font_family,
        path=f"{app_path}/{font_path}",
        **font_kwargs,
    )

    # Update widget font family and other options if needed
    widget.style.font_family = font_family
    for prop, value in font_kwargs.items():
        widget.style.update(
            **{f"font_{kwarg}": value for kwarg, value in font_kwargs.items()}
        )
    await widget_probe.redraw()

    # Check that font properties are updated
    widget_probe.assert_font_family(font_family)
    for prop, value in font_kwargs.items():
        assert getattr(widget_probe.font, prop) == value


@pytest.mark.parametrize(
    "font_family,font_path",
    [
        # File does not exist
        ("nonexistent", "resources/fonts/nonexistent.ttf"),
        # File exists but is corrupted/wrong format
        ("Corrupted", "resources/fonts/Corrupted.ttf"),
    ],
)
async def test_font_file_not_loaded(
    widget: toga.Label, widget_probe: Any, font_family: str, font_path: str
):
    Font.register(family=font_family, path=f"{app_path.parent}/src/testbed/{font_path}")
    widget.style.font_family = font_family
    await widget_probe.redraw()
    widget_probe.assert_font_family == SYSTEM
