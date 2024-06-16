from __future__ import annotations

from typing import TYPE_CHECKING

import System.Windows.Forms as WinForms
from System.Drawing import Bitmap, Graphics, Point, Size as WinSize
from System.Drawing.Imaging import ImageFormat
from System.IO import MemoryStream

from toga.command import Separator
from toga.constants import WindowState
from toga.types import Position, Size

from .container import Container
from .libs.wrapper import WeakrefCallable
from .screens import Screen as ScreenImpl
from .widgets.base import Scalable

if TYPE_CHECKING:  # pragma: no cover
    from toga.types import PositionT, SizeT


class Window(Container, Scalable):
    def __init__(self, interface, title, position, size):
        self.interface = interface

        # Winforms close handling is caught on the FormClosing handler. To allow
        # for async close handling, we need to be able to abort this close event,
        # call the Toga event handler, and let that decide whether to call close().
        # If it does, there will be another FormClosing event, which we need
        # to ignore. The `_is_closing` flag lets us do this.
        self._is_closing = False

        self.native = WinForms.Form()
        self.native.FormClosing += WeakrefCallable(self.winforms_FormClosing)
        super().__init__(self.native)
        self.init_scale(self.native)

        self.native.MinimizeBox = self.interface.minimizable
        self.native.MaximizeBox = self.interface.resizable

        self.set_title(title)
        self.set_size(size)
        # Winforms does window cascading by default; use that behavior, rather than
        # Toga's re-implementation.
        if position:
            self.set_position(position)

        self.toolbar_native = None

        self.native.Resize += WeakrefCallable(self.winforms_Resize)
        self.resize_content()  # Store initial size

        # Set window border style based on whether window resizability is enabled or not.
        self.native.FormBorderStyle = getattr(
            WinForms.FormBorderStyle,
            "Sizable" if self.interface.resizable else "FixedSingle",
        )

    ######################################################################
    # Native event handlers
    ######################################################################

    def winforms_Resize(self, sender, event):
        self.resize_content()

    def winforms_FormClosing(self, sender, event):
        # If the app is exiting, or a manual close has been requested, don't get
        # confirmation; just close.
        if not self.interface.app._impl._is_exiting and not self._is_closing:
            if not self.interface.closable:
                # Window isn't closable, so any request to close should be cancelled.
                event.Cancel = True
            else:
                # See _is_closing comment in __init__.
                self.interface.on_close()
                event.Cancel = True

    ######################################################################
    # Window properties
    ######################################################################

    def get_title(self):
        return self.native.Text

    def set_title(self, title):
        self.native.Text = title

    ######################################################################
    # Window lifecycle
    ######################################################################

    def close(self):
        if self.interface.content:
            self.interface.content.window = None
        self.interface.app.windows.discard(self.interface)

        self._is_closing = True
        self.native.Close()

        self.interface._closed = True

    def create_toolbar(self):
        if self.interface.toolbar:
            if self.toolbar_native:
                self.toolbar_native.Items.Clear()
            else:
                # The toolbar doesn't need to be positioned, because its `Dock` property
                # defaults to `Top`.
                self.toolbar_native = WinForms.ToolStrip()
                self.native.Controls.Add(self.toolbar_native)
                self.toolbar_native.BringToFront()  # In a dock, "front" means "bottom".

            prev_group = None
            for cmd in self.interface.toolbar:
                if isinstance(cmd, Separator):
                    item = WinForms.ToolStripSeparator()
                    prev_group = None
                else:
                    # A change in group requires adding a toolbar separator
                    if prev_group is not None and prev_group != cmd.group:
                        self.toolbar_native.Items.Add(WinForms.ToolStripSeparator())
                        prev_group = None
                    else:
                        prev_group = cmd.group

                    item = WinForms.ToolStripMenuItem(cmd.text)
                    if cmd.tooltip is not None:
                        item.ToolTipText = cmd.tooltip
                    if cmd.icon is not None:
                        item.Image = cmd.icon._impl.native.ToBitmap()
                    item.Enabled = cmd.enabled
                    item.Click += WeakrefCallable(cmd._impl.winforms_Click)
                    cmd._impl.native.append(item)
                self.toolbar_native.Items.Add(item)

        elif self.toolbar_native:
            self.native.Controls.Remove(self.toolbar_native)
            self.toolbar_native = None

        self.resize_content()

    def set_app(self, app):
        icon_impl = app.interface.icon._impl
        self.native.Icon = icon_impl.native

    def show(self):
        if self.interface.content is not None:
            self.interface.content.refresh()
        self.native.Show()

    ######################################################################
    # Window content and resources
    ######################################################################

    # "Decor" includes the title bar and the (usually invisible) resize borders. It does
    # not include the menu bar and toolbar, which are included in the ClientSize (see
    # _top_bars_height).
    def _decor_width(self):
        return self.native.Size.Width - self.native.ClientSize.Width

    def _decor_height(self):
        return self.native.Size.Height - self.native.ClientSize.Height

    def _top_bars_height(self):
        vertical_shift = 0
        if self.toolbar_native and self.toolbar_native.Visible:
            vertical_shift += self.toolbar_native.Height
        if self.native.MainMenuStrip and self.native.MainMenuStrip.Visible:
            vertical_shift += self.native.MainMenuStrip.Height
        return vertical_shift

    def refreshed(self):
        super().refreshed()
        layout = self.interface.content.layout
        self.native.MinimumSize = WinSize(
            self.scale_in(layout.min_width) + self._decor_width(),
            self.scale_in(layout.min_height)
            + self._top_bars_height()
            + self._decor_height(),
        )

    def resize_content(self):
        vertical_shift = self._top_bars_height()
        self.native_content.Location = Point(0, vertical_shift)
        super().resize_content(
            self.native.ClientSize.Width,
            self.native.ClientSize.Height - vertical_shift,
        )

    ######################################################################
    # Window size
    ######################################################################

    def get_size(self) -> Size:
        size = self.native.Size
        return Size(
            self.scale_out(size.Width - self._decor_width()),
            self.scale_out(size.Height - self._decor_height()),
        )

    def set_size(self, size: SizeT):
        self.native.Size = WinSize(
            self.scale_in(size[0]) + self._decor_width(),
            self.scale_in(size[1]) + self._decor_height(),
        )

    ######################################################################
    # Window position
    ######################################################################

    def get_current_screen(self):
        return ScreenImpl(WinForms.Screen.FromControl(self.native))

    def get_position(self) -> Position:
        location = self.native.Location
        return Position(*map(self.scale_out, (location.X, location.Y)))

    def set_position(self, position: PositionT):
        self.native.Location = Point(*map(self.scale_in, position))

    ######################################################################
    # Window visibility
    ######################################################################

    def get_visible(self):
        return self.native.Visible

    def hide(self):
        self.native.Hide()

    ######################################################################
    # Window state
    ######################################################################

    def get_window_state(self):
        window_state = self.native.WindowState
        if window_state == WinForms.FormWindowState.Maximized:
            if self.native.FormBorderStyle == getattr(WinForms.FormBorderStyle, "None"):
                # Use a shadow variable since a window without any app menu and toolbar
                # in presentation mode would be indistinguishable from full screen mode.
                if getattr(self, "_is_in_presentation_mode", False) is True:
                    return WindowState.PRESENTATION
                else:
                    return WindowState.FULLSCREEN
            else:
                return WindowState.MAXIMIZED
        elif window_state == WinForms.FormWindowState.Minimized:
            return WindowState.MINIMIZED
        elif window_state == WinForms.FormWindowState.Normal:
            return WindowState.NORMAL
        else:  # pragma: no cover
            # Marking this as no cover, since the above cases cover all the possible values
            # of the FormWindowState enum type that can be returned by WinForms.WindowState.
            return

    def set_window_state(self, state):
        if state == WindowState.NORMAL:
            current_state = self.get_window_state()
            if current_state == WindowState.PRESENTATION:
                if self.native.MainMenuStrip:
                    self.native.MainMenuStrip.Visible = True
                if self.toolbar_native:
                    self.toolbar_native.Visible = True

                self.interface.screen = self._before_presentation_mode_screen
                self._before_presentation_mode_screen = None
                self._is_in_presentation_mode = False

            self.native.FormBorderStyle = getattr(
                WinForms.FormBorderStyle,
                "Sizable" if self.interface.resizable else "FixedSingle",
            )
            self.native.WindowState = WinForms.FormWindowState.Normal
        else:
            if state == WindowState.MAXIMIZED:
                self.native.WindowState = WinForms.FormWindowState.Maximized

            elif state == WindowState.MINIMIZED:
                self.native.WindowState = WinForms.FormWindowState.Minimized

            elif state == WindowState.FULLSCREEN:
                self.native.FormBorderStyle = getattr(WinForms.FormBorderStyle, "None")
                self.native.WindowState = WinForms.FormWindowState.Maximized

            elif state == WindowState.PRESENTATION:
                if getattr(self, "_before_presentation_mode_screen", None) is None:
                    self._before_presentation_mode_screen = self.interface.screen
                if self.native.MainMenuStrip:
                    self.native.MainMenuStrip.Visible = False
                if self.toolbar_native:
                    self.toolbar_native.Visible = False
                self.native.FormBorderStyle = getattr(WinForms.FormBorderStyle, "None")
                self.native.WindowState = WinForms.FormWindowState.Maximized
                self._is_in_presentation_mode = True
            else:  # pragma: no cover
                # Marking this as no cover, since the type of the state parameter
                # value is checked on the interface.
                pass

    ######################################################################
    # Window capabilities
    ######################################################################

    def get_image_data(self):
        size = WinSize(self.native_content.Size.Width, self.native_content.Size.Height)
        bitmap = Bitmap(size.Width, size.Height)
        graphics = Graphics.FromImage(bitmap)

        graphics.CopyFromScreen(
            self.native_content.PointToScreen(Point.Empty),
            Point(0, 0),
            size,
        )

        stream = MemoryStream()
        bitmap.Save(stream, ImageFormat.Png)
        return bytes(stream.ToArray())
