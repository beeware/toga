import asyncio
from ctypes import byref
from pathlib import Path

import PIL.Image
import pytest
import toga_winui3
from toga_winui3.libs.gdiplus import icon_pixels
from win32more import ComError, UInt32
from win32more.Microsoft.UI import IconId
from win32more.Microsoft.UI.Interop import GetWindowFromWindowId
from win32more.Microsoft.UI.Xaml.Controls import Button, ImageIcon
from win32more.Windows.Win32.UI.WindowsAndMessaging import (
    WM_GETICON,
    SendMessageW,
)

import toga

from .probe import BaseProbe


class IconProbe(BaseProbe):
    alternate_resource = "resources/icons/orange"
    alternate_bad = "resources/icons/bad_ico"

    def __init__(self, app, icon):
        super().__init__()
        self.app = app
        self.icon = icon

        # The WinUI 3 ImageIcon won't load until it has been added to the visual tree.
        self.container_native = app.main_window._impl.container.native
        self.button = Button()
        image_icon = self.icon._impl.image_icon()
        self.button.Content = image_icon
        self.container_native.Children.Append(self.button)

        assert isinstance(image_icon, ImageIcon)
        assert isinstance(self.icon._impl.id, IconId)

        # Create a future to track when the icon has been loaded.
        self._loaded = app.loop.create_future()
        if self.icon._impl._bitmap_image.PixelWidth > 0:
            self._loaded.set_result(self.icon._impl._bitmap_image.PixelWidth > 0)
        else:
            self.icon._impl._bitmap_image.event_handler.ImageOpened += (
                self.native_event_image_opened
            )

    def _cleanup(self):
        try:
            index = UInt32()
            self.container_native.Children.IndexOf(self.button, byref(index))
            self.container_native.Children.RemoveAt(index)
        except ComError:
            # This error occurs when the actual WinUI 3 object has been removed, for
            # example when its parent is destroyed, but the python win32more object
            # remains. Since the actual WinUI 3 object has been removed, and hence
            # will not raise any events, this error is ignored.
            pass

    def native_event_image_opened(self, sender, args):
        self._loaded.set_result(True)

    async def _assert_source(self, path: Path):
        if not self._loaded.done():
            async with asyncio.timeout(5):
                await self._loaded

        uri = f"file:///{self.icon._impl.path.as_posix()}"
        assert self.icon._impl.path == path
        assert self.icon._impl._bitmap_image.UriSource.ToString() == uri

        self._cleanup()

    async def assert_icon_content(self, path):
        if path == "resources/icons/green":
            await self._assert_source(self.app.paths.app / "resources/icons/green.png")
        elif path == "resources/icons/orange":
            await self._assert_source(self.app.paths.app / "resources/icons/orange.ico")
        else:
            pytest.fail("Unknown icon resource")

    async def assert_default_icon_content(self):
        await self._assert_source(
            Path(toga_winui3.__file__).parent / "resources/toga.png"
        )

    async def assert_platform_icon_content(self):
        await self._assert_source(self.app.paths.app / "resources/logo-windows.ico")

    def assert_app_icon_content(self):
        # Compare the pixels of the default icon using Pillow to those from the
        # registered app icon using GDI+.
        path = toga.Icon.DEFAULT_ICON._impl.path

        with PIL.Image.open(path).convert("RGBA") as pil_image:
            width_pil, height_pil = pil_image.size
            pixels_pil = pil_image.load()

        for window in self.app.windows:
            hwnd = GetWindowFromWindowId(window._impl.native.AppWindow.Id)
            hicon = SendMessageW(hwnd, WM_GETICON, 0, 0)
            pixels_gdip = icon_pixels(hicon)

            assert width_pil == len(pixels_gdip)
            assert height_pil == len(pixels_gdip[0])

            count = 0
            for x in range(width_pil):
                for y in range(height_pil):
                    if pixels_pil[x, y] == pixels_gdip[x][y]:
                        count += 1

            # There are some difference in how alpha is treated. Accept 97% match
            assert count / (width_pil * height_pil) > 0.97

        self._cleanup()
