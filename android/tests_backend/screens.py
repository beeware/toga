from android.view import Display

import toga
from toga.images import Image as TogaImage
from toga_android.widgets.base import Scalable

from .probe import BaseProbe


class ScreenProbe(BaseProbe, Scalable):
    def __init__(self, screen):
        app = toga.App.app
        super().__init__(app)
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native
        self.init_scale(app._impl.native)
        assert isinstance(self.native, Display)

    def get_screenshot(self, format=TogaImage):
        return self.screen.as_image(format=format)
