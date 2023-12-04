import System.Windows.Forms as WinForms
from System.Drawing import Bitmap, Graphics, Point, Size
from System.Drawing.Imaging import ImageFormat
from System.IO import MemoryStream

from toga.command import Separator

from .container import Container
from .libs.wrapper import WeakrefCallable
from .widgets.base import Scalable


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
        self.set_position(position)

        self.toolbar_native = None

        self.native.Resize += WeakrefCallable(self.winforms_Resize)
        self.resize_content()  # Store initial size

        self.set_full_screen(self.interface.full_screen)

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

    def get_position(self):
        location = self.native.Location
        return tuple(map(self.scale_out, (location.X, location.Y)))

    def set_position(self, position):
        self.native.Location = Point(*map(self.scale_in, position))

    def get_size(self):
        size = self.native.Size
        return (
            self.scale_out(size.Width - self.decor_width()),
            self.scale_out(size.Height - self.decor_height()),
        )

    def set_size(self, size):
        width, height = size
        self.native.Size = Size(
            self.scale_in(width) + self.decor_width(),
            self.scale_in(height) + self.decor_height(),
        )

    def set_app(self, app):
        icon_impl = app.interface.icon._impl
        self.native.Icon = icon_impl.native

    def get_title(self):
        return self.native.Text

    def set_title(self, title):
        self.native.Text = title

    def refreshed(self):
        super().refreshed()
        layout = self.interface.content.layout
        self.native.MinimumSize = Size(
            self.scale_in(layout.min_width) + self.decor_width(),
            self.scale_in(layout.min_height)
            + self.top_bars_height()
            + self.decor_height(),
        )

    def show(self):
        if self.interface.content is not None:
            self.interface.content.refresh()
        if self.interface is not self.interface.app._main_window:
            self.native.Icon = self.interface.app.icon._impl.native
        self.native.Show()

    def hide(self):
        self.native.Hide()

    def get_visible(self):
        return self.native.Visible

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

    def set_full_screen(self, is_full_screen):
        if is_full_screen:
            self.native.FormBorderStyle = getattr(WinForms.FormBorderStyle, "None")
            self.native.WindowState = WinForms.FormWindowState.Maximized
        else:
            self.native.FormBorderStyle = getattr(
                WinForms.FormBorderStyle,
                "Sizable" if self.interface.resizable else "FixedSingle",
            )
            self.native.WindowState = WinForms.FormWindowState.Normal

    def close(self):
        self._is_closing = True
        self.native.Close()

    # "Decor" includes the title bar and the (usually invisible) resize borders. It does
    # not include the menu bar and toolbar, which are included in the ClientSize (see
    # top_bars_height).
    def decor_width(self):
        return self.native.Size.Width - self.native.ClientSize.Width

    def decor_height(self):
        return self.native.Size.Height - self.native.ClientSize.Height

    def top_bars_height(self):
        vertical_shift = 0
        if self.toolbar_native:
            vertical_shift += self.toolbar_native.Height
        if self.native.MainMenuStrip:
            vertical_shift += self.native.MainMenuStrip.Height
        return vertical_shift

    def resize_content(self):
        vertical_shift = self.top_bars_height()
        self.native_content.Location = Point(0, vertical_shift)
        super().resize_content(
            self.native.ClientSize.Width,
            self.native.ClientSize.Height - vertical_shift,
        )

    def get_image_data(self):
        size = Size(self.native_content.Size.Width, self.native_content.Size.Height)
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
