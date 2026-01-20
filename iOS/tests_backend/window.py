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

    async def _wait_for_assertion(self, assertion, timeout=5, polling_interval=0.1):
        # Loop for up to `timeout` seconds, until assertion() passes without
        # raising an AssertionError
        loop = asyncio.get_running_loop()
        start_time = loop.time()
        while (loop.time() - start_time) < timeout:
            try:
                assertion()
                return
            except AssertionError as e:
                exception = e
                await asyncio.sleep(polling_interval)

        raise exception

    def _assert_container_layout(self):
        # If the window has been laid out, the origin should be at least at the
        # position of the top bar height.
        assert self.impl.container.content.native.frame.origin.y >= self.top_bar_height

    def _assert_window_state(self, state):
        # Create an assertion function that the window's instantaneous state is a
        # specific required value.
        def _state_assertion():
            assert self.instantaneous_state == state

        return _state_assertion

    async def wait_for_window(self, message, state=None):
        await self.redraw(message)

        # There may be some internal rendering delays that mean the container's content
        # hasn't undergone full layout; wait for that to occur.
        await self._wait_for_assertion(self._assert_container_layout)

        # If a specific window state has been requested, wait for that state to occur.
        if state:
            await self._wait_for_assertion(self._assert_window_state(state))

    async def cleanup(self):
        self.window.close()
        await self.redraw("Closing window")

    @property
    def content_size(self):
        # As a test, assert that our content is not overlapping the top bar.
        self._assert_container_layout()

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
