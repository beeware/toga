from PIL import Image, ImageDraw

from toga.screens import Screen as ScreenInterface
from toga.types import Position, Size

from .utils import LoggedObject


class Screen(LoggedObject):
    _instances = {}

    # native: tuple = (
    #   name: str,
    #   origin: tuple(x:int, y:int),
    #   size: tuple(width:int, height:int)
    # )
    def __new__(cls, native):
        if native in cls._instances:
            return cls._instances[native]
        else:
            instance = super().__new__(cls)
            instance.interface = ScreenInterface(_impl=instance)
            instance.native = native
            cls._instances[native] = instance
            return instance

    def get_name(self):
        return self.native[0]

    def get_origin(self) -> Position:
        return Position(*self.native[1])

    def get_size(self) -> Size:
        return Size(*self.native[2])

    def get_image_data(self):
        self._action("get image data")

        img = Image.new("RGB", self.native[2], "white")
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), self.native[0], fill="black")  # text = self.native[0]
        return img
