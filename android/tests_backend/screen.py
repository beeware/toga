import pytest
from android.view import Display

from toga_android.widgets.base import Scalable

from .probe import BaseProbe


class ScreenProbe(BaseProbe, Scalable):
    def __init__(self, app, screen):
        super().__init__(app)
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native
        self.init_scale(app._impl.native)
        assert isinstance(self.native, Display)

    def get_screenshot(self):
        pytest.skip("Screen.as_image is not implemented on Android.")
