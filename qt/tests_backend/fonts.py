import pytest

from toga.fonts import NORMAL


class FontMixin:
    supports_custom_fonts = False
    supports_custom_variable_fonts = False

    def preinstalled_font(self):
        pytest.skip("Qt backend doesn't implement fonts")

    def assert_font_family(self, expected):
        pytest.skip("Qt backend doesn't implement fonts")

    def assert_font_size(self, expected):
        pytest.skip("Qt backend doesn't implement fonts")

    def assert_font_options(self, weight=NORMAL, style=NORMAL, variant=NORMAL):
        pytest.skip("Qt backend doesn't implement fonts")
