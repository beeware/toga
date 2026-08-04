import pytest

from toga_iOS.libs import UIWindow

from .dialogs import DialogsMixin
from .probe import BaseProbe
from .scaffolds.base import ScaffoldProbe


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

    def _assert_window_state(self, state):
        # Create an assertion function that the window's instantaneous state is a
        # specific required value.
        def _state_assertion():
            assert self.instantaneous_state == state

        return _state_assertion

    async def wait_for_window(self, message, state=None):
        await self.redraw(message)
        await ScaffoldProbe(self.window.scaffold).wait_for_layout()

        # If a specific window state has been requested, wait for that state to occur.
        if state:
            await self._wait_for_assertion(self._assert_window_state(state))

    async def cleanup(self):
        self.window.close()
        await self.redraw("Closing window")

    @property
    def instantaneous_state(self):
        return self.impl.get_window_state(in_progress_state=False)

    def has_toolbar(self):
        pytest.skip("Toolbars not implemented on iOS")
