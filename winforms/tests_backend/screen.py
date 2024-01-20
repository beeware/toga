from System.Windows.Forms import Screen as WinFormsScreen

from toga_winforms.screen import Screen as ScreenImpl

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
        assert isinstance(self.native, WinFormsScreen)

    def assert_name(self):
        assert self.screen.name == self.native.DeviceName

    def assert_origin(self):
        assert self.screen.origin == (self.native.Bounds.X, self.native.Bounds.Y)

    def assert_size(self):
        assert self.screen.size == (self.native.Bounds.Width, self.native.Bounds.Height)
