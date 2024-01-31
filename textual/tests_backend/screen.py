import pytest

from textual.screen import Screen as TextualScreen


class ScreenProbe:
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native
        assert isinstance(self.native, TextualScreen)

    def get_screenshot(self):
        pytest.skip("Screen.as_image is not implemented on textual.")
