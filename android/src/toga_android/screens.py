from android.graphics import (
    Bitmap,
    Canvas as A_Canvas,
)

from toga.screens import Screen as ScreenInterface
from toga.types import Position, Size

from .widgets.base import Scalable


class Screen(Scalable):
    _instances = {}

    def __new__(cls, app, native):
        if native in cls._instances:
            return cls._instances[native]
        else:
            instance = super().__new__(cls)
            instance.interface = ScreenInterface(_impl=instance)
            instance.native = native
            cls._instances[native] = instance
            cls.app = app
            instance.init_scale(instance.app.native)
            return instance

    def get_name(self):
        return self.native.getName()

    def get_origin(self) -> Position:
        return Position(0, 0)

    def get_size(self) -> Size:
        return Size(
            self.scale_out(self.native.getWidth()),
            self.scale_out(self.native.getHeight()),
        )

    def get_image_data(self):
        # Get the root view of the current activity
        root_view = self.app.native.getWindow().getDecorView().getRootView()
        bitmap = Bitmap.createBitmap(
            *map(self.scale_in, self.get_size()),
            Bitmap.Config.ARGB_8888,
        )
        canvas = A_Canvas(bitmap)
        root_view.draw(canvas)

        return bitmap
