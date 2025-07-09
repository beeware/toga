from importlib import import_module

import pytest

import toga
from toga.fonts import (
    BOLD,
    FONT_STYLES,
    FONT_VARIANTS,
    FONT_WEIGHTS,
    ITALIC,
    MESSAGE,
    SANS_SERIF,
    SERIF,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    SYSTEM_DEFAULT_FONTS,
    Font,
)


# Fully testing fonts requires a manifested widget.
@pytest.fixture
async def widget():
    return toga.Label("This is a font test")


@pytest.fixture
async def font_probe(main_window, widget):
    box = toga.Box(children=[widget])
    main_window.content = box

    module = import_module("tests_backend.widgets.label")
    probe = module.LabelProbe(widget)
    await probe.redraw("\nConstructing Font probe")
    probe.assert_container(box)

    yield probe

    main_window.content = toga.Box()


async def test_use_system_font_fallback(
    widget: toga.Label,
    font_probe,
    capsys: pytest.CaptureFixture[str],
):
    """If an unknown font is requested, the system font is used as a fallback."""
    font_probe.assert_font_family(SYSTEM)
    widget.style.font_family = "unknown"
    await font_probe.redraw("Falling back to system font")

    assert "using system font as a fallback" in capsys.readouterr().out


@pytest.mark.parametrize(
    "family, result, custom",
    [
        ([SERIF, SANS_SERIF, MESSAGE], SERIF, False),
        (["Bogus", SANS_SERIF, SERIF], SANS_SERIF, False),
        ([MESSAGE, "Bogus", SERIF], MESSAGE, False),
        (["Bogus", "Missing"], SYSTEM, False),
        (["Endor", SERIF, "Bogus"], "Endor", True),
        (["Bogus", "Endor"], "Endor", True),
        ([SERIF, "Endor"], SERIF, True),
    ],
)
async def test_use_first_valid_font(
    app,
    widget: toga.Label,
    font_probe,
    family,
    result,
    custom,
):
    """The widget should get the first valid font."""
    if custom:
        if not font_probe.supports_custom_fonts:
            pytest.skip("Platform doesn't support registering and loading custom fonts")

        Font.register("Endor", path=app.paths.app / "resources/fonts/ENDOR___.ttf")

    widget.style.font_family = family
    await font_probe.redraw(f"Font family should be {result}")
    font_probe.assert_font_family(result)


async def test_font_options(widget: toga.Label, font_probe):
    """Every combination of weight, style and variant can be used on a font."""
    for font_family in SYSTEM_DEFAULT_FONTS:
        for font_size in [20, SYSTEM_DEFAULT_FONT_SIZE]:
            for font_weight in FONT_WEIGHTS:
                for font_style in FONT_STYLES:
                    for font_variant in FONT_VARIANTS:
                        widget.style.font_family = font_family
                        widget.style.font_size = font_size
                        widget.style.font_style = font_style
                        widget.style.font_variant = font_variant
                        widget.style.font_weight = font_weight
                        await font_probe.redraw(
                            f"Using a {font_family} {font_size} {font_weight} "
                            f"{font_style} {font_variant} font"
                        )

                        font_probe.assert_font_family(font_family)
                        font_probe.assert_font_size(font_size)
                        font_probe.assert_font_options(
                            font_weight, font_style, font_variant
                        )


@pytest.mark.parametrize(
    "font_family,font_path,font_kwargs,variable_font_test",
    [
        # OpenType font with weight property
        (
            "Font Awesome 5 Free Solid",
            "resources/fonts/Font Awesome 5 Free-Solid-900.otf",
            {"weight": BOLD},
            False,
        ),
        # TrueType font supporting multiple styles, no options
        ("Endor", "resources/fonts/ENDOR___.ttf", {}, False),
        # TrueType font supporting multiple styles, with options
        ("Endor", "resources/fonts/ENDOR___.ttf", {"weight": BOLD}, True),
        # Font with weight property
        ("Roboto", "resources/fonts/Roboto-Bold.ttf", {"weight": BOLD}, False),
        # Font with style property
        ("Roboto", "resources/fonts/Roboto-Italic.ttf", {"style": ITALIC}, False),
        # Font with multiple properties
        (
            "Roboto",
            "resources/fonts/Roboto-BoldItalic.ttf",
            {"weight": BOLD, "style": ITALIC},
            False,
        ),
    ],
)
async def test_font_file_loaded(
    app: toga.App,
    widget: toga.Label,
    font_probe,
    font_family: str,
    font_path: str,
    font_kwargs,
    variable_font_test: bool,
    capsys: pytest.CaptureFixture[str],
):
    """Custom fonts can be loaded and used."""
    if not font_probe.supports_custom_fonts:
        pytest.skip("Platform doesn't support loading custom fonts")

    Font.register(
        family=font_family,
        path=app.paths.app / font_path,
        **font_kwargs,
    )

    # Update widget font family and other options if needed
    widget.style |= {
        "font_family": font_family,
        **{f"font_{kwarg}": value for kwarg, value in font_kwargs.items()},
    }
    await font_probe.redraw(f"Using {font_family} {' '.join(font_kwargs.values())}")

    # Check that font properties are updated
    font_probe.assert_font_family(font_family)
    # Only check the font options if this is a non-variable font test, or the backend
    # supports variable fonts
    if not variable_font_test or font_probe.supports_custom_variable_fonts:
        font_probe.assert_font_options(**font_kwargs)

    assert "; using system font as a fallback" not in capsys.readouterr().out


async def test_non_existent_font_file(widget: toga.Label, app: toga.App, font_probe):
    """Invalid font files fail registration."""
    if not font_probe.supports_custom_fonts:
        pytest.skip("Platform doesn't support loading custom fonts")

    Font.register(
        family="non-existent",
        path=app.paths.app / "resources/fonts/nonexistent.ttf",
    )
    with pytest.raises(
        ValueError, match=r"Font file .*nonexistent.ttf could not be found"
    ):
        widget.style.font_family = "non-existent"


async def test_corrupted_font_file(
    widget: toga.Label,
    font_probe,
    app: toga.App,
):
    """Corrupted font files fail registration."""
    if not font_probe.supports_custom_fonts:
        pytest.skip("Platform doesn't support registering and loading custom fonts")

    Font.register(
        family="corrupted",
        path=app.paths.app / "resources/fonts/Corrupted.ttf",
    )
    with pytest.raises(ValueError, match=r"Unable to load font file .*Corrupted.ttf"):
        widget.style.font_family = "corrupted"


async def test_arbitrary_system_font(widget: toga.Label, font_probe):
    """An arbitrary font installed on the system can be used."""
    family = font_probe.preinstalled_font()
    widget.font_family = family
    font_probe.assert_font_family(family)
