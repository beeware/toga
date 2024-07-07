from __future__ import annotations

from typing import TYPE_CHECKING

import System.Windows.Forms as WinForms
from System.ComponentModel import InvalidEnumArgumentException
from System.Drawing import Bitmap, Graphics, Point, Size as WinSize
from System.Drawing.Imaging import ImageFormat
from System.IO import MemoryStream

from toga.command import Separator
from toga.constants import WindowState
from toga.types import Position, Size

from .container import Container
from .keys import toga_to_winforms_key, toga_to_winforms_shortcut
from .libs.wrapper import WeakrefCallable
from .screens import Screen as ScreenImpl
from .widgets.base import Scalable

if TYPE_CHECKING:  # pragma: no cover
    from toga.types import PositionT, SizeT


class Window(Container, Scalable):
    def __init__(self, interface, title, position, size):
        self.interface = interface

        self.create()

        self._FormClosing_handler = WeakrefCallable(self.winforms_FormClosing)
        self.native.FormClosing += self._FormClosing_handler
        super().__init__(self.native)
        self.init_scale(self.native)

        self.native.MinimizeBox = self.interface.minimizable
        self.native.MaximizeBox = self.interface.resizable

        # Use a shadow variable since a window without any app menu and toolbar
        # in presentation mode would be indistinguishable from full screen mode.
        self._is_presentation_mode = False

        self.set_title(title)
        self.set_size(size)
        # Winforms does window cascading by default; use that behavior, rather than
        # Toga's re-implementation.
        if position:
            self.set_position(position)

        self.native.Resize += WeakrefCallable(self.winforms_Resize)
        self.resize_content()  # Store initial size

        # Set window border style based on whether window resizability is enabled or not.
        self.native.FormBorderStyle = getattr(
            WinForms.FormBorderStyle,
            "Sizable" if self.interface.resizable else "FixedSingle",
        )

    def create(self):
        self.native = WinForms.Form()

    ######################################################################
    # Native event handlers
    ######################################################################

    def winforms_Resize(self, sender, event):
        self.resize_content()

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
                if self._is_presentation_mode:
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
        current_state = self.get_window_state()
        if current_state == state:
            return
        if (
            current_state != WindowState.NORMAL
            and state != WindowState.NORMAL
            and (getattr(self, "_pending_window_state_transition", None) is None)
        ):
            # Set Window state to NORMAL before changing to other states as some
            # states block changing window state without first exiting them or
            # can even cause rendering glitches.
            self._pending_window_state_transition = state
            self.set_window_state(WindowState.NORMAL)

        elif state == WindowState.MAXIMIZED:
            self.native.WindowState = WinForms.FormWindowState.Maximized

        elif state == WindowState.MINIMIZED:
            self.native.WindowState = WinForms.FormWindowState.Minimized

        elif state == WindowState.FULLSCREEN:
            self.native.FormBorderStyle = getattr(WinForms.FormBorderStyle, "None")
            self.native.WindowState = WinForms.FormWindowState.Maximized

        elif state == WindowState.PRESENTATION:
            self._before_presentation_mode_screen = self.interface.screen
            if self.native.MainMenuStrip:
                self.native.MainMenuStrip.Visible = False
            if getattr(self, "toolbar_native", None):
                self.toolbar_native.Visible = False
            self.native.FormBorderStyle = getattr(WinForms.FormBorderStyle, "None")
            self.native.WindowState = WinForms.FormWindowState.Maximized
            self._is_presentation_mode = True

        # WindowState.NORMAL case:
        else:
            if current_state == WindowState.PRESENTATION:
                if self.native.MainMenuStrip:
                    self.native.MainMenuStrip.Visible = True
                if getattr(self, "toolbar_native", None):
                    self.toolbar_native.Visible = True

                self.interface.screen = self._before_presentation_mode_screen
                del self._before_presentation_mode_screen
                self._is_presentation_mode = False

            self.native.FormBorderStyle = getattr(
                WinForms.FormBorderStyle,
                "Sizable" if self.interface.resizable else "FixedSingle",
            )
            self.native.WindowState = WinForms.FormWindowState.Normal
            # Complete any pending window state transition.
            if getattr(self, "_pending_window_state_transition", None) is not None:
                self.set_window_state(self._pending_window_state_transition)
                del self._pending_window_state_transition

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

    def _top_bars_height(self):
        vertical_shift = 0
        if self.toolbar_native and self.toolbar_native.Visible:
            vertical_shift += self.toolbar_native.Height
        if self.native.MainMenuStrip and self.native.MainMenuStrip.Visible:
            vertical_shift += self.native.MainMenuStrip.Height
        return vertical_shift

    def _submenu(self, group, menubar):
        try:
            return self._menu_groups[group]
        except KeyError:
            if group is None:
                submenu = menubar
            else:
                parent_menu = self._submenu(group.parent, menubar)

                submenu = WinForms.ToolStripMenuItem(group.text)

                # Top level menus are added in a different way to submenus
                if group.parent is None:
                    parent_menu.Items.Add(submenu)
                else:
                    parent_menu.DropDownItems.Add(submenu)

            self._menu_groups[group] = submenu
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
            menubar.SendToBack()  # In a dock, "back" means "top".

        self._menu_groups = {}

        submenu = None
        for cmd in self.interface.app.commands:
            submenu = self._submenu(cmd.group, menubar)
            if isinstance(cmd, Separator):
                submenu.DropDownItems.Add("-")
            else:
                submenu = self._submenu(cmd.group, menubar)
                item = WinForms.ToolStripMenuItem(cmd.text)
                item.Click += WeakrefCallable(cmd._impl.winforms_Click)
                if cmd.shortcut is not None:
                    try:
                        item.ShortcutKeys = toga_to_winforms_key(cmd.shortcut)
                        # The Winforms key enum is... daft. The "oem" key
                        # values render as "Oem" or "Oemcomma", so we need to
                        # *manually* set the display text for the key shortcut.
                        item.ShortcutKeyDisplayString = toga_to_winforms_shortcut(
                            cmd.shortcut
                        )
                    except (
                        ValueError,
                        InvalidEnumArgumentException,
                    ) as e:  # pragma: no cover
                        # Make this a non-fatal warning, because different backends may
                        # accept different shortcuts.
                        print(f"WARNING: invalid shortcut {cmd.shortcut!r}: {e}")

                item.Enabled = cmd.enabled

                cmd._impl.native.append(item)
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
