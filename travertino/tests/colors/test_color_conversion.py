import pytest

from travertino.colors import hsl, hsla, rgb, rgba

from ..utils import assert_equal_color


@pytest.mark.parametrize(
    "input_color, expected_color",
    [
        # Black, gray, white,
        (rgba(0, 0, 0, 0), rgb(0, 0, 0)),
        (rgba(0, 0, 0, 1.0), rgb(0, 0, 0)),
        (rgba(128, 128, 128, 1.0), rgb(128, 128, 128)),
        (rgba(255, 255, 255, 1.0), rgb(255, 255, 255)),
        # Primaries
        (rgba(255, 0, 0, 1.0), rgb(255, 0, 0)),
        (rgba(0, 255, 0, 1.0), rgb(0, 255, 0)),
        (rgba(0, 0, 255, 1.0), rgb(0, 0, 255)),
        # Color with different channel values, including transparency
        (rgba(50, 128, 200, 0.0), rgb(50, 128, 200)),
        (rgba(50, 128, 200, 0.5), rgb(50, 128, 200)),
        (rgba(50, 128, 200, 0.9), rgb(50, 128, 200)),
        (rgba(50, 128, 200, 1.0), rgb(50, 128, 200)),
        # Color having intermediate alpha values
        (rgba(100, 200, 255, 0.15), rgb(100, 200, 255)),
        (rgba(120, 180, 240, 0.2), rgb(120, 180, 240)),
        (rgba(150, 50, 100, 0.4), rgb(150, 50, 100)),
        (rgba(50, 60, 70, 0.55), rgb(50, 60, 70)),
        (rgba(255, 255, 0, 0.3), rgb(255, 255, 0)),
    ],
)
def test_rgba_to_rgb(input_color, expected_color):
    """A rgba color can be converted to rgb."""
    assert_equal_color(input_color.rgb, expected_color)


@pytest.mark.parametrize(
    "input_color, expected_color",
    [
        # Black, gray, white,
        (rgba(0, 0, 0, 0), hsla(0, 0, 0, 0)),
        (rgba(0, 0, 0, 1.0), hsla(0, 0, 0, 1)),
        (rgba(128, 128, 128, 1.0), hsla(0, 0, 0.502, 1)),
        (rgba(255, 255, 255, 1.0), hsla(0, 0, 1, 1)),
        # Primaries
        (rgba(255, 0, 0, 1.0), hsla(0, 1, 0.5, 1)),
        (rgba(0, 255, 0, 1.0), hsla(120.0, 1, 0.5, 1)),
        (rgba(0, 0, 255, 1.0), hsla(240.0, 1, 0.5, 1)),
        # Color with different channel values, including transparency
        (rgba(50, 128, 200, 0.0), hsla(208.8, 0.6, 0.4902, 0)),
        (rgba(50, 128, 200, 0.5), hsla(208.8, 0.6, 0.4902, 0.5)),
        (rgba(50, 128, 200, 0.9), hsla(208.8, 0.6, 0.4902, 0.9)),
        (rgba(50, 128, 200, 1.0), hsla(208.8, 0.6, 0.4902, 1)),
        # Color having intermediate alpha values
        (rgba(100, 200, 255, 0.15), hsla(201.2903, 1, 0.6961, 0.15)),
        (rgba(120, 180, 240, 0.2), hsla(210.0, 0.8, 0.7059, 0.2)),
        (rgba(150, 50, 100, 0.4), hsla(330.0, 0.5, 0.3922, 0.4)),
        (rgba(50, 60, 70, 0.55), hsla(210.0, 0.1667, 0.2353, 0.55)),
        (rgba(255, 255, 0, 0.3), hsla(60.0, 1, 0.5, 0.3)),
    ],
)
def test_rgba_to_hsla(input_color, expected_color):
    """A rgba color can be converted to hsla."""
    assert_equal_color(input_color.hsla, expected_color, abs=1e-4)


