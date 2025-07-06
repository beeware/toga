import pytest
from travertino.colors import color

def test_rgb_char_invalido_no_final():
    with pytest.raises(ValueError):
        color("rgb(1, 2, 3q")

def test_hsl_sem_percentual():
    with pytest.raises(ValueError):
        color("hsl(0, 50, 50)")

def test_rgba_strings_hex_e_percent():
    c = color('rgba("FF","00","FF","100%")')
    assert (c.r, c.g, c.b, c.a) == (255, 0, 255, 1.0)
