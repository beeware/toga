import asyncio

from PySide6.QtCore import Qt
from toga_qt.libs import IS_WAYLAND

from toga.constants import WindowState

from .probe import BaseProbe


class WindowProbe(BaseProbe):
    # There *is* a close button hint but it doesn't seem to work
    # under KDE so we take similar handling as winforms here: disable
    # the action of the close button.
    supports_closable = False
    supports_as_image = True
    supports_focus = True
    # Cannot be implemented on Qt, the minimize button will show even if hinted away
    supports_minimizable = False
    supports_move_while_hidden = False
    supports_unminimize = True
    supports_minimize = True
    supports_placement = True
    fullscreen_presentation_equal_size = True
    maximize_fullscreen_presentation_equal_size = False

    def __init__(self, app, window):
        self.app = app
        self.window = window
        self.native = window._impl.native
        self.container = window._impl.container
        assert self.native.isWindow()
        if IS_WAYLAND:
            self.supports_placement = (
                False  # returns all sorts of messy values in CI in mutter
            )
            self.supports_focus = (
                False  # Qt activiateWindow doesn't work with mutter used in CI
            )
            # Qt upstream bug
            self.supports_unminimize = False
            self.supports_minimize = False

    async def wait_for_window(self, message, state=None):
        # 0.15 seconds to allow window size operations to propagate
        # events.
        await self.redraw(message, 0.15)
        if state == WindowState.MINIMIZED and IS_WAYLAND:
            state = WindowState.NORMAL

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
            raise exception

    async def cleanup(self):
        self.window.close()
        await self.redraw("Closing window", delay=0.5)

    def close(self):
        if self.is_closable:
            self.native.close()

    @property
    def content_size(self):
        size = self.container.native.size()
        return (size.width(), size.height())

    @property
    def is_resizable(self):
        min_size = self.native.minimumSize()
        max_size = self.native.maximumSize()
        return not (min_size == max_size)

    @property
    def is_closable(self):
        flags = self.native.windowFlags()
        return bool(flags & Qt.WindowCloseButtonHint)

    @property
    def is_minimized(self):
        return self.native.isMinimized()

    def minimize(self):
        self.native.showMinimized()

    def unminimize(self):
        self.native.showNormal()

    @property
    def instantaneous_state(self):
        return self.window._impl.get_window_state(in_progress_state=False)

    def has_toolbar(self):
        return self.window._impl.toolbar_native is not None

    def assert_is_toolbar_separator(self, index, section=False):
        assert self.window._impl.toolbar_native.actions()[index].isSeparator()

    def assert_toolbar_item(self, index, label, tooltip, has_icon, enabled):
        action = self.window._impl.toolbar_native.actions()[index]
        assert action.text() == label
        if tooltip is None:
            tooltip = "No Tooltip"
        assert action.toolTip() == tooltip
        assert not action.icon().isNull() == has_icon
        assert action.isEnabled() == enabled

    def press_toolbar_button(self, index):
        self.window._impl.toolbar_native.actions()[index].trigger()
