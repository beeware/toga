from pathlib import Path

import pytest

import toga_gtk
from toga_gtk.libs import Gtk

from .probe import BaseProbe


class IconProbe(BaseProbe):
    alternate_resource = "resources/icons/orange"

    def __init__(self, app, icon):
        super().__init__()
        self.app = app
        self.icon = icon
        assert isinstance(self.icon._impl.native, Gtk.Widget)

    def assert_icon_content(self, path):
        if path == "resources/icons/green":
            assert self.icon._impl.path == self.app.paths.app / "resources/icons/green.png"
        elif path == "resources/icons/orange":
            assert self.icon._impl.path == self.app.paths.app / "resources/icons/orange.ico"
        else:
            pytest.fail("Unknown icon resource")

    def assert_default_icon_content(self):
        assert self.icon._impl.path == Path(toga_gtk.__file__).parent / "resources/toga.png"

    def assert_platform_icon_content(self, platform):
        assert self.icon._impl.path == self.app.paths.app / f"resources/logo-{platform}.png"