@pytest.mark.parametrize(
    "input_color, expected_color",
    [
        # Black, gray, white,
        (rgba(0, 0, 0, 0), hsl(0, 0, 0)),
        (rgba(0, 0, 0, 1.0), hsl(0, 0, 0)),
        (rgba(128, 128, 128, 1.0), hsl(0, 0, 0.502)),
        (rgba(255, 255, 255, 1.0), hsl(0, 0, 1)),
        # Primaries
        (rgba(255, 0, 0, 1.0), hsl(0, 1, 0.5)),
        (rgba(0, 255, 0, 1.0), hsl(120.0, 1, 0.5)),
        (rgba(0, 0, 255, 1.0), hsl(240.0, 1, 0.5)),
        # Color with different channel values, including transparency
        (rgba(50, 128, 200, 0.0), hsl(208.8, 0.6, 0.4902)),
        (rgba(50, 128, 200, 0.5), hsl(208.8, 0.6, 0.4902)),
        (rgba(50, 128, 200, 0.9), hsl(208.8, 0.6, 0.4902)),
        (rgba(50, 128, 200, 1.0), hsl(208.8, 0.6, 0.4902)),
        # Color having intermediate alpha values
        (rgba(100, 200, 255, 0.15), hsl(201.2903, 1, 0.6961)),
        (rgba(120, 180, 240, 0.2), hsl(210.0, 0.8, 0.7059)),
        (rgba(150, 50, 100, 0.4), hsl(330.0, 0.5, 0.3922)),
        (rgba(50, 60, 70, 0.55), hsl(210.0, 0.1667, 0.2353)),
        (rgba(255, 255, 0, 0.3), hsl(60.0, 1, 0.5)),
    ],
)
def test_rgba_to_hsl(input_color, expected_color):
    """A rgba color can be converted to hsl."""
    assert_equal_color(input_color.hsl, expected_color, abs=1e-4)


@pytest.mark.parametrize(
    "input_color, expected_color",
    [
        # Black, gray, white,
        (rgb(0, 0, 0), rgba(0, 0, 0, 1.0)),
        (rgb(128, 128, 128), rgba(128, 128, 128, 1.0)),
        (rgb(255, 255, 255), rgba(255, 255, 255, 1.0)),
        # Primaries
        (rgb(255, 0, 0), rgba(255, 0, 0, 1.0)),
        (rgb(0, 255, 0), rgba(0, 255, 0, 1.0)),
        (rgb(0, 0, 255), rgba(0, 0, 255, 1.0)),
        # Color with different channel values
        (rgb(50, 128, 200), rgba(50, 128, 200, 1.0)),
        (rgb(100, 200, 255), rgba(100, 200, 255, 1.0)),
        (rgb(120, 180, 240), rgba(120, 180, 240, 1.0)),
        (rgb(150, 50, 100), rgba(150, 50, 100, 1.0)),
        (rgb(50, 60, 70), rgba(50, 60, 70, 1.0)),
        (rgb(255, 255, 0), rgba(255, 255, 0, 1.0)),
    ],
)
def test_rgb_to_rgba(input_color, expected_color):
    """A rgb color can be converted to rgba."""
    assert_equal_color(input_color.rgba, expected_color)


@pytest.mark.parametrize(
    "input_color, expected_color",
    [
        # Black, gray, white,
        (rgb(0, 0, 0), hsla(0, 0, 0, 1)),
        (rgb(128, 128, 128), hsla(0, 0, 0.502, 1)),
        (rgb(255, 255, 255), hsla(0, 0, 1, 1)),
        # Primaries
        (rgb(255, 0, 0), hsla(0, 1, 0.5, 1)),
        (rgb(0, 255, 0), hsla(120.0, 1, 0.5, 1)),
        (rgb(0, 0, 255), hsla(240.0, 1, 0.5, 1)),
        # Color with different channel values
        (rgb(50, 128, 200), hsla(208.8, 0.6, 0.4902, 1)),
        (rgb(100, 200, 255), hsla(201.2903, 1, 0.6961, 1)),
        (rgb(120, 180, 240), hsla(210.0, 0.8, 0.7059, 1)),
        (rgb(150, 50, 100), hsla(330.0, 0.5, 0.3922, 1)),
        (rgb(50, 60, 70), hsla(210.0, 0.1667, 0.2353, 1)),
        (rgb(255, 255, 0), hsla(60.0, 1, 0.5, 1)),
    ],
)
def test_rgb_to_hsla(input_color, expected_color):
    """A rgb color can be converted to hsla."""
    assert_equal_color(input_color.hsla, expected_color, abs=1e-4)


