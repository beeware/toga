from ctypes import byref
from decimal import ROUND_HALF_EVEN, Decimal
from typing import ClassVar

from win32more.Microsoft.UI.Interop import GetMonitorFromDisplayId
from win32more.Windows.Win32.Graphics.Gdi import HMONITOR
from win32more.Windows.Win32.UI.Shell import GetScaleFactorForMonitor
from win32more.Windows.Win32.UI.Shell.Common import DEVICE_SCALE_FACTOR

from toga import App
from toga.screens import Screen as ScreenInterface
from toga.types import Position, Size


def round_pixels(value) -> int:
    return int(Decimal(value).to_integral(ROUND_HALF_EVEN))


class Screen:
    _instances: ClassVar[dict] = {}

    def __new__(cls, native):
        native_id = str(native.DisplayId.Value)
        if native_id in cls._instances:
            return cls._instances[native_id]
        else:
            instance = super().__new__(cls)
            instance.interface = ScreenInterface(_impl=instance)
            instance.native = native
            cls._instances[native_id] = instance
            return instance

    def __eq__(self, other) -> bool:
        return self.get_name() == other.get_name()

    @property
    def handle(self) -> HMONITOR:
        return GetMonitorFromDisplayId(self.native.DisplayId)

    def get_name(self) -> str:
        device_id = str(self.native.DisplayId.Value)
        return "screen-" + device_id

    ####################################################################################
    # DPI scaling
    ####################################################################################

    @property
    def dpi_scale(self) -> float:
        p_scale = DEVICE_SCALE_FACTOR()
        GetScaleFactorForMonitor(self.handle, byref(p_scale))
        return p_scale.value / 100

    def css_to_physical(self, value):
        return round_pixels(value * self.dpi_scale)

    def physical_to_css(self, value):
        return round_pixels(value / self.dpi_scale)

    ####################################################################################
    # Size and position
    ####################################################################################

    # Screen.origin is scaled according to the DPI of the primary screen, because there
    # is no better choice that could cover screens of multiple DPIs.
    def get_origin(self) -> Position:
        native_bounds = self.native.OuterBounds
        physical_to_css = App.app._impl.get_primary_screen().physical_to_css

        return Position(
            physical_to_css(native_bounds.X), physical_to_css(native_bounds.Y)
        )

    # Screen.size is scaled according to the screen's own DPI, to be consistent with the
    # scaling of Window size and content.
    def get_size(self) -> Size:
        native_bounds = self.native.OuterBounds
        return Size(
            self.physical_to_css(native_bounds.Width),
            self.physical_to_css(native_bounds.Width),
        )

    ####################################################################################
    # Screen capabilities
    ####################################################################################

    def get_image_data(self):
        self.interface.factory.not_implemented("Screen.get_image_data()")
