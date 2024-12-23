from ctypes import wintypes

from System.Drawing import (
    Bitmap,
    Graphics,
    Imaging,
    Point,
    Size as WinSize,
)
from System.IO import MemoryStream

from toga import App
from toga.screens import Screen as ScreenInterface
from toga.types import Position, Size

from .libs import shcore, user32
from .widgets.base import Scalable


class Screen(Scalable):
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

    @property
    def dpi_scale(self):
        screen_rect = wintypes.RECT(
            self.native.Bounds.Left,
            self.native.Bounds.Top,
            self.native.Bounds.Right,
            self.native.Bounds.Bottom,
        )
        hMonitor = user32.MonitorFromRect(screen_rect, user32.MONITOR_DEFAULTTONEAREST)
        pScale = wintypes.UINT()
        shcore.GetScaleFactorForMonitor(hMonitor, pScale)
        return pScale.value / 100

    def get_name(self):
        name = self.native.DeviceName
        # WinForms Display naming convention is "\\.\DISPLAY1". Remove the
        # non-text part to prevent any errors due to non-escaped characters.
        return name.split("\\")[-1]

    # Screen.origin is scaled according to the DPI of the primary screen, because there
    # is no better choice that could cover screens of multiple DPIs.
    def get_origin(self) -> Position:
        primary_screen = App.app._impl.get_primary_screen()
        bounds = self.native.Bounds
        return Position(
            primary_screen.scale_out(bounds.X), primary_screen.scale_out(bounds.Y)
        )

    # Screen.size is scaled according to the screen's own DPI, to be consistent with the
    # scaling of Window size and content.
    def get_size(self) -> Size:
        bounds = self.native.Bounds
        return Size(self.scale_out(bounds.Width), self.scale_out(bounds.Height))

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
