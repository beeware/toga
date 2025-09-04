import pytest

from travertino.colors import hsl, rgb

from ..utils import assert_equal_color


@pytest.mark.parametrize(
    "color, method",
    [
        (rgb(10, 20, 30), "rgb"),
        (hsl(120, 0.5, 0.5), "hsl"),
    ],
)
def test_conversion_noop(color, method):
    """rgb.rgb and hsl.hsl return the original color."""
    assert getattr(color, method) is color
    assert getattr(color, f"{method}a") is color


@pytest.mark.parametrize(
    "color, method",
    [
        (rgb(10, 20, 30), "hsl"),
        (hsl(120, 0.5, 0.5), "rgb"),
    ],
)
def test_conversion_caching(color, method):
    """Conversions (hsl.rgb and rgb.hsl) are cached after first call."""
    assert getattr(color, method) is getattr(color, method)
    assert getattr(color, f"{method}a") is getattr(color, f"{method}a")
    assert getattr(color, method) is getattr(color, f"{method}a")


equivalent_colors = pytest.mark.parametrize(
    "rgb_color, hsl_color",
    [
        # Black, gray, white,
        (rgb(0, 0, 0, 0), hsl(0, 0, 0, 0)),
        (rgb(0, 0, 0, 1.0), hsl(0, 0, 0, 1)),
        (rgb(128, 128, 128, 1.0), hsl(0, 0, 0.502, 1)),
        (rgb(255, 255, 255, 1.0), hsl(0, 0, 1, 1)),
        # Primaries
        (rgb(255, 0, 0, 1.0), hsl(0, 1, 0.5, 1)),
        (rgb(0, 255, 0, 1.0), hsl(120, 1, 0.5, 1)),
        (rgb(0, 0, 255, 1.0), hsl(240, 1, 0.5, 1)),
        # Color with different channel values, including transparency
        (rgb(50, 128, 200, 0.0), hsl(209, 0.6, 0.4902, 0)),
        (rgb(50, 128, 200, 0.5), hsl(209, 0.6, 0.4902, 0.5)),
        (rgb(50, 128, 200, 0.9), hsl(209, 0.6, 0.4902, 0.9)),
        (rgb(50, 128, 200, 1.0), hsl(209, 0.6, 0.4902, 1)),
        # Color having intermediate alpha values
        (rgb(100, 201, 255, 0.15), hsl(201, 1, 0.6961, 0.15)),
        (rgb(120, 180, 240, 0.2), hsl(210, 0.8, 0.7059, 0.2)),
        (rgb(150, 50, 100, 0.4), hsl(330, 0.5, 0.3922, 0.4)),
        (rgb(50, 60, 70, 0.55), hsl(210, 0.1667, 0.2353, 0.55)),
        (rgb(255, 255, 0, 0.3), hsl(60, 1, 0.5, 0.3)),
        # The following were transferred over from what used to be test_hsl in
        # test_constructor.py:
        # Blacks
        (rgb(0x00, 0x00, 0x00), hsl(0, 0.0, 0.0)),
        (rgb(0x00, 0x00, 0x00), hsl(60, 0.0, 0.0)),
        (rgb(0x00, 0x00, 0x00), hsl(180, 0.0, 0.0)),
        (rgb(0x00, 0x00, 0x00), hsl(240, 0.0, 0.0)),
        (rgb(0x00, 0x00, 0x00), hsl(360, 0.0, 0.0)),
        # Whites
        (rgb(0xFF, 0xFF, 0xFF), hsl(0, 0.0, 1.0)),
        (rgb(0xFF, 0xFF, 0xFF), hsl(60, 0.0, 1.0)),
        (rgb(0xFF, 0xFF, 0xFF), hsl(180, 0.0, 1.0)),
        (rgb(0xFF, 0xFF, 0xFF), hsl(240, 0.0, 1.0)),
        (rgb(0xFF, 0xFF, 0xFF), hsl(360, 0.0, 1.0)),
        # Grays
        (rgb(0x33, 0x33, 0x33), hsl(0, 0.0, 0.2)),
        (rgb(0x66, 0x66, 0x66), hsl(0, 0.0, 0.4)),
        (rgb(0x80, 0x80, 0x80), hsl(0, 0.0, 0.502)),
        (rgb(0x99, 0x99, 0x99), hsl(0, 0.0, 0.6)),
        (rgb(0xCC, 0xCC, 0xCC), hsl(0, 0.0, 0.8)),
        # Primaries
        (rgb(0xFF, 0x00, 0x00), hsl(0, 1.0, 0.5)),
        (rgb(0xFF, 0x80, 0x00), hsl(30, 1.0, 0.5)),
        (rgb(0xFF, 0xFF, 0x00), hsl(60, 1.0, 0.5)),
        (rgb(0x80, 0xFF, 0x00), hsl(90, 1.0, 0.5)),
        (rgb(0x00, 0xFF, 0x00), hsl(120, 1.0, 0.5)),
        (rgb(0x00, 0xFF, 0x80), hsl(150, 1.0, 0.5)),
        (rgb(0x00, 0xFF, 0xFF), hsl(180, 1.0, 0.5)),
        (rgb(0x00, 0x80, 0xFF), hsl(210, 1.0, 0.5)),
        (rgb(0x00, 0x00, 0xFF), hsl(240, 1.0, 0.5)),
        (rgb(0x80, 0x00, 0xFF), hsl(270, 1.0, 0.5)),
        (rgb(0xFF, 0x00, 0xFF), hsl(300, 1.0, 0.5)),
        (rgb(0xFF, 0x00, 0x80), hsl(330, 1.0, 0.5)),
        (rgb(0xFF, 0x00, 0x00), hsl(360, 1.0, 0.5)),
        # Muted
        (rgb(0x50, 0x30, 0x30), hsl(0, 0.25, 0.25)),
        (rgb(0x50, 0x40, 0x30), hsl(30, 0.25, 0.25)),
        (rgb(0x50, 0x50, 0x30), hsl(60, 0.25, 0.25)),
        (rgb(0x40, 0x50, 0x30), hsl(90, 0.25, 0.25)),
        (rgb(0x30, 0x50, 0x30), hsl(120, 0.25, 0.25)),
        (rgb(0x30, 0x50, 0x40), hsl(150, 0.25, 0.25)),
        (rgb(0x30, 0x50, 0x50), hsl(180, 0.25, 0.25)),
        (rgb(0x30, 0x40, 0x50), hsl(210, 0.25, 0.25)),
        (rgb(0x30, 0x30, 0x50), hsl(240, 0.25, 0.25)),
        (rgb(0x40, 0x30, 0x50), hsl(270, 0.25, 0.25)),
        (rgb(0x50, 0x30, 0x50), hsl(300, 0.25, 0.25)),
        (rgb(0x50, 0x30, 0x40), hsl(330, 0.25, 0.25)),
        (rgb(0x50, 0x30, 0x30), hsl(360, 0.25, 0.25)),
        (rgb(0xCF, 0xAF, 0xAF), hsl(0, 0.25, 0.75)),
        (rgb(0xCF, 0xBF, 0xAF), hsl(30, 0.25, 0.75)),
        (rgb(0xCF, 0xCF, 0xAF), hsl(60, 0.25, 0.75)),
        (rgb(0xBF, 0xCF, 0xAF), hsl(90, 0.25, 0.75)),
        (rgb(0xAF, 0xCF, 0xAF), hsl(120, 0.25, 0.75)),
        (rgb(0xAF, 0xCF, 0xBF), hsl(150, 0.25, 0.75)),
        (rgb(0xAF, 0xCF, 0xCF), hsl(180, 0.25, 0.75)),
        (rgb(0xAF, 0xBF, 0xCF), hsl(210, 0.25, 0.75)),
        (rgb(0xAF, 0xAF, 0xCF), hsl(240, 0.25, 0.75)),
        (rgb(0xBF, 0xAF, 0xCF), hsl(270, 0.25, 0.75)),
        (rgb(0xCF, 0xAF, 0xCF), hsl(300, 0.25, 0.75)),
        (rgb(0xCF, 0xAF, 0xBF), hsl(330, 0.25, 0.75)),
        (rgb(0xCF, 0xAF, 0xAF), hsl(360, 0.25, 0.75)),
        (rgb(0xEF, 0x8F, 0x8F), hsl(0, 0.75, 0.75)),
        (rgb(0xEF, 0xBF, 0x8F), hsl(30, 0.75, 0.75)),
        (rgb(0xEF, 0xEF, 0x8F), hsl(60, 0.75, 0.75)),
        (rgb(0xBF, 0xEF, 0x8F), hsl(90, 0.75, 0.75)),
        (rgb(0x8F, 0xEF, 0x8F), hsl(120, 0.75, 0.75)),
        (rgb(0x8F, 0xEF, 0xBF), hsl(150, 0.75, 0.75)),
        (rgb(0x8F, 0xEF, 0xEF), hsl(180, 0.75, 0.75)),
        (rgb(0x8F, 0xBF, 0xEF), hsl(210, 0.75, 0.75)),
        (rgb(0x8F, 0x8F, 0xEF), hsl(240, 0.75, 0.75)),
        (rgb(0xBF, 0x8F, 0xEF), hsl(270, 0.75, 0.75)),
        (rgb(0xEF, 0x8F, 0xEF), hsl(300, 0.75, 0.75)),
        (rgb(0xEF, 0x8F, 0xBF), hsl(330, 0.75, 0.75)),
        (rgb(0xEF, 0x8F, 0x8F), hsl(360, 0.75, 0.75)),
        (rgb(0x70, 0x10, 0x10), hsl(0, 0.75, 0.25)),
        (rgb(0x70, 0x40, 0x10), hsl(30, 0.75, 0.25)),
        (rgb(0x70, 0x70, 0x10), hsl(60, 0.75, 0.25)),
        (rgb(0x40, 0x70, 0x10), hsl(90, 0.75, 0.25)),
        (rgb(0x10, 0x70, 0x10), hsl(120, 0.75, 0.25)),
        (rgb(0x10, 0x70, 0x40), hsl(150, 0.75, 0.25)),
        (rgb(0x10, 0x70, 0x70), hsl(180, 0.75, 0.25)),
        (rgb(0x10, 0x40, 0x70), hsl(210, 0.75, 0.25)),
        (rgb(0x10, 0x10, 0x70), hsl(240, 0.75, 0.25)),
        (rgb(0x40, 0x10, 0x70), hsl(270, 0.75, 0.25)),
        (rgb(0x70, 0x10, 0x70), hsl(300, 0.75, 0.25)),
        (rgb(0x70, 0x10, 0x40), hsl(330, 0.75, 0.25)),
        (rgb(0x70, 0x10, 0x10), hsl(360, 0.75, 0.25)),
        # With alpha
        (rgb(0x00, 0x00, 0x00, 0.3), hsl(60, 0.0, 0.0, 0.3)),
        (rgb(0xFF, 0xFF, 0xFF, 0.3), hsl(60, 0.0, 1.0, 0.3)),
        (rgb(0xFF, 0xFF, 0x00, 0.3), hsl(60, 1.0, 0.5, 0.3)),
        (rgb(0x50, 0x50, 0x30, 0.3), hsl(60, 0.25, 0.25, 0.3)),
        (rgb(0xCF, 0xCF, 0xAF, 0.3), hsl(60, 0.25, 0.75, 0.3)),
        (rgb(0xEF, 0xEF, 0x8F, 0.3), hsl(60, 0.75, 0.75, 0.3)),
        (rgb(0x70, 0x70, 0x10, 0.3), hsl(60, 0.75, 0.25, 0.3)),
    ],
)


@equivalent_colors
def test_rgb_to_hsl(rgb_color, hsl_color):
    """An rgb color can be converted to hsl."""
    assert_equal_color(rgb_color.hsl, hsl_color, abs=1e-3)


@equivalent_colors
def test_hsl_to_rgb(rgb_color, hsl_color):
    """An hsl color can be converted to rgb."""
    assert_equal_color(hsl_color.rgb, rgb_color)
