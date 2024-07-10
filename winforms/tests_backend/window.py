from System import EventArgs
from System.Windows.Forms import (
    Form,
    FormBorderStyle,
    FormWindowState,
    MenuStrip,
    ToolStrip,
    ToolStripSeparator,
)

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

    def __init__(self, app, window):
        super().__init__()
        self.app = app
        self.window = window
        self.impl = window._impl
        self.native = window._impl.native
        assert isinstance(self.native, Form)

    async def wait_for_window(self, message, minimize=False, full_screen=False):
        await self.redraw(message)

    def close(self):
        self.native.Close()

    @property
    def content_size(self):
        return (
            (self.native.ClientSize.Width) / self.scale_factor,
            (
                (self.native.ClientSize.Height - self.impl._top_bars_height())
                / self.scale_factor
            ),
        )

    @property
    def is_full_screen(self):
        return (
            self.native.FormBorderStyle == getattr(FormBorderStyle, "None")
            and self.native.WindowState == FormWindowState.Maximized
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

    def minimize(self):
        if self.native.MinimizeBox:
            self.native.WindowState = FormWindowState.Minimized

    def unminimize(self):
        self.native.WindowState = FormWindowState.Normal

    def _native_toolbar(self):
        for control in self.native.Controls:
            if isinstance(control, ToolStrip) and not isinstance(control, MenuStrip):
                return control
        else:
            return None

    def has_toolbar(self):
        return self._native_toolbar() is not None

    def _native_toolbar_item(self, index):
        return self._native_toolbar().Items[index]

    def assert_is_toolbar_separator(self, index, section=False):
        assert isinstance(self._native_toolbar_item(index), ToolStripSeparator)

    def assert_toolbar_item(self, index, label, tooltip, has_icon, enabled):
        item = self._native_toolbar_item(index)
        assert item.Text == label
        assert item.ToolTipText == tooltip
        assert (item.Image is not None) == has_icon
        assert item.Enabled == enabled

    def press_toolbar_button(self, index):
        self._native_toolbar_item(index).OnClick(EventArgs.Empty)
