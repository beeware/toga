from toga_iOS.libs import UIScreen
from toga_iOS.screen import Screen as ScreenImpl

from .probe import BaseProbe


class ScreenProbe(BaseProbe):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native

    def assert_implementation_type(self):
        assert isinstance(self._impl, ScreenImpl)

    def assert_native_type(self):
        print(type(self.native))
        assert isinstance(self.native, UIScreen)

    def assert_name(self):
        assert self.screen.name == "iOS Screen"

    def assert_origin(self):
        assert self.screen.origin == (0, 0)

    def assert_size(self):
        assert self.screen.size == (
            int(self.native.bounds.size.width),
            int(self.native.bounds.size.height),
        )
