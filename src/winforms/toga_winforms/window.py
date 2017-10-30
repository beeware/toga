from .libs import *

from .container import Container
from . import dialogs
# from .command import SEPARATOR, SPACER, EXPANDING_SPACER



class Window:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.container = None
        self.create()

    def create(self):
        self.native = WinForms.Form(self)
        self.native.ClientSize = Size(self.interface._size[0], self.interface._size[1])
        self.native.Resize += self._on_resize

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
        pass

    def set_app(self, app):
        pass

    def set_content(self, widget):
        if widget.native is None:
            self.container = Container()
            self.container.content = widget
        else:
            self.container = widget

        if self.toolbar_native:
            self.native.Controls.Add(self.toolbar_native)

        self.native.Controls.Add(self.container.native)

    def set_title(self, title):
        self.native.Text = title

    def show(self):
        # The first render of the content will establish the
        # minimum possible content size; use that to enforce
        # a minimum window size.
        TITLEBAR_HEIGHT = 36  # FIXME: this shouldn't be hard coded...
        self.native.MinimumSize = Size(
            int(self.interface.content.layout.width),
            int(self.interface.content.layout.height) + TITLEBAR_HEIGHT
        )

        # Set the size of the container to be the same as the window
        self.container.native.Size = self.native.ClientSize

        # Do the first layout render.
        self.container.update_layout(
            width=self.native.ClientSize.Width,
            height=self.native.ClientSize.Height,
        )

    def on_close(self):
        pass

    def close(self):
        self.native.Close()

    def _on_resize(self, sender, args):
        if self.interface.content:
            # Set the size of the container to be the same as the window
            self.container.native.Size = self.native.ClientSize
            # Re-layout the content
            self.interface.content._update_layout(
                width=sender.ClientSize.Width,
                height=sender.ClientSize.Height,
            )

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
