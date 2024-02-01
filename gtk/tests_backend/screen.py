import os

import pytest
from gi.repository import GdkX11

from toga.images import Image as TogaImage

from .probe import BaseProbe


class ScreenProbe(BaseProbe):
    def __init__(self, app, screen):
        super().__init__()
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native
        if "WAYLAND_DISPLAY" in os.environ:
            # TODO:
            # For wayland, the native type is `__gi__.GdkWaylandMonitor`
            # But it cannot be imported directly.
            pass
        else:
            assert isinstance(self.native, GdkX11.X11Monitor)
            # For CI, the native type is also GdkX11.X11Monitor

    def get_screenshot(self, format=TogaImage):
        if "WAYLAND_DISPLAY" in os.environ:
            pytest.skip("Screen.as_image() is not implemented on wayland.")
        else:
            return self.screen.as_image(format=format)
