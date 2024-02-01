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
        # Using XDG_SESSION_TYPE to detect specific native monitor types
        # Use WAYLAND_DISPLAY for everything else
        session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
        if session_type == "x11":
            assert isinstance(self.native, GdkX11.X11Monitor)
        elif session_type == "wayland":
            # For wayland, the native type is __gi__.GdkWaylandMonitor
            # But it cannot be imported directly.
            pass
        else:
            assert self.native == "a"
            # session_type is "" for CI
            # TODO: Check for the other monitor native types

    def get_screenshot(self):
        if "WAYLAND_DISPLAY" in os.environ:
            pytest.skip("Screen.as_image() is not implemented on wayland.")
        else:
            return self.screen.as_image()
