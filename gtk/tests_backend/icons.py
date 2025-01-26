import sys
from pathlib import Path

import pytest

import toga
import toga_gtk
from toga_gtk.libs import GdkPixbuf

from .probe import BaseProbe


class IconProbe(BaseProbe):
    alternate_resource = "resources/icons/orange"

    def __init__(self, app, icon):
        super().__init__()
        self.app = app
        self.icon = icon
        # Check the icons that have been explicitly provided
        assert isinstance(self.icon._impl.native(16), GdkPixbuf.Pixbuf)
        assert isinstance(self.icon._impl.native(32), GdkPixbuf.Pixbuf)
        assert isinstance(self.icon._impl.native(72), GdkPixbuf.Pixbuf)
        # Make sure that a backfilled size can be created
        assert isinstance(self.icon._impl.native(64), GdkPixbuf.Pixbuf)

    def assert_icon_content(self, path):
        if path == "resources/icons/green":
            # Three icons given with size; others sizes match the generic name
            assert self.icon._impl.paths == {
                16: self.app.paths.app / "resources/icons/green-16.png",
                32: self.app.paths.app / "resources/icons/green-32.png",
                64: self.app.paths.app / "resources/icons/green.png",
                72: self.app.paths.app / "resources/icons/green-72.png",
                128: self.app.paths.app / "resources/icons/green.png",
                256: self.app.paths.app / "resources/icons/green.png",
                512: self.app.paths.app / "resources/icons/green.png",
            }
        elif path == "resources/icons/orange":
            # All icons match the single size .ico
            assert self.icon._impl.paths == {
                size: self.app.paths.app / "resources/icons/orange.ico"
                for size in [16, 32, 64, 72, 128, 256, 512]
            }
        else:
            pytest.fail("Unknown icon resource")

    def assert_default_icon_content(self):
        assert self.icon._impl.paths == {
            size: Path(toga_gtk.__file__).parent / "resources/toga.png"
            for size in [16, 32, 64, 72, 128, 256, 512]
        }

    def assert_platform_icon_content(self):
        # Only 32 and 72 pixel forms are available
        assert self.icon._impl.paths == {
            32: self.app.paths.app / "resources/logo-linux-32.png",
            72: self.app.paths.app / "resources/logo-linux-72.png",
        }

    def assert_app_icon_content(self):
        if Path(sys.executable).stem.startswith("python"):
            # When running in dev mode, the icon will fall back to the app default.
            assert self.icon._impl == toga.Icon.DEFAULT_ICON._impl
        else:
            assert self.icon._impl.paths == {
                16: (
                    Path(sys.executable).parent.parent
                    / "share/icons/hicolor/16x16/apps/org.beeware.toga.testbed.png"
                ),
                32: (
                    Path(sys.executable).parent.parent
                    / "share/icons/hicolor/32x32/apps/org.beeware.toga.testbed.png"
                ),
                64: (
                    Path(sys.executable).parent.parent
                    / "share/icons/hicolor/64x64/apps/org.beeware.toga.testbed.png"
                ),
                128: (
                    Path(sys.executable).parent.parent
                    / "share/icons/hicolor/128x128/apps/org.beeware.toga.testbed.png"
                ),
                256: (
                    Path(sys.executable).parent.parent
                    / "share/icons/hicolor/256x256/apps/org.beeware.toga.testbed.png"
                ),
                512: (
                    Path(sys.executable).parent.parent
                    / "share/icons/hicolor/512x512/apps/org.beeware.toga.testbed.png"
                ),
            }
