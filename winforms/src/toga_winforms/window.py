import System.Windows.Forms as WinForms
from System.Drawing import Point, Size

from toga import GROUP_BREAK, SECTION_BREAK

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

            for cmd in self.interface.toolbar:
                if cmd == GROUP_BREAK:
                    item = WinForms.ToolStripSeparator()
                elif cmd == SECTION_BREAK:
                    item = WinForms.ToolStripSeparator()
                else:
                    if cmd.icon is not None:
                        native_icon = cmd.icon._impl.native
                        item = WinForms.ToolStripMenuItem(
                            cmd.text, native_icon.ToBitmap()
                        )
                    else:
                        item = WinForms.ToolStripMenuItem(cmd.text)
                    item.Click += WeakrefCallable(cmd._impl.winforms_handler)
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
        return tuple(map(self.scale_out, (size.Width, size.Height)))

    def set_size(self, size):
        self.native.Size = Size(*map(self.scale_in, size))

    def set_app(self, app):
        icon_impl = app.interface.icon._impl
        self.native.Icon = icon_impl.native

    def get_title(self):
        return self.native.Text

    def set_title(self, title):
        self.native.Text = title

    def refreshed(self):
        super().refreshed()

        # Enforce a minimum window size. This takes into account the title bar and
        # borders, which are included in Size but not in ClientSize.
        decor_size = self.native.Size - self.native.ClientSize
        layout = self.interface.content.layout
        min_client_size = Size(
            self.scale_in(layout.min_width),
            self.scale_in(layout.min_height) + self.top_bars_height(),
        )
        self.native.MinimumSize = decor_size + min_client_size

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
                self.interface.on_close(None)
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
