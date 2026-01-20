import asyncio

import pytest

from toga_iOS.libs import UIWindow

from .dialogs import DialogsMixin
from .probe import BaseProbe


class WindowProbe(BaseProbe, DialogsMixin):
    supports_fullscreen = False
    supports_presentation = False
    supports_as_image = True
    supports_focus = True

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
        state=None,
    ):
        await self.redraw(message)

        # There may be some internal rendering delays that mean the container's content
        # hasn't undergone full layout; wait for that to occur.
        timeout = 5
        polling_interval = 0.1
        loop = asyncio.get_running_loop()
        start_time = loop.time()
        while (loop.time() - start_time) < timeout:
            if self.impl.container.content.native.frame.origin.y >= self.top_bar_height:
                return
            else:
                await asyncio.sleep(polling_interval)

        # If a specific window state has been requested, wait for that state to occur.
        if state:
            start_time = loop.time()
            while (loop.time() - start_time) < timeout:
                try:
                    assert self.instantaneous_state == state
                    return
                except AssertionError as e:
                    exception = e
                    await asyncio.sleep(polling_interval)

            raise exception

    async def cleanup(self):
        self.window.close()
        await self.redraw("Closing window")

    @property
    def content_size(self):
        # As a test, assert that our content is not overlapping the top bar.
        assert self.impl.container.content.native.frame.origin.y >= self.top_bar_height
        # Content height doesn't include the status bar or navigation bar.
        return (
            self.native.contentView.frame.size.width,
            self.native.contentView.frame.size.height
            - (
                self.native.rootViewController.navigationBar.frame.origin.y
                + self.native.rootViewController.navigationBar.frame.size.height
            ),
        )

    @property
    def top_bar_height(self):
        return (
            self.native.rootViewController.navigationBar.frame.origin.y
            + self.native.rootViewController.navigationBar.frame.size.height
        )

    @property
    def instantaneous_state(self):
        return self.impl.get_window_state(in_progress_state=False)

    def has_toolbar(self):
        pytest.skip("Toolbars not implemented on iOS")
