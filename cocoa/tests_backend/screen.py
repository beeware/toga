from toga_cocoa.libs import NSScreen

from .probe import BaseProbe


class ScreenProbe(BaseProbe):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native
        assert isinstance(self.native, NSScreen)

    def assert_name(self):
        assert self.screen.name == self.native.localizedName

    def assert_origin(self):
        frame_native = self.native.frame
        assert self.screen.origin == (frame_native.origin.x, frame_native.origin.y)

    def assert_size(self):
        frame_native = self.native.frame
        assert self.screen.size == (frame_native.size.width, frame_native.size.height)
