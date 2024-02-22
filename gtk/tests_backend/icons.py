from pathlib import Path

import pytest

import toga_gtk
from toga_gtk.libs import GdkPixbuf

from .probe import BaseProbe


class IconProbe(BaseProbe):
    alternate_resource = "resources/icons/orange"

    def __init__(self, app, icon):
        super().__init__()
        self.app = app
        self.icon = icon
        assert isinstance(self.icon._impl.native_16, GdkPixbuf.Pixbuf)
        assert isinstance(self.icon._impl.native_32, GdkPixbuf.Pixbuf)
        assert isinstance(self.icon._impl.native_72, GdkPixbuf.Pixbuf)

    def assert_icon_content(self, path):
        if path == "resources/icons/green":
            assert self.icon._impl.paths == {
                16: self.app.paths.app / "resources/icons/green-16.png",
                32: self.app.paths.app / "resources/icons/green-32.png",
                72: self.app.paths.app / "resources/icons/green-72.png",
            }
        elif path == "resources/icons/orange":
            assert self.icon._impl.paths == {
                16: self.app.paths.app / "resources/icons/orange.ico",
                32: self.app.paths.app / "resources/icons/orange.ico",
                72: self.app.paths.app / "resources/icons/orange.ico",
            }
        else:
            pytest.fail("Unknown icon resource")

    def assert_default_icon_content(self):
        assert self.icon._impl.paths == {
            16: Path(toga_gtk.__file__).parent / "resources/toga.png",
            32: Path(toga_gtk.__file__).parent / "resources/toga.png",
            72: Path(toga_gtk.__file__).parent / "resources/toga.png",
        }

    def assert_platform_icon_content(self):
        assert self.icon._impl.paths == {
            16: self.app.paths.app / "resources/logo-linux-16.png",
            32: self.app.paths.app / "resources/logo-linux-32.png",
            72: self.app.paths.app / "resources/logo-linux-72.png",
        }
