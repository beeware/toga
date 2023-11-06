import ctypes
from ctypes import byref, c_void_p, windll, wintypes
from pathlib import Path
from time import sleep

import pytest
from System import EventArgs
from System.Drawing import Point
from System.Windows.Forms import Application, Cursor, Screen as WinScreen

from .probe import BaseProbe
from .window import WindowProbe


class AppProbe(BaseProbe):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.main_window = app.main_window
        # The Winforms Application class is a singleton instance
        assert self.app._impl.native == Application

    @property
    def config_path(self):
        return (
            Path.home()
            / "AppData"
            / "Local"
            / "Tiberius Yak"
            / "Toga Testbed"
            / "Config"
        )

    @property
    def data_path(self):
        return (
            Path.home() / "AppData" / "Local" / "Tiberius Yak" / "Toga Testbed" / "Data"
        )

    @property
    def cache_path(self):
        return (
            Path.home()
            / "AppData"
            / "Local"
            / "Tiberius Yak"
            / "Toga Testbed"
            / "Cache"
        )

    @property
    def logs_path(self):
        return (
            Path.home() / "AppData" / "Local" / "Tiberius Yak" / "Toga Testbed" / "Logs"
        )

    @property
    def is_cursor_visible(self):
        # Despite what the documentation says, Cursor.Current never returns null in
        # Windows 10, whether the cursor is over the window or not.
        #
        # The following code is based on https://stackoverflow.com/a/12467292, but it
        # only works when the cursor is over the window.
        form = self.main_window._impl.native
        Cursor.Position = Point(
            form.Location.X + (form.Size.Width // 2),
            form.Location.Y + (form.Size.Height // 2),
        )

        # A small delay is apparently required for the new position to take effect.
        sleep(0.1)

        class POINT(ctypes.Structure):
            _fields_ = [
                ("x", ctypes.c_long),
                ("y", ctypes.c_long),
            ]

        class CURSORINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_uint32),
                ("flags", ctypes.c_uint32),
                ("hCursor", ctypes.c_void_p),
                ("ptScreenPos", POINT),
            ]

        GetCursorInfo = ctypes.windll.user32.GetCursorInfo
        GetCursorInfo.argtypes = [ctypes.POINTER(CURSORINFO)]

        info = CURSORINFO()
        info.cbSize = ctypes.sizeof(info)
        if not GetCursorInfo(ctypes.byref(info)):
            raise RuntimeError("GetCursorInfo failed")

        # `flags` is 0 or 1 in local testing, but the GitHub Actions runner always
        # returns 2 ("the system is not drawing the cursor because the user is providing
        # input through touch or pen instead of the mouse"). hCursor is more reliable.
        return info.hCursor is not None

    def is_full_screen(self, window):
        return WindowProbe(self.app, window).is_full_screen

    def content_size(self, window):
        return WindowProbe(self.app, window).content_size

    def _menu_item(self, path):
        item = self.main_window._impl.native.MainMenuStrip
        for i, label in enumerate(path):
            children = getattr(item, "Items" if i == 0 else "DropDownItems")
            child_labels = [child.Text for child in children]
            try:
                child_index = child_labels.index(label)
            except ValueError:
                raise AssertionError(
                    f"no item named {path[:i+1]}; options are {child_labels}"
                ) from None
            item = children[child_index]

        return item

    def _activate_menu_item(self, path):
        self._menu_item(path).OnClick(EventArgs.Empty)

    def activate_menu_exit(self):
        self._activate_menu_item(["File", "Exit"])

    def activate_menu_about(self):
        self._activate_menu_item(["Help", "About Toga Testbed"])

    async def close_about_dialog(self):
        await WindowProbe(self.app, self.main_window)._close_dialog("\n")

    def activate_menu_visit_homepage(self):
        self._activate_menu_item(["Help", "Visit homepage"])

    def assert_menu_item(self, path, *, enabled=True):
        assert self._menu_item(path).Enabled == enabled

    def assert_system_menus(self):
        self.assert_menu_item(["File", "Preferences"], enabled=False)
        self.assert_menu_item(["File", "Exit"])

        self.assert_menu_item(["Help", "Visit homepage"])
        self.assert_menu_item(["Help", "About Toga Testbed"])

    def activate_menu_close_window(self):
        pytest.xfail("This platform doesn't have a window management menu")

    def activate_menu_close_all_windows(self):
        pytest.xfail("This platform doesn't have a window management menu")

    def activate_menu_minimize(self):
        pytest.xfail("This platform doesn't have a window management menu")

    def keystroke(self, combination):
        pytest.xfail("Not applicable to this backend")

    # ------------------- Functions specific to test_system_dpi_change -------------------

    def trigger_dpi_change_event(self):
        self.app._impl.winforms_DisplaySettingsChanged(None, None)

    def assert_main_window_menubar_font_scale_updated(self):
        main_window_impl = self.main_window._impl
        assert (
            main_window_impl.native.MainMenuStrip.Font.FontFamily.Name
            == main_window_impl.original_menubar_font.FontFamily.Name
        )
        assert (
            main_window_impl.native.MainMenuStrip.Font.Size
            == main_window_impl.scale_font(main_window_impl.original_menubar_font.Size)
        )
        assert (
            main_window_impl.native.MainMenuStrip.Font.Style
            == main_window_impl.original_menubar_font.Style
        )

    def assert_main_window_toolbar_font_scale_updated(self):
        main_window_impl = self.main_window._impl
        assert (
            main_window_impl.toolbar_native.Font.FontFamily.Name
            == main_window_impl.original_toolbar_font.FontFamily.Name
        )
        assert main_window_impl.toolbar_native.Font.Size == main_window_impl.scale_font(
            main_window_impl.original_toolbar_font.Size
        )
        assert (
            main_window_impl.toolbar_native.Font.Style
            == main_window_impl.original_toolbar_font.Style
        )

    def assert_main_window_widgets_font_scale_updated(self):
        for widget in self.main_window.widgets:
            assert (
                widget._impl.native.Font.FontFamily.Name
                == widget._impl.original_font.FontFamily.Name
            )
            assert widget._impl.native.Font.Size == widget._impl.scale_font(
                widget._impl.original_font.Size
            )
            assert widget._impl.native.Font.Style == widget._impl.original_font.Style

    def assert_main_window_stack_trace_dialog_scale_updated(self):
        stack_trace_dialog_impl = (
            self.app.main_window._impl.current_stack_trace_dialog_impl
        )
        for control in stack_trace_dialog_impl.native.Controls:
            # Assert Font
            assert (
                control.Font.FontFamily.Name
                == stack_trace_dialog_impl.original_control_fonts[
                    control
                ].FontFamily.Name
            )
            assert control.Font.Size == stack_trace_dialog_impl.scale_font(
                stack_trace_dialog_impl.original_control_fonts[control].Size
            )
            assert (
                control.Font.Style
                == stack_trace_dialog_impl.original_control_fonts[control].Style
            )

            # Assert Bounds
            assert control.Bounds.X == stack_trace_dialog_impl.scale_in(
                stack_trace_dialog_impl.original_control_bounds[control].X
            )
            assert control.Bounds.Y == stack_trace_dialog_impl.scale_in(
                stack_trace_dialog_impl.original_control_bounds[control].Y
            )
            assert control.Bounds.Width == stack_trace_dialog_impl.scale_in(
                stack_trace_dialog_impl.original_control_bounds[control].Width
            )
            assert control.Bounds.Height == stack_trace_dialog_impl.scale_in(
                stack_trace_dialog_impl.original_control_bounds[control].Height
            )

    def assert_dpi_scale_equal_to_primary_screen_dpi_scale(self, window):
        screen = WinScreen.PrimaryScreen
        screen_rect = wintypes.RECT(
            screen.Bounds.Left,
            screen.Bounds.Top,
            screen.Bounds.Right,
            screen.Bounds.Bottom,
        )
        windll.user32.MonitorFromRect.restype = c_void_p
        windll.user32.MonitorFromRect.argtypes = [wintypes.RECT, wintypes.DWORD]
        # MONITOR_DEFAULTTONEAREST = 2
        hMonitor = windll.user32.MonitorFromRect(screen_rect, 2)
        pScale = wintypes.UINT()
        windll.shcore.GetScaleFactorForMonitor(c_void_p(hMonitor), byref(pScale))

        assert window._impl.dpi_scale == pScale.value / 100

    # ------------------------------------------------------------------------------------
