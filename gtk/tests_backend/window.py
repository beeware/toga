import asyncio
import os

import pytest

from toga.constants import WindowState
from toga_gtk.libs import GTK_VERSION, IS_WAYLAND, Adw, Gdk, Gtk

from .dialogs import DialogsMixin
from .probe import BaseProbe


class WindowProbe(BaseProbe, DialogsMixin):
    # GTK defers a lot of window behavior to the window manager, which means some
    # features either don't exist, or we can't guarantee they behave the way Toga would
    # like.
    fullscreen_presentation_equal_size = True
    maximize_fullscreen_presentation_equal_size = False
    if GTK_VERSION < (4, 0, 0):
        supports_closable = True
        supports_as_image = True
        # Gtk 3.24.41 ships with Ubuntu 24.04 where present() works on Wayland
        supports_focus = not (IS_WAYLAND and GTK_VERSION < (3, 24, 41))
        # Wayland mostly prohibits interaction with the larger windowing environment
        supports_minimize = not IS_WAYLAND
        supports_placement = not IS_WAYLAND
    else:
        supports_closable = False
        supports_as_image = False
        supports_focus = False
        supports_minimize = False
        supports_placement = False
        # When the test is run under xvfb + nested mutter, as in the CI, the window
        # size of maximized state remains the same as in the fullscreen & presentation.
        # However, this is not the case when test is run on a normal ubuntu system.
        if os.environ.get("WAYLAND_DISPLAY") == "toga":
            maximize_fullscreen_presentation_equal_size = True
    supports_minimizable = False
    supports_move_while_hidden = False
    supports_unminimize = False

    def __init__(self, app, window):
        super().__init__()
        self.app = app
        self.window = window
        self.impl = window._impl
        self.native = window._impl.native
        if Adw is None:
            assert isinstance(self.native, Gtk.Window)
        else:
            assert isinstance(self.native, Adw.Window) or isinstance(
                self.native, Adw.ApplicationWindow
            )

    async def wait_for_window(
        self,
        message,
        state=None,
    ):
        await self.redraw(message, delay=0.1)
        if state:
            timeout = 5
            polling_interval = 0.1
            exception = None
            loop = asyncio.get_running_loop()
            start_time = loop.time()
            while (loop.time() - start_time) < timeout:
                try:
                    assert self.instantaneous_state == state
                    assert self.window._impl._pending_state_transition is None
                    if GTK_VERSION < (4, 0, 0) and IS_WAYLAND:
                        if state in {WindowState.FULLSCREEN, WindowState.PRESENTATION}:
                            # Add a slight delay to ensure window properties like
                            # `size` are updated according to the new state.
                            await self.redraw(delay=0.2)
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
        if pre_close_window_state in {
            WindowState.PRESENTATION,
            WindowState.FULLSCREEN,
            WindowState.MINIMIZED,
        }:
            delay = 0.5
        else:
            delay = 0.1
        await self.redraw("Closing window", delay=delay)

    def close(self):
        if self.is_closable:
            # Trigger the OS-level window close event.
            if GTK_VERSION < (4, 0, 0):
                self.native.emit("delete-event", None)
            else:
                self.native.emit("close-request")

    @property
    def content_size(self):
        if GTK_VERSION < (4, 0, 0):
            content_allocation = self.impl.container.get_allocation()
            return content_allocation.width, content_allocation.height
        else:
            pytest.skip("Content size in GTK4 is not implemented")
            content = self.impl.container
            return content.width, content.height

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
        if GTK_VERSION < (4, 0, 0):
            self.native.iconify()
        else:
            self.native.minimize()

    def unminimize(self):
        if GTK_VERSION < (4, 0, 0):
            self.native.deiconify()
        else:
            self.native.present()

    @property
    def instantaneous_state(self):
        return self.impl.get_window_state(in_progress_state=False)

    def has_toolbar(self):
        if GTK_VERSION < (4, 0, 0):
            return self.impl.native_toolbar.get_n_items() > 0
        pytest.skip("Toolbars not implemented on GTK4")

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
