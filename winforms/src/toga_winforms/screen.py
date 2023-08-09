from toga.screen import Screen as ScreenInterface
from toga_winforms.libs import (
    Bitmap,
    Graphics,
    ImageFormat,
    MemoryStream,
    Point,
    Size,
)


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
        return self.native.DeviceName

    def get_origin(self):
        return self.native.Bounds.X, self.native.Bounds.Y

    def get_size(self):
        return self.native.Bounds.Width, self.native.Bounds.Height

    def get_image_data(self):
        bitmap = Bitmap(*self.get_size())
        graphics = Graphics.FromImage(bitmap)
        source_point = Point(*self.get_origin())
        destination_point = Point(0, 0)
        copy_size = Size(*self.get_size())
        graphics.CopyFromScreen(source_point, destination_point, copy_size)
        stream = MemoryStream()
        bitmap.Save(stream, ImageFormat.Png)
        return stream.ToArray()