@pytest.mark.parametrize(
    "input_color, expected_color",
    [
        # Black, gray, white,
        (rgb(0, 0, 0), hsl(0, 0, 0)),
        (rgb(128, 128, 128), hsl(0, 0, 0.502)),
        (rgb(255, 255, 255), hsl(0, 0, 1)),
        # Primaries
        (rgb(255, 0, 0), hsl(0, 1, 0.5)),
        (rgb(0, 255, 0), hsl(120.0, 1, 0.5)),
        (rgb(0, 0, 255), hsl(240.0, 1, 0.5)),
        # Color with different channel values
        (rgb(50, 128, 200), hsl(208.8, 0.6, 0.4902)),
        (rgb(100, 200, 255), hsl(201.2903, 1, 0.6961)),
        (rgb(120, 180, 240), hsl(210.0, 0.8, 0.7059)),
        (rgb(150, 50, 100), hsl(330.0, 0.5, 0.3922)),
        (rgb(50, 60, 70), hsl(210.0, 0.1667, 0.2353)),
        (rgb(255, 255, 0), hsl(60.0, 1, 0.5)),
    ],
)
def test_rgb_to_hsl(input_color, expected_color):
    """A rgb color can be converted to hsl."""
    assert_equal_color(input_color.hsl, expected_color, abs=1e-4)


@pytest.mark.parametrize(
    "input_color, expected_color",
    [
        # Black, gray, white,
        (hsla(0, 0, 0, 0), hsl(0, 0, 0)),
        (hsla(0, 0, 0, 1), hsl(0, 0, 0)),
        (hsla(0, 0, 0.502, 1), hsl(0, 0, 0.502)),
        (hsla(0, 0, 1, 1), hsl(0, 0, 1)),
        # Primaries
        (hsla(0, 1, 0.5, 1), hsl(0, 1, 0.5)),
        (hsla(120.0, 1, 0.5, 1), hsl(120.0, 1, 0.5)),
        (hsla(240.0, 1, 0.5, 1), hsl(240.0, 1, 0.5)),
        # Color with different channel values, including transparency
        (hsla(208.8, 0.6, 0.4902, 0), hsl(208.8, 0.6, 0.4902)),
        (hsla(208.8, 0.6, 0.4902, 0.5), hsl(208.8, 0.6, 0.4902)),
        (hsla(208.8, 0.6, 0.4902, 0.9), hsl(208.8, 0.6, 0.4902)),
        (hsla(208.8, 0.6, 0.4902, 1), hsl(208.8, 0.6, 0.4902)),
        # Color having intermediate alpha values
        (hsla(201.2903, 1, 0.6961, 0.15), hsl(201.2903, 1, 0.6961)),
        (hsla(210.0, 0.8, 0.7059, 0.2), hsl(210.0, 0.8, 0.7059)),
        (hsla(330.0, 0.5, 0.3922, 0.4), hsl(330.0, 0.5, 0.3922)),
        (hsla(210.0, 0.1667, 0.2353, 0.55), hsl(210.0, 0.1667, 0.2353)),
        (hsla(60.0, 1, 0.5, 0.3), hsl(60.0, 1, 0.5)),
    ],
)
def test_hsla_to_hsl(input_color, expected_color):
    """A hsla color can be converted to hsl."""
    assert_equal_color(input_color.hsl, expected_color)


