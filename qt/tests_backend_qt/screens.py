import pytest
from toga_qt.libs import get_is_wayland

from toga.images import Image as TogaImage

from .probe import BaseProbe


class ScreenProbe(BaseProbe):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native

    def get_screenshot(self, format=TogaImage):
        if get_is_wayland():
            pytest.xfail("Cannot get image in Qt using conventional APIs of screen")
        else:
            return self.screen.as_image(format=format)
