import pytest
from textual.screen import Screen as TextualScreen

from toga.constants import WindowState

from .probe import BaseProbe


class WindowProbe(BaseProbe):
    supports_as_image = False
    supports_closable = True
    supports_focus = True
    supports_minimizable = False
    supports_minimize = False
    supports_move_while_hidden = False
    supports_placement = False
    supports_unminimize = False
    fullscreen_presentation_equal_size = True
    maximize_fullscreen_presentation_equal_size = True

    def __init__(self, app, window):
        super().__init__()
        self.app = app
        self.window = window
        self.impl = window._impl
        self.native = window._impl.native
        assert isinstance(self.native, TextualScreen)

    async def wait_for_window(self, message, state=None):
        await self.redraw(message)
        if state:
            assert self.instantaneous_state == state

    async def cleanup(self):
        self.window.close()
        await self.redraw("Closing window")

    def close(self):
        pytest.xfail("Textual doesn't have native window close controls.")

    @property
    def content_size(self):
        return self.impl.container.width, self.impl.container.height

    @property
    def is_resizable(self):
        return False

    @property
    def is_closable(self):
        return True

    @property
    def is_minimized(self):
        return False

    def minimize(self):
        pytest.xfail("Textual doesn't support minimizing windows.")

    def unminimize(self):
        pytest.xfail("Textual doesn't support unminimizing windows.")

    @property
    def instantaneous_state(self):
        return WindowState.NORMAL

    def has_toolbar(self):
        if len(self.window.toolbar):
            pytest.xfail("Textual doesn't support native window toolbars.")
        return False

    def assert_is_toolbar_separator(self, index, section=False):
        pytest.xfail("Textual doesn't support native window toolbars.")

    def assert_toolbar_item(self, index, label, tooltip, has_icon, enabled):
        pytest.xfail("Textual doesn't support native window toolbars.")

    def press_toolbar_button(self, index):
        pytest.xfail("Textual doesn't support native window toolbars.")
