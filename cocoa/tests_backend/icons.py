from pathlib import Path

import PIL.Image
import pytest

import toga
import toga_cocoa
from toga_cocoa.libs import NSImage

from .probe import BaseProbe


class IconProbe(BaseProbe):
    alternate_resource = "resources/icons/blue"

    def __init__(self, app, icon):
        super().__init__()
        self.app = app
        self.icon = icon
        assert isinstance(self.icon._impl.native, NSImage)

    def assert_icon_content(self, path):
        if path == "resources/icons/green":
            assert (
                self.icon._impl.path
                == self.app.paths.app / "resources/icons/green.icns"
            )
        elif path == "resources/icons/blue":
            assert (
                self.icon._impl.path == self.app.paths.app / "resources/icons/blue.png"
            )
        else:
            pytest.fail("Unknown icon resource")

    def assert_default_icon_content(self):
        assert (
            self.icon._impl.path
            == Path(toga_cocoa.__file__).parent / "resources/toga.icns"
        )

    def assert_platform_icon_content(self):
        assert self.icon._impl.path == self.app.paths.app / "resources/logo-macOS.icns"

    def assert_app_icon_content(self):
        # We have no real way to check we've got the right icon; use pixel peeping as a
        # guess. Construct a PIL image from the current icon.
        img = toga.Image(self.icon._impl.native).as_format(PIL.Image.Image)

        # The default icon is transparent background, and brown in the center.
        # Due to icon resizing, the exact pixel color is inconsistent, depending
        # on whether it's the default or the value after a reset.
        assert img.getpixel((5, 5))[3] == 0
        mid_color = img.getpixel((img.size[0] // 2, img.size[1] // 2))
        assert mid_color in {(130, 100, 57, 255), (130, 109, 66, 255)}
