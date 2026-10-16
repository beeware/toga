import asyncio
from ctypes import byref, c_void_p, cast
from ctypes.wintypes import RECT
from functools import partial

import pytest
from System import EventArgs
from System.Windows.Forms import (
    Form,
    FormBorderStyle,
    FormWindowState,
    MenuStrip,
    Panel,
    ToolStrip,
    ToolStripSeparator,
)

from toga import Box, Command, Label, Position, Size
from toga.style.pack import Pack
from toga_winforms.libs import user32, win32constants as wc

from .dialogs import DialogsMixin
from .probe import BaseProbe


class WindowProbe(BaseProbe, DialogsMixin):
    # Disabling the close button requires overriding a protected method
    # (https://stackoverflow.com/a/7301828), which Python.NET doesn't support
    # (https://github.com/pythonnet/pythonnet/issues/2192).
    supports_closable = False
    supports_minimizable = True
    supports_move_while_hidden = True
    supports_unminimize = True
    supports_minimize = True
    supports_placement = True
    supports_as_image = True
    supports_focus = True
    fullscreen_presentation_equal_size = True
    maximize_fullscreen_presentation_equal_size = False

    def __init__(self, app, window):
        self.app = app
        self.window = window
        self.impl = window._impl
        super().__init__(window._impl.native)
        assert isinstance(self.native, Form)

    async def wait_for_window(self, message, state=None):
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

    async def close(self):
        self.native.Close()

    @property
    def content_size(self):
        client_size = self.client_size
        return Size(
            client_size.width,
            client_size.height - (self.impl._top_bars_height() / self.scale_factor),
        )

    @property
    def client_size(self):
        return Size(
            self.native.ClientSize.Width / self.scale_factor,
            self.native.ClientSize.Height / self.scale_factor,
        )

    @property
    def is_resizable(self):
        return self.native.FormBorderStyle == FormBorderStyle.Sizable

    @property
    def is_minimizable(self):
        return self.native.MinimizeBox

    @property
    def is_minimized(self):
        return self.native.WindowState == FormWindowState.Minimized

    async def minimize(self):
        if self.native.MinimizeBox:
            self.native.WindowState = FormWindowState.Minimized

    def unminimize(self):
        self.native.WindowState = FormWindowState.Normal

    @property
    def container_probe(self):
        panels = [
            control for control in self.native.Controls if isinstance(control, Panel)
        ]
        assert len(panels) == 1
        return BaseProbe(panels[0])

    @property
    def instantaneous_state(self):
        return self.impl.get_window_state(in_progress_state=False)

    @property
    def menubar_probe(self):
        return BaseProbe(bar) if (bar := self.native.MainMenuStrip) else None

    @property
    def toolbar_probe(self):
        return BaseProbe(bar) if (bar := self._native_toolbar()) else None

    def _native_toolbar(self):
        for control in self.native.Controls:
            if isinstance(control, ToolStrip) and not isinstance(control, MenuStrip):
                return control
        return None

    def has_toolbar(self):
        return self._native_toolbar() is not None

    def _native_toolbar_item(self, index):
        return self._native_toolbar().Items[index]

    def assert_is_toolbar_separator(self, index, section=False):
        assert isinstance(self._native_toolbar_item(index), ToolStripSeparator)

    def assert_toolbar_item(self, index, separators, label, tooltip, has_icon, enabled):
        item = self._native_toolbar_item(index)
        assert item.Text == label
        assert item.ToolTipText == tooltip
        assert (item.Image is not None) == has_icon
        assert item.Enabled == enabled

    def press_toolbar_button(self, index):
        self._native_toolbar_item(index).OnClick(EventArgs.Empty)

    async def assert_system_dpi_change(self, get_probe, mock_scale):
        real_scale = self.scale_factor
        if real_scale == mock_scale:
            pytest.skip("mock scale and real scale are the same")
        scale_change = mock_scale / real_scale
        client_size = self.client_size

        original_content = self.window.content
        AdjustWindowRectExForDpi_original = user32.AdjustWindowRectExForDpi

        # During our testing, we mock DPICHANGED events, but the system does not
        # actually change the DPI of the titlebar decors.  Thus, we need to be able
        # to keep proper track of those ourselves.
        def AdjustWindowRectExForDpi_mock(lpRect, dwStyle, bMenu, dwExStyle, dpi):
            return AdjustWindowRectExForDpi_original(
                lpRect, dwStyle, bMenu, dwExStyle, real_scale * 96
            )

        user32.AdjustWindowRectExForDpi = AdjustWindowRectExForDpi_mock

        native_window = self.window._impl.native
        bounds = native_window.Bounds
        new_width, new_height = (
            int(bounds.Width * scale_change),
            int(bounds.Height * scale_change),
        )
        original_window_rect = RECT(
            bounds.X, bounds.Y, bounds.X + bounds.Width, bounds.Y + bounds.Height
        )
        scaled_window_rect = RECT(
            bounds.X,
            bounds.Y,
            bounds.X + new_width,
            bounds.Y + new_height,
        )

        try:
            self.window.toolbar.add(Command(None, "Test command"))

            # Include widgets which are sized in different ways, with margin and fixed
            # sizes in both dimensions.
            self.window.content = Box(
                style=Pack(direction="row"),
                children=[
                    Label(
                        "fixed",
                        id="fixed",
                        style=Pack(
                            background_color="yellow", margin_left=20, width=100
                        ),
                    ),
                    Label(
                        "minimal",  # Shrink to fit content
                        id="minimal",
                        style=Pack(background_color="cyan", font_size=16),
                    ),
                    Label(
                        "flex",
                        id="flex",
                        style=Pack(
                            background_color="pink", flex=1, margin_top=15, height=50
                        ),
                    ),
                ],
            )
            await self.redraw("main_window is ready for testing")

            widget_ids = ["fixed", "minimal", "flex"]
            probes = {id: get_probe(self.window.widgets[id]) for id in widget_ids}

            decor_ids = ["menubar", "toolbar", "container"]
            probes.update({id: getattr(self, f"{id}_probe") for id in decor_ids})
            ids = widget_ids + decor_ids

            def get_metrics():
                return (
                    {id: Position(probes[id].x, probes[id].y) for id in ids},
                    {id: Size(probes[id].width, probes[id].height) for id in ids},
                    {id: probes[id].font_size for id in ids},
                )

            positions, sizes, font_sizes = get_metrics()

            # Because of hinting, font size changes can have non-linear effects on pixel
            # sizes.
            approx_fixed = partial(pytest.approx, abs=1)
            approx_font = partial(pytest.approx, rel=0.25)

            # Positions of the menubar, toolbar and top-level container are relative to
            # the window client area.
            assert font_sizes["menubar"] == 9
            assert positions["menubar"] == approx_fixed((0, 0))
            assert sizes["menubar"].width == approx_fixed(client_size.width)

            assert font_sizes["toolbar"] == 9
            assert positions["toolbar"] == approx_fixed((0, sizes["menubar"].height))
            assert sizes["toolbar"].width == approx_fixed(client_size.width)

            # Container has no text, so its font doesn't matter.
            assert positions["container"] == approx_fixed(
                (0, positions["toolbar"].y + sizes["toolbar"].height)
            )
            assert sizes["container"] == approx_fixed(
                (client_size.width, client_size.height - positions["container"].y)
            )

            # Positions of widgets are relative to the top-level container.
            assert font_sizes["fixed"] == 9  # Default font size on Windows
            assert positions["fixed"] == approx_fixed((20, 0))
            assert sizes["fixed"].width == approx_fixed(100)

            assert font_sizes["minimal"] == 16
            assert positions["minimal"] == approx_fixed((120, 0))
            assert sizes["minimal"].height == approx_font(
                sizes["fixed"].height * 16 / 9
            )

            assert font_sizes["flex"] == 9
            assert positions["flex"] == approx_fixed((120 + sizes["minimal"].width, 15))
            assert sizes["flex"] == approx_fixed(
                (client_size.width - positions["flex"].x, 50)
            )

            # Trigger the DPI change
            lParam = cast(byref(scaled_window_rect), c_void_p).value
            mock_dpi = int(mock_scale * 96)
            # high word = X dpi, low word = Y dpi -- should be the same
            wParam = mock_dpi * 0x10001

            handle = int(native_window.Handle.ToString())
            # We don't actually need uIdSubclass and dwRefData here, so we pad them out
            # with 0s.
            self.window._impl._subclass_proc(
                handle, wc.WM_DPICHANGED, wParam, lParam, 0, 0
            )

            # We cannot directly compare against new width and height here, as CI's
            # screen size is limited and clips the window when we resize it too large.
            if scale_change > 1:
                assert native_window.Width > bounds.Width
            else:
                assert native_window.Height > bounds.Height

            client_size = self.client_size

            await self.redraw(f"Triggered dpi change event with {mock_scale} dpi scale")

            # Check Widget size DPI scaling
            positions_scaled, sizes_scaled, font_sizes_scaled = get_metrics()
            for id in ids:
                if id != "container":
                    assert font_sizes_scaled[id] == approx_fixed(
                        font_sizes[id] * scale_change
                    )

            assert positions_scaled["menubar"] == approx_fixed((0, 0))
            # WinForms seems to impose a minimum height on the menubar and toolbar
            # for touchablility if the font size gets small; this limit is done relative
            # to the current DPI, and because we have no way to mock WinForms'
            # internals, we have to accept that if we're scaling to a very small scale
            # our menubar height may not be preserved correctly.
            if scale_change <= 1.5 / 1.25:
                assert sizes_scaled["menubar"][0] == approx_fixed(client_size.width)
            else:
                assert sizes_scaled["menubar"] == (
                    approx_fixed(client_size.width),
                    approx_font(sizes["menubar"].height * scale_change),
                )

            assert positions_scaled["toolbar"] == approx_fixed(
                (0, sizes_scaled["menubar"].height)
            )
            if scale_change <= 1.5 / 1.25:
                assert sizes_scaled["toolbar"][0] == approx_fixed(client_size.width)
            else:
                assert sizes_scaled["toolbar"] == (
                    approx_fixed(client_size.width),
                    approx_font(sizes["toolbar"].height * scale_change),
                )

            assert positions_scaled["container"] == approx_fixed(
                (0, positions_scaled["toolbar"].y + sizes_scaled["toolbar"].height)
            )
            assert sizes_scaled["container"] == approx_fixed(
                (
                    client_size.width,
                    client_size.height - positions_scaled["container"].y,
                )
            )

            assert positions_scaled["fixed"] == approx_fixed(
                Position(20, 0) * scale_change
            )
            assert sizes_scaled["fixed"] == (
                approx_fixed(100 * scale_change),
                approx_font(sizes["fixed"].height * scale_change),
            )

            assert positions_scaled["minimal"] == approx_fixed(
                Position(120, 0) * scale_change
            )
            assert sizes_scaled["minimal"] == approx_font(
                sizes["minimal"] * scale_change
            )

            assert positions_scaled["flex"] == approx_fixed(
                (
                    positions_scaled["minimal"].x + sizes_scaled["minimal"].width,
                    15 * scale_change,
                )
            )
            assert sizes_scaled["flex"] == approx_fixed(
                (
                    client_size.width - positions_scaled["flex"].x,
                    50 * scale_change,
                )
            )

        finally:
            user32.AdjustWindowRectExForDpi = AdjustWindowRectExForDpi_original
            # Trigger the DPI change
            lParam = cast(byref(original_window_rect), c_void_p).value
            real_dpi = int(real_scale * 96)
            # high word = X dpi, low word = Y dpi -- should be the same
            wParam = real_dpi * 0x10001

            handle = int(native_window.Handle.ToString())
            # We don't actually need uIdSubclass and dwRefData here, so we pad them out
            # with 0s.
            self.window._impl._subclass_proc(
                handle, wc.WM_DPICHANGED, wParam, lParam, 0, 0
            )

            client_size = self.client_size
            await self.redraw("Restored original state of main_window")
            assert get_metrics() == (positions, sizes, font_sizes)

            self.window.toolbar.clear()
            self.window.content = original_content
