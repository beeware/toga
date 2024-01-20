from android.view import Display

from toga_android.screen import Screen as ScreenImpl
from toga_android.widgets.base import Scalable

from .probe import BaseProbe


class ScreenProbe(BaseProbe, Scalable):
    def __init__(self, app, screen):
        super().__init__(app)
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native
        self.init_scale(app._impl.native)

    def assert_implementation_type(self):
        assert isinstance(self._impl, ScreenImpl)

    def assert_native_type(self):
        print(type(self.native))
        assert isinstance(self.native, Display)

    def assert_name(self):
        assert self.screen.name == self.native.getName()

    def assert_origin(self):
        assert self.screen.origin == (0, 0)

    def assert_size(self):
        assert self.screen.size == (
            self.scale_out(self.native.getWidth()),
            self.scale_out(self.native.getHeight()),
        )
