from System.Windows.Forms import Screen as WinFormsScreen

from .probe import BaseProbe


class ScreenProbe(BaseProbe):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native
        assert isinstance(self.native, WinFormsScreen)

    def get_screenshot(self):
        return self.screen.as_image()
