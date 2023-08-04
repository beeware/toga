import pytest

from toga_iOS.libs import UIImage

from .probe import BaseProbe


class IconProbe(BaseProbe):
    alternate_resource = "resources/icons/blue"

    def __init__(self, app, icon):
        super().__init__()
        self.app = app
        self.icon = icon
        assert isinstance(self.icon._impl.native, UIImage)

    def assert_icon_content(self, path):
        if path == "resources/icons/green":
            assert (
                self.icon._impl.path
                == self.app.paths.app / "resources" / "icons" / "green.icns"
            )
        elif path == "resources/icons/blue":
            assert (
                self.icon._impl.path
                == self.app.paths.app / "resources" / "icons" / "blue.png"
            )
        else:
            pytest.fail("Unknown icon resource")

    def assert_default_icon_content(self):
        assert self.icon._impl.path == self.app.paths.toga / "resources" / "toga.icns"
