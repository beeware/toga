from toga import GROUP_BREAK, SECTION_BREAK

from .libs import Point, Size, WinForms


class WinFormsViewport:
    def __init__(self, native, frame):
        self.native = native
        self.frame = frame
        self.baseline_dpi = 96

    @property
    def width(self):
        # Treat `native=None` as a 0x0 viewport
        if self.native is None:
            return 0
        return self.native.ClientSize.Width

    @property
    def height(self):
        if self.native is None:
            return 0
        # Subtract any vertical shift of the frame. This is to allow
        # for toolbars, or any other viewport-level decoration.
        return self.native.ClientSize.Height - self.frame.vertical_shift

    @property
    def dpi(self):
        if self.native is None:
            return self.baseline_dpi
        return self.native.CreateGraphics().DpiX


class Window:
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
        self.native.FormClosing += self.winforms_FormClosing

        self.native.MinimizeBox = self.native.interface.minimizable

        self.set_title(title)
        self.set_size(size)
        self.set_position(position)

        self.toolbar_native = None
        self.toolbar_items = None
        if self.native.interface.resizeable:
            self.native.Resize += self.winforms_resize
        else:
            self.native.FormBorderStyle = self.native.FormBorderStyle.FixedSingle
            self.native.MaximizeBox = False

    def create_toolbar(self):
        self.toolbar_native = WinForms.ToolStrip()
        for cmd in self.interface.toolbar:
            if cmd == GROUP_BREAK:
                item = WinForms.ToolStripSeparator()
            elif cmd == SECTION_BREAK:
                item = WinForms.ToolStripSeparator()
            else:
                if cmd.icon is not None:
                    native_icon = cmd.icon._impl.native
                    item = WinForms.ToolStripMenuItem(cmd.text, native_icon.ToBitmap())
                else:
                    item = WinForms.ToolStripMenuItem(cmd.text)
                item.Click += cmd._impl.as_handler()
                cmd._impl.native.append(item)
            self.toolbar_native.Items.Add(item)

    def get_position(self):
        return (self.native.Location.X, self.native.Location.Y)

    def set_position(self, position):
        self.native.Location = Point(*position)

    def get_size(self):
        return (self.native.ClientSize.Width, self.native.ClientSize.Height)

    def set_size(self, size):
        self.native.ClientSize = Size(*size)

    def set_app(self, app):
        if app is None:
            return
        icon_impl = app.interface.icon._impl
        if icon_impl is None:
            return
        self.native.Icon = icon_impl.native

    @property
    def vertical_shift(self):
        # vertical shift is the toolbar height or 0
        result = 0
        try:
            result += self.native.interface._impl.toolbar_native.Height
        except AttributeError:
            pass
        try:
            result += self.native.interface._impl.native.MainMenuStrip.Height
        except AttributeError:
            pass
        return result

    def clear_content(self):
        if self.interface.content:
            for child in self.interface.content.children:
                child._impl.container = None

    def set_content(self, widget):
        has_content = False
        for control in self.native.Controls:
            # The main menu and toolbar are normal in-window controls;
            # however, they shouldn't be removed if window content is
            # removed.
            if control != self.native.MainMenuStrip and control != self.toolbar_native:
                has_content = True
                self.native.Controls.Remove(control)

        # The first time content is set for the window, we also need
        # to add the toolbar as part of the main window content.
        # We use "did we haev to remove any content" as a marker for
        # whether this is the first time we're setting content.
        if not has_content:
            self.native.Controls.Add(self.toolbar_native)

        # Add the actual window content.
        self.native.Controls.Add(widget.native)

        # Set the widget's viewport to be based on the window's content.
        widget.viewport = WinFormsViewport(native=self.native, frame=self)
        widget.frame = self

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

    def get_title(self):
        return self.native.Text

    def set_title(self, title):
        self.native.Text = title

    def show(self):
        # The first render of the content will establish the
        # minimum possible content size; use that to enforce
        # a minimum window size.
        TITLEBAR_HEIGHT = WinForms.SystemInformation.CaptionHeight
        # Now that the content is visible, we can do our initial hinting,
        # and use that as the basis for setting the minimum window size.
        self.interface.content._impl.rehint()
        self.interface.content.style.layout(
            self.interface.content,
            WinFormsViewport(native=None, frame=None),
        )
        self.native.MinimumSize = Size(
            int(self.interface.content.layout.width),
            int(self.interface.content.layout.height) + TITLEBAR_HEIGHT
        )
        self.interface.content.refresh()

        if self.interface is not self.interface.app._main_window:
            self.native.Icon = self.interface.app.icon.bind(self.interface.factory).native
        self.native.Show()

    def hide(self):
        self.native.Hide()

    def get_visible(self):
        return self.native.Visible

    def winforms_FormClosing(self, sender, event):
        # If the app is exiting, or a manual close has been requested,
        # don't get confirmation; just close.
        if not self.interface.app._impl._is_exiting and not self._is_closing:
            if not self.interface.closeable:
                # Closeability is implemented by shortcutting the close handler.
                event.Cancel = True
            elif self.interface.on_close:
                # If there is an on_close event handler, process it;
                # but then cancel the close event. If the result of
                # on_close handling indicates the window should close,
                # then it will be manually triggered as part of that
                # result handling.
                self.interface.on_close(self)
                event.Cancel = True

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented('Window.set_full_screen()')

    def set_on_close(self, handler):
        pass

    def close(self):
        self._is_closing = True
        self.native.Close()

    def winforms_resize(self, sender, args):
        if self.interface.content:
            # Re-layout the content
            self.interface.content.refresh()
