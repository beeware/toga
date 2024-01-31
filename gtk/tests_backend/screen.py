import os

import pytest
from gi.repository import GdkX11

from .probe import BaseProbe


class ScreenProbe(BaseProbe):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native
        if os.environ.get("XDG_SESSION_TYPE", "").lower() == "x11":
            assert isinstance(self.native, GdkX11.X11Monitor)
        else:
            # TODO: Check for the other monitor native types
            pass

    def get_screenshot(self):
        if "WAYLAND_DISPLAY" in os.environ:
            pytest.skip("Screen.as_image() is not implemented on wayland.")
        else:
            return self.screen.as_image()
