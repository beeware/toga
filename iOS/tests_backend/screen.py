import pytest

from toga_iOS.libs import UIScreen

from .probe import BaseProbe


class ScreenProbe(BaseProbe):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native
        assert isinstance(self.native, UIScreen)

    def get_screenshot(self):
        pytest.skip("Screen.as_image is not implemented on iOS.")
