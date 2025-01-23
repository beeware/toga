from __future__ import annotations

from typing import TYPE_CHECKING

import System.Windows.Forms as WinForms
from System.Drawing import Bitmap, Font as WinFont, Graphics, Point, Size as WinSize
from System.Drawing.Imaging import ImageFormat
from System.IO import MemoryStream

from toga import App
from toga.command import Separator
from toga.constants import WindowState
from toga.types import Position, Size

from .container import Container
from .fonts import DEFAULT_FONT
from .libs.wrapper import WeakrefCallable
from .screens import Screen as ScreenImpl
from .widgets.base import Scalable

if TYPE_CHECKING:  # pragma: no cover
    from toga.types import PositionT, SizeT


# It looks like something is caching the initial scale of the primary screen, and
# scaling all font sizes by it. Experiments show that this cache is at the level of the
# app, not the window.
initial_dpi_scale = ScreenImpl(WinForms.Screen.PrimaryScreen).dpi_scale


class Window(Container, Scalable):
    def __init__(self, interface, title, position, size):
        self.interface = interface

        self.create()

        self._FormClosing_handler = WeakrefCallable(self.winforms_FormClosing)
        self.native.FormClosing += self._FormClosing_handler
        super().__init__(self.native)
        self._dpi_scale = self.get_current_screen().dpi_scale

        self.native.MinimizeBox = self.interface.minimizable
        self.native.MaximizeBox = self.interface.resizable

        # Use a shadow variable since a window without any app menu and toolbar
        # in presentation mode would be indistinguishable from full screen mode.
        self._in_presentation_mode = False
        # Required to detect if the window has been un-minimized, and to prevent
        # double triggering of visibility events.
        self._previous_state = WindowState.NORMAL

        self.set_title(title)
        self.set_size(size)
        # Winforms does window cascading by default; use that behavior, rather than
        # Toga's re-implementation.
        if position:
            self.set_position(position)

        self.native.LocationChanged += WeakrefCallable(self.winforms_LocationChanged)
        self.native.Resize += WeakrefCallable(self.winforms_Resize)
        self.resize_content()  # Store initial size

        # Set window border style based on the window resizability setting at interface.
        self.native.FormBorderStyle = getattr(
            WinForms.FormBorderStyle,
            "Sizable" if self.interface.resizable else "FixedSingle",
        )

        self.native.Activated += WeakrefCallable(self.winforms_Activated)
        self.native.Deactivate += WeakrefCallable(self.winforms_Deactivate)
        self.native.VisibleChanged += WeakrefCallable(self.winforms_VisibleChanged)
        self.native.SizeChanged += WeakrefCallable(self.winforms_SizeChanged)

    def create(self):
        self.native = WinForms.Form()

    # We cache the scale to make sure that it only changes inside update_dpi.
    @property
    def dpi_scale(self):
        return self._dpi_scale

    def scale_font(self, native_font):
        return WinFont(
            native_font.FontFamily,
            native_font.Size * (self.dpi_scale / initial_dpi_scale),
            native_font.Style,
        )

    ######################################################################
    # Native event handlers
    ######################################################################

    def winforms_Resize(self, sender, event):
        if self.native.WindowState != WinForms.FormWindowState.Minimized:
            self.resize_content()

        # See DisplaySettingsChanged in app.py.
        if self.get_current_screen().dpi_scale != self._dpi_scale:
            self.update_dpi()

    def winforms_FormClosing(self, sender, event):
        # If the app is exiting, do nothing; we've already approved the exit
        # (and thus the window close). This branch can't be triggered in test
        # conditions, so it's marked no-branch.
        #
        # Otherwise, handle the close request by always cancelling the event,
        # and invoking `on_close()` handling. This will evaluate whether a close
        # is allowed, and if it is, programmatically invoke close on the window,
        # removing this handler first so that the close will complete.
        #
        # Winforms doesn't provide a way to disable/hide the close button, so if
        # the window is non-closable, don't trigger on_close handling - just
        # cancel the close event.
        if not self.interface.app._impl._is_exiting:  # pragma: no branch
            if self.interface.closable:
                self.interface.on_close()
            event.Cancel = True

    def winforms_LocationChanged(self, sender, event):
        # See DisplaySettingsChanged in app.py.
        if self.get_current_screen().dpi_scale != self._dpi_scale:
            self.update_dpi()

    def winforms_Activated(self, sender, event):
        self.interface.on_gain_focus()

    def winforms_Deactivate(self, sender, event):
        self.interface.on_lose_focus()

    def winforms_VisibleChanged(self, sender, event):
        if self.native.Visible:
            self.interface.on_show()
        else:
            self.interface.on_hide()

    def winforms_SizeChanged(self, sender, event):
        current_state = self.get_window_state()
        if self._previous_state != current_state:
            if self._previous_state == WindowState.MINIMIZED:
                self.interface.on_show()
            elif current_state == WindowState.MINIMIZED:
                self.interface.on_hide()
            self._previous_state = current_state

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
        self.native.FormClosing -= self._FormClosing_handler
        self.native.Close()

    def set_app(self, app):
        icon_impl = app.interface.icon._impl
        self.native.Icon = icon_impl.native

    def show(self):
        if self.interface.content is not None:
            self.interface.content.refresh()
        self.update_dpi()
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
        return 0

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

    def update_dpi(self):
        self._dpi_scale = self.get_current_screen().dpi_scale

        # Update all the native fonts and determine the new preferred sizes.
        for widget in self.interface.widgets:
            widget._impl.scale_font()
            widget._impl.refresh()

        # Then do a single layout pass.
        if self.interface.content is not None:
            self.interface.content.refresh()

        self.resize_content()

    ######################################################################
    # Window size
    ######################################################################

    # Window.size is scaled according to the DPI of the current screen, to be consistent
    # with the scaling of its content.
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

    # Window.position is scaled according to the DPI of the primary screen, because the
    # interface layer assumes that Screen.origin, Window.position and
    # Window.screen_position are all in the same coordinate system.
    #
    # TODO: remove that assumption, and make Window.position return coordinates relative
    # to the current screen's origin and DPI.
    def get_position(self) -> Position:
        location = self.native.Location
        primary_screen = App.app._impl.get_primary_screen()
        return Position(*map(primary_screen.scale_out, (location.X, location.Y)))

    def set_position(self, position: PositionT):
        primary_screen = App.app._impl.get_primary_screen()
        self.native.Location = Point(*map(primary_screen.scale_in, position))

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

    def get_window_state(self, in_progress_state=False):
        window_state = self.native.WindowState
        if window_state == WinForms.FormWindowState.Maximized:
            if self.native.FormBorderStyle == getattr(WinForms.FormBorderStyle, "None"):
                if self._in_presentation_mode:
                    return WindowState.PRESENTATION
                else:
                    return WindowState.FULLSCREEN
            else:
                return WindowState.MAXIMIZED
        elif window_state == WinForms.FormWindowState.Minimized:
            return WindowState.MINIMIZED
        else:  # window_state == WinForms.FormWindowState.Normal:
            return WindowState.NORMAL

    def set_window_state(self, state):
        # If the app is in presentation mode, but this window isn't, then
        # exit app presentation mode before setting the requested state.
        if any(
            window.state == WindowState.PRESENTATION and window != self.interface
            for window in self.interface.app.windows
        ):
            self.interface.app.exit_presentation_mode()

        current_state = self.get_window_state()
        if current_state == state:
            return

        elif current_state != WindowState.NORMAL:
            if current_state == WindowState.PRESENTATION:
                if self.native.MainMenuStrip:
                    self.native.MainMenuStrip.Visible = True
                if getattr(self, "toolbar_native", None):
                    self.toolbar_native.Visible = True

                self.interface.screen = self._before_presentation_mode_screen
                del self._before_presentation_mode_screen
                self._in_presentation_mode = False

            self.native.FormBorderStyle = getattr(
                WinForms.FormBorderStyle,
                "Sizable" if self.interface.resizable else "FixedSingle",
            )
            self.native.WindowState = WinForms.FormWindowState.Normal

            self.set_window_state(state)

        else:  # current_state == WindowState.NORMAL:
            if state == WindowState.MAXIMIZED:
                self.native.WindowState = WinForms.FormWindowState.Maximized

            elif state == WindowState.MINIMIZED:
                self.native.WindowState = WinForms.FormWindowState.Minimized

            elif state == WindowState.FULLSCREEN:
                self.native.FormBorderStyle = getattr(WinForms.FormBorderStyle, "None")
                self.native.WindowState = WinForms.FormWindowState.Maximized

            else:  # state == WindowState.PRESENTATION:
                self._before_presentation_mode_screen = self.interface.screen
                if self.native.MainMenuStrip:
                    self.native.MainMenuStrip.Visible = False
                if getattr(self, "toolbar_native", None):
                    self.toolbar_native.Visible = False
                self.native.FormBorderStyle = getattr(WinForms.FormBorderStyle, "None")
                self.native.WindowState = WinForms.FormWindowState.Maximized
                self._in_presentation_mode = True

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


