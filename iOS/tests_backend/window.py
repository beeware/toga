import asyncio

from toga_iOS.libs import UIApplication, UIBarButtonSystemItem, UIWindow

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
        if state:
            timeout = 5
            polling_interval = 0.1
            exception = None
            loop = asyncio.get_running_loop()
            start_time = loop.time()
            while (loop.time() - start_time) < timeout:
                try:
                    assert self.instantaneous_state == state
                    return
                except AssertionError as e:
                    exception = e
                    await asyncio.sleep(polling_interval)
                    continue
                raise exception

    async def cleanup(self):
        self.window.close()
        await self.redraw("Closing window")

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

    def _toolbar_items(self):
        navigation_item = self.impl.container.content_controller.navigationItem
        return (
            navigation_item.rightBarButtonItems.reverseObjectEnumerator().allObjects()
        )

    def has_toolbar(self):
        return len(self._toolbar_items()) > 0

    def assert_is_toolbar_separator(self, index, section=False):
        assert (
            self._toolbar_items()[index].systemItem
            == UIBarButtonSystemItem.FixedSpace.value
        )

    def assert_toolbar_item(self, index, label, tooltip, has_icon, enabled):
        item = self._toolbar_items()[index]
        assert item.title == label
        # # UIKit does not expose tooltips; no assertion possible.
        assert (item.image is not None) == has_icon
        # # No way to disable things on UIKit; do not check for it.

    def press_toolbar_button(self, index):
        item = self._toolbar_items()[index]
        item.target.performSelectorOnMainThread(
            item.action, withObject=item, waitUntilDone=True
        )
