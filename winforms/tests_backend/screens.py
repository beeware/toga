from System.Windows.Forms import Screen as WinFormsScreen

from toga.images import Image as TogaImage

from .probe import BaseProbe


class ScreenProbe(BaseProbe):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native
        assert isinstance(self.native, WinFormsScreen)

    def get_screenshot(self, format=TogaImage):
        return self.screen.as_image(format=format)
