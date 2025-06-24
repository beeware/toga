from pathlib import Path

import pytest
from android.graphics import Bitmap

import toga_android

from .probe import BaseProbe


class IconProbe(BaseProbe):
    # Android only supports 1 format, so the alternate is the same as the primary.
    alternate_resource = "resources/icons/blue"

    def __init__(self, app, icon):
        super().__init__(app)
        self.icon = icon
        assert isinstance(self.icon._impl.native, Bitmap)

    def assert_icon_content(self, path):
        if path == "resources/icons/green":
            assert (
                self.icon._impl.path == self.app.paths.app / "resources/icons/green.png"
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
            == Path(toga_android.__file__).parent / "resources/toga.png"
        )

    def assert_platform_icon_content(self):
        assert self.icon._impl.path == self.app.paths.app / "resources/logo-android.png"

    def assert_app_icon_content(self):
        pytest.xfail("Android apps don't have app icons at runtime")