class MainWindow(Window):
    def create(self):
        super().create()
        self.toolbar_native = None

    def update_dpi(self):
        super().update_dpi()
        if self.native.MainMenuStrip:  # pragma: no branch
            self.native.MainMenuStrip.Font = self.scale_font(DEFAULT_FONT)
        if self.toolbar_native:
            self.toolbar_native.Font = self.scale_font(DEFAULT_FONT)
        self.resize_content()

    def _top_bars_height(self):
        vertical_shift = 0
        if self.toolbar_native and self.toolbar_native.Visible:
            vertical_shift += self.toolbar_native.Height
        if self.native.MainMenuStrip and self.native.MainMenuStrip.Visible:
            vertical_shift += self.native.MainMenuStrip.Height
        return vertical_shift

    def _submenu(self, group, group_cache):
        try:
            return group_cache[group]
        except KeyError:
            parent_menu = self._submenu(group.parent, group_cache)

            submenu = WinForms.ToolStripMenuItem(group.text)

            # Top level menus are added in a different way to submenus
            if group.parent is None:
                parent_menu.Items.Add(submenu)
            else:
                parent_menu.DropDownItems.Add(submenu)

            group_cache[group] = submenu
        return submenu

    def create_menus(self):
        menubar = self.native.MainMenuStrip
        if menubar:
            menubar.Items.Clear()
        else:
            # The menu bar doesn't need to be positioned, because its `Dock` property
            # defaults to `Top`.
            menubar = WinForms.MenuStrip()
            self.native.Controls.Add(menubar)
            self.native.MainMenuStrip = menubar
            self.native.MainMenuStrip.Font = self.scale_font(DEFAULT_FONT)
            menubar.SendToBack()  # In a dock, "back" means "top".

        group_cache = {None: menubar}

        submenu = None
        for cmd in self.interface.app.commands:
            submenu = self._submenu(cmd.group, group_cache)
            if isinstance(cmd, Separator):
                item = "-"
            else:
                item = cmd._impl.create_menu_item(WinForms.ToolStripMenuItem)

            submenu.DropDownItems.Add(item)

        self.resize_content()

    def create_toolbar(self):
        if self.interface.toolbar:
            if self.toolbar_native:
                self.toolbar_native.Items.Clear()
            else:
                # The toolbar doesn't need to be positioned, because its `Dock` property
                # defaults to `Top`.
                self.toolbar_native = WinForms.ToolStrip()
                self.native.Controls.Add(self.toolbar_native)
                self.toolbar_native.Font = self.scale_font(DEFAULT_FONT)
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

                    item = WinForms.ToolStripButton(cmd.text)
                    item.AutoToolTip = False
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