@pytest.mark.parametrize(
    "input_color, expected_color",
    [
        # Black, gray, white,
        (hsla(0, 0, 0, 0), rgba(0, 0, 0, 0)),
        (hsla(0, 0, 0, 1), rgba(0, 0, 0, 1.0)),
        (hsla(0, 0, 0.502, 1), rgba(128, 128, 128, 1.0)),
        (hsla(0, 0, 1, 1), rgba(255, 255, 255, 1.0)),
        # Primaries
        (hsla(0, 1, 0.5, 1), rgba(255, 0, 0, 1.0)),
        (hsla(120.0, 1, 0.5, 1), rgba(0, 255, 0, 1.0)),
        (hsla(240.0, 1, 0.5, 1), rgba(0, 0, 255, 1.0)),
        # Color with different channel values, including transparency
        (hsla(208.8, 0.6, 0.4902, 0), rgba(50, 128, 200, 0.0)),
        (hsla(208.8, 0.6, 0.4902, 0.5), rgba(50, 128, 200, 0.5)),
        (hsla(208.8, 0.6, 0.4902, 0.9), rgba(50, 128, 200, 0.9)),
        (hsla(208.8, 0.6, 0.4902, 1), rgba(50, 128, 200, 1.0)),
        # Color having intermediate alpha values
        (hsla(201.2903, 1, 0.6961, 0.15), rgba(100, 200, 255, 0.15)),
        (hsla(210.0, 0.8, 0.7059, 0.2), rgba(120, 180, 240, 0.2)),
        (hsla(330.0, 0.5, 0.3922, 0.4), rgba(150, 50, 100, 0.4)),
        (hsla(210.0, 0.1667, 0.2353, 0.55), rgba(50, 60, 70, 0.55)),
        (hsla(60.0, 1, 0.5, 0.3), rgba(255, 255, 0, 0.3)),
    ],
)
def test_hsla_to_rgba(input_color, expected_color):
    """A hsla color can be converted to rgba."""
    assert_equal_color(input_color.rgba, expected_color)


@pytest.mark.parametrize(
    "input_color, expected_color",
    [
        # Black, gray, white,
        (hsla(0, 0, 0, 0), rgb(0, 0, 0)),
        (hsla(0, 0, 0, 1), rgb(0, 0, 0)),
        (hsla(0, 0, 0.502, 1), rgb(128, 128, 128)),
        (hsla(0, 0, 1, 1), rgb(255, 255, 255)),
        # Primaries
        (hsla(0, 1, 0.5, 1), rgb(255, 0, 0)),
        (hsla(120.0, 1, 0.5, 1), rgb(0, 255, 0)),
        (hsla(240.0, 1, 0.5, 1), rgb(0, 0, 255)),
        # Color with different channel values, including transparency
        (hsla(208.8, 0.6, 0.4902, 0), rgb(50, 128, 200)),
        (hsla(208.8, 0.6, 0.4902, 0.5), rgb(50, 128, 200)),
        (hsla(208.8, 0.6, 0.4902, 0.9), rgb(50, 128, 200)),
        (hsla(208.8, 0.6, 0.4902, 1), rgb(50, 128, 200)),
        # Color having intermediate alpha values
        (hsla(201.2903, 1, 0.6961, 0.15), rgb(100, 200, 255)),
        (hsla(210.0, 0.8, 0.7059, 0.2), rgb(120, 180, 240)),
        (hsla(330.0, 0.5, 0.3922, 0.4), rgb(150, 50, 100)),
        (hsla(210.0, 0.1667, 0.2353, 0.55), rgb(50, 60, 70)),
        (hsla(60.0, 1, 0.5, 0.3), rgb(255, 255, 0)),
    ],
)
def test_hsla_to_rgb(input_color, expected_color):
    """A hsla color can be converted to rgb."""
    assert_equal_color(input_color.rgb, expected_color)


