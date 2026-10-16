from pytest import skip
from win32more.Microsoft.UI.Windowing import DisplayArea

from toga.images import Image as TogaImage

from .probe import BaseProbe


class ScreenProbe(BaseProbe):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native
        assert isinstance(self.native, DisplayArea)

    def get_screenshot(self, format=TogaImage):
        skip("Screen.get_image_data is not implemented on toga_winui3 yet.")
