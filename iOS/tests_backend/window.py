import pytest

from toga_iOS.libs import UIApplication, UIWindow

from .dialogs import DialogsMixin
from .probe import BaseProbe


class WindowProbe(BaseProbe, DialogsMixin):
    def __init__(self, app, window):
        super().__init__()
        self.app = app
        self.window = window
        self.impl = window._impl
        self.native = window._impl.native
        assert isinstance(self.native, UIWindow)

    async def wait_for_window(self, message, minimize=False, full_screen=False):
        await self.redraw(message)

    @property
    def content_size(self):
        # Content height doesn't include the status bar or navigation bar.
        return (
            self.native.contentView.frame.size.width,
            self.native.contentView.frame.size.height
            - (
                UIApplication.sharedApplication.statusBarFrame.size.height
                + self.native.rootViewController.navigationBar.frame.size.height
            ),
        )

    def get_window_state(self, state):
        pytest.skip("Window states are not implemented on iOS")

    def has_toolbar(self):
        pytest.skip("Toolbars not implemented on iOS")
