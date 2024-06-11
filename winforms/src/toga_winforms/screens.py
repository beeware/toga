from System.Drawing import (
    Bitmap,
    Graphics,
    Imaging,
    Point,
    Size as WinSize,
)
from System.IO import MemoryStream

from toga.screens import Screen as ScreenInterface
from toga.types import Position, Size


class Screen:
    _instances = {}

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
        name = self.native.DeviceName
        # WinForms Display naming convention is "\\.\DISPLAY1". Remove the
        # non-text part to prevent any errors due to non-escaped characters.
        return name.split("\\")[-1]

    def get_origin(self) -> Position:
        return Position(self.native.Bounds.X, self.native.Bounds.Y)

    def get_size(self) -> Size:
        return Size(self.native.Bounds.Width, self.native.Bounds.Height)

    def get_image_data(self):
        bitmap = Bitmap(*self.get_size())
        graphics = Graphics.FromImage(bitmap)
        source_point = Point(*self.get_origin())
        destination_point = Point(0, 0)
        copy_size = WinSize(*self.get_size())
        graphics.CopyFromScreen(source_point, destination_point, copy_size)
        stream = MemoryStream()
        bitmap.Save(stream, Imaging.ImageFormat.Png)
        return bytes(stream.ToArray())
