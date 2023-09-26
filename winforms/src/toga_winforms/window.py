import System.Windows.Forms as WinForms
from System.Drawing import Point, Size

from toga import GROUP_BREAK, SECTION_BREAK

from .container import Container
from .widgets.base import Scalable


class Window(Container, Scalable):
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        # Winforms close handling is caught on the FormClosing handler. To allow
        # for async close handling, we need to be able to abort this close
        # event, and then manually cause the close as part of the async result
        # handling. However, this then causes an is_closing event, which we need
        # to ignore. The `_is_closing` flag lets us easily identify if the
        # window is in the process of closing.
        self._is_closing = False

        self.native = WinForms.Form()
        self.native.interface = self.interface
        self.native._impl = self
        self.native.FormClosing += self.winforms_FormClosing
        super().__init__(self.native)
        self.init_scale(self.native)

        self.native.MinimizeBox = self.native.interface.minimizable

        self.set_title(title)
        self.set_size(size)
        self.set_position(position)

        self.toolbar_native = None
        self.toolbar_items = None

        self.native.Resize += lambda sender, args: self.resize_content()
        self.resize_content()  # Store initial size

        if not self.native.interface.resizeable:
            self.native.FormBorderStyle = self.native.FormBorderStyle.FixedSingle
            self.native.MaximizeBox = False

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
                    item.Click += cmd._impl.as_handler()
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
        size = self.native.ClientSize
        return tuple(map(self.scale_out, (size.Width, size.Height)))

    def set_size(self, size):
        self.native.ClientSize = Size(*map(self.scale_in, size))

    def set_app(self, app):
        if app is None:
            return
        icon_impl = app.interface.icon._impl
        if icon_impl is None:
            return
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

    def winforms_FormClosing(self, sender, event):
        # If the app is exiting, or a manual close has been requested, don't get
        # confirmation; just close.
        if not self.interface.app._impl._is_exiting and not self._is_closing:
            if not self.interface.closeable:
                # Window isn't closable, so any request to close should be cancelled.
                event.Cancel = True
            elif self.interface.on_close._raw:
                # If there is an on_close event handler, process it; but then cancel
                # the close event. If the result of on_close handling indicates the
                # window should close, then it will be manually triggered as part of
                # that result handling.
                self.interface.on_close(self)
                event.Cancel = True

    def set_full_screen(self, is_full_screen):
        if is_full_screen:
            self.native.FormBorderStyle = WinForms.FormBorderStyle(0)
            self.native.WindowState = WinForms.FormWindowState.Maximized
        else:
            self.native.FormBorderStyle = WinForms.FormBorderStyle(1)
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
