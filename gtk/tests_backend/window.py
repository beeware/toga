import asyncio

from toga.constants import WindowState
from toga_gtk.libs import IS_WAYLAND, Gdk, Gtk

from .dialogs import DialogsMixin
from .probe import BaseProbe


class WindowProbe(BaseProbe, DialogsMixin):
    # GTK defers a lot of window behavior to the window manager, which means some
    # features either don't exist, or we can't guarantee they behave the way Toga would
    # like.
    supports_closable = True
    supports_minimizable = False
    supports_move_while_hidden = False
    supports_unminimize = False
    # Wayland mostly prohibits interaction with the larger windowing environment
    supports_minimize = not IS_WAYLAND
    supports_placement = not IS_WAYLAND

    def __init__(self, app, window):
        super().__init__()
        self.app = app
        self.window = window
        self.impl = window._impl
        self.native = window._impl.native
        assert isinstance(self.native, Gtk.Window)

    async def wait_for_window(
        self,
        message,
        expected_state=None,
    ):
        await self.redraw(message, delay=0.1)
        if expected_state:
            timeout = 5
            polling_interval = 0.1
            exception = None
            loop = asyncio.get_running_loop()
            start_time = loop.time()
            while (loop.time() - start_time) < timeout:
                try:
                    assert self.instantaneous_state == expected_state
                    assert self.window._impl._pending_state_transition is None
                    return
                except AssertionError as e:
                    exception = e
                    await asyncio.sleep(polling_interval)
                    continue
                raise exception

    async def cleanup(self):
        # Store the pre closing window state as determination of
        # window state after closing the window is unreliable.
        pre_close_window_state = self.window.state
        self.window.close()
        if pre_close_window_state in {WindowState.FULLSCREEN, WindowState.MINIMIZED}:
            delay = 0.5
        else:
            delay = 0.1
        await self.redraw("Closing window", delay=delay)

    def close(self):
        if self.is_closable:
            # Trigger the OS-level window close event.
            self.native.emit("delete-event", None)

    @property
    def content_size(self):
        content_allocation = self.impl.container.get_allocation()
        return (content_allocation.width, content_allocation.height)

    @property
    def is_resizable(self):
        return self.native.get_resizable()

    @property
    def is_closable(self):
        return self.native.get_deletable()

    @property
    def is_minimized(self):
        return self.impl._window_state_flags & Gdk.WindowState.ICONIFIED

    def minimize(self):
        self.native.iconify()

    def unminimize(self):
        self.native.deiconify()

    @property
    def instantaneous_state(self):
        return self.impl.get_window_state(in_progress_state=False)

    def has_toolbar(self):
        return self.impl.native_toolbar.get_n_items() > 0

    def assert_is_toolbar_separator(self, index, section=False):
        item = self.impl.native_toolbar.get_nth_item(index)
        assert isinstance(item, Gtk.SeparatorToolItem)
        assert item.get_draw() == (not section)

    def assert_toolbar_item(self, index, label, tooltip, has_icon, enabled):
        item = self.impl.native_toolbar.get_nth_item(index)
        assert item.get_label() == label
        # FIXME: get_tooltip_text() doesn't work. The tooltip can be set, but the
        # API to return the value just doesn't work. If it is ever fixed, this
        # is the test for it:
        # assert (
        #     None if item.get_tooltip_text() is None else item.get_tooltip_text()
        # ) == tooltip
        assert (item.get_icon_widget() is not None) == has_icon
        assert item.get_sensitive() == enabled

    def press_toolbar_button(self, index):
        item = self.impl.native_toolbar.get_nth_item(index)
        item.emit("clicked")
