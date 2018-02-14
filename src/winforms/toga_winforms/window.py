from travertino.layout import Viewport
from .libs import *


class WinFormsViewport:
    def __init__(self, native):
        self.native = native
        self.dpi = 96  # FIXME This is almost certainly wrong...

    @property
    def width(self):
        return self.native.ClientSize.Width

    @property
    def height(self):
        return self.native.ClientSize.Height


class Window:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        self.native = WinForms.Form(self)
        self.native.ClientSize = Size(self.interface._size[0], self.interface._size[1])
        self.native.Resize += self.on_resize

        self.toolbar_native = None
        self.toolbar_items = None

    def create_toolbar(self):
        self.toolbar_native = WinForms.ToolStrip()
        for cmd in self.interface.toolbar:
            if cmd == GROUP_BREAK:
                item = WinForms.ToolStripSeparator()
            elif cmd == SECTION_BREAK:
                item = WinForms.ToolStripSeparator()
            else:
                item = WinForms.ToolStripButton()
            self.toolbar_native.Items.Add(item)

    def set_position(self, position):
        pass

    def set_size(self, size):
        self.native.ClientSize = Size(self.interface._size[0], self.interface._size[1])

    def set_app(self, app):
        pass

    def set_content(self, widget):
        # If the content widget doesn't have a native, manifest a Panel as that native.
        if widget.native is None:
            widget.native = WinForms.Panel()

        # Construct the top-level layout, and set the window's view to
        # the be the widget's native object.
        if self.toolbar_native:
            self.native.Controls.Add(self.toolbar_native)

        self.native.Controls.Add(widget.native)

        # Set the widget's viewport to be based on the window's content.
        widget.viewport = WinFormsViewport(self.native)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

    def set_title(self, title):
        self.native.Text = title

    def show(self):
        # The first render of the content will establish the
        # minimum possible content size; use that to enforce
        # a minimum window size.
        TITLEBAR_HEIGHT = 36  # FIXME: this shouldn't be hard coded...

        # Now that the content is visible, we can do our initial hinting,
        # and use that as the basis for setting the minimum window size.
        self.interface.content._impl.rehint()
        self.interface.content.style.layout(self.interface.content, Viewport(0, 0))
        self.native.MinimumSize = Size(
            int(self.interface.content.layout.width),
            int(self.interface.content.layout.height) + TITLEBAR_HEIGHT
        )

    def on_close(self):
        pass

    def close(self):
        self.native.Close()

    def on_resize(self, sender, args):
        if self.interface.content:
            # Re-layout the content
            self.interface.content.refresh()

    def info_dialog(self, title, message):
        pass

    def question_dialog(self, title, message):
        pass

    def confirm_dialog(self, title, message):
        pass

    def error_dialog(self, title, message):
        pass

    def stack_trace_dialog(self, title, message, content, retry=False):
        pass

    def save_file_dialog(self, title, suggested_filename, file_types):
        pass
