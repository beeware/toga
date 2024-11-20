import pytest

from toga_iOS.libs import UIApplication, UIWindow

from .dialogs import DialogsMixin
from .probe import BaseProbe


class WindowProbe(BaseProbe, DialogsMixin):
    supports_fullscreen = False
    supports_presentation = False

    def __init__(self, app, window):
        super().__init__()
        self.app = app
        self.window = window
        self.impl = window._impl
        self.native = window._impl.native
        assert isinstance(self.native, UIWindow)

    async def wait_for_window(
        self,
        message,
        minimize=False,
        full_screen=False,
        state_switch_not_from_normal=False,
    ):
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

    @property
    def top_bar_height(self):
        return (
            UIApplication.sharedApplication.statusBarFrame.size.height
            + self.native.rootViewController.navigationBar.frame.size.height
        )

    @property
    def instantaneous_state(self):
        return self.impl.get_window_state(in_progress_state=False)

    def has_toolbar(self):
        pytest.skip("Toolbars not implemented on iOS")
