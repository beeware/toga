from pathlib import Path

import pytest

import toga_iOS
from toga_iOS.libs import UIImage

from .probe import BaseProbe


class IconProbe(BaseProbe):
    alternate_resource = "resources/icons/blue"
    alternate_bad = "resources/icons/bad_png"

    def __init__(self, app, icon):
        super().__init__()
        self.app = app
        self.icon = icon
        assert isinstance(self.icon._impl.native, UIImage)

    async def assert_icon_content(self, path):
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

    async def assert_default_icon_content(self):
        assert (
            self.icon._impl.path
            == Path(toga_iOS.__file__).parent / "resources/toga.icns"
        )

    async def assert_platform_icon_content(self):
        assert self.icon._impl.path == self.app.paths.app / "resources/logo-iOS.icns"

    def assert_app_icon_content(self):
        pytest.xfail("iOS apps don't have app icons at runtime")
