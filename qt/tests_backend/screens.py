import pytest
from toga_qt.libs import IS_WAYLAND

from toga.images import Image as TogaImage

from .probe import BaseProbe


class ScreenProbe(BaseProbe):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native

    def get_screenshot(self, format=TogaImage):
        if IS_WAYLAND:
            pytest.xfail("Cannot get image in Qt using APIs of screen in Wayland")
        else:
            return self.screen.as_image(format=format)