@pytest.mark.parametrize(
    "input_color, expected_color",
    [
        # Black, gray, white,
        (hsl(0, 0, 0), hsla(0, 0, 0, 1.0)),
        (hsl(0, 0, 0.502), hsla(0, 0, 0.502, 1.0)),
        (hsl(0, 0, 1), hsla(0, 0, 1, 1.0)),
        # Primaries
        (hsl(0, 1, 0.5), hsla(0, 1, 0.5, 1.0)),
        (hsl(120.0, 1, 0.5), hsla(120.0, 1, 0.5, 1.0)),
        (hsl(240.0, 1, 0.5), hsla(240.0, 1, 0.5, 1.0)),
        # Color with different channel values
        (hsl(208.8, 0.6, 0.4902), hsla(208.8, 0.6, 0.4902, 1.0)),
        (hsl(201.2903, 1, 0.6961), hsla(201.2903, 1, 0.6961, 1.0)),
        (hsl(210.0, 0.8, 0.7059), hsla(210.0, 0.8, 0.7059, 1.0)),
        (hsl(330.0, 0.5, 0.3922), hsla(330.0, 0.5, 0.3922, 1.0)),
        (hsl(210.0, 0.1667, 0.2353), hsla(210.0, 0.1667, 0.2353, 1.0)),
        (hsl(60.0, 1, 0.5), hsla(60.0, 1, 0.5, 1.0)),
    ],
)
def test_hsl_to_hsla(input_color, expected_color):
    """A hsl color can be converted to hsla."""
    assert_equal_color(input_color.hsla, expected_color)


@pytest.mark.parametrize(
    "input_color, expected_color",
    [
        # Black, gray, white,
        (hsl(0, 0, 0), rgba(0, 0, 0, 1.0)),
        (hsl(0, 0, 0.502), rgba(128, 128, 128, 1.0)),
        (hsl(0, 0, 1), rgba(255, 255, 255, 1.0)),
        # Primaries
        (hsl(0, 1, 0.5), rgba(255, 0, 0, 1.0)),
        (hsl(120.0, 1, 0.5), rgba(0, 255, 0, 1.0)),
        (hsl(240.0, 1, 0.5), rgba(0, 0, 255, 1.0)),
        # Color with different channel values
        (hsl(208.8, 0.6, 0.4902), rgba(50, 128, 200, 1.0)),
        (hsl(201.2903, 1, 0.6961), rgba(100, 200, 255, 1.0)),
        (hsl(210.0, 0.8, 0.7059), rgba(120, 180, 240, 1.0)),
        (hsl(330.0, 0.5, 0.3922), rgba(150, 50, 100, 1.0)),
        (hsl(210.0, 0.1667, 0.2353), rgba(50, 60, 70, 1.0)),
        (hsl(60.0, 1, 0.5), rgba(255, 255, 0, 1.0)),
    ],
)
def test_hsl_to_rgba(input_color, expected_color):
    """A hsl color can be converted to rgba."""
    assert_equal_color(input_color.rgba, expected_color)


@pytest.mark.parametrize(
    "input_color, expected_color",
    [
        # Black, gray, white,
        (hsl(0, 0, 0), rgb(0, 0, 0)),
        (hsl(0, 0, 0.502), rgb(128, 128, 128)),
        (hsl(0, 0, 1), rgb(255, 255, 255)),
        # Primaries
        (hsl(0, 1, 0.5), rgb(255, 0, 0)),
        (hsl(120.0, 1, 0.5), rgb(0, 255, 0)),
        (hsl(240.0, 1, 0.5), rgb(0, 0, 255)),
        # Color with different channel values
        (hsl(208.8, 0.6, 0.4902), rgb(50, 128, 200)),
        (hsl(201.2903, 1, 0.6961), rgb(100, 200, 255)),
        (hsl(210.0, 0.8, 0.7059), rgb(120, 180, 240)),
        (hsl(330.0, 0.5, 0.3922), rgb(150, 50, 100)),
        (hsl(210.0, 0.1667, 0.2353), rgb(50, 60, 70)),
        (hsl(60.0, 1, 0.5), rgb(255, 255, 0)),
    ],
)
def test_hsl_to_rgb(input_color, expected_color):
    """A hsl color can be converted to rgb."""
    assert_equal_color(input_color.rgb, expected_color)
