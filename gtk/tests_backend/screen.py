import os

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
            # TODO: Check for the wayland monitor native type
            pass

    def assert_name(self):
        assert self.screen.name == self.native.get_model()

    def assert_origin(self):
        geometry = self.native.get_geometry()
        assert self.screen.origin == (geometry.x, geometry.y)

    def assert_size(self):
        geometry = self.native.get_geometry()
        assert self.screen.size == (geometry.width, geometry.height)
