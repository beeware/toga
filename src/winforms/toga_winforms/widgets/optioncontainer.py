from toga_winforms.libs import WinForms
from toga_winforms.window import WinFormsViewport

from .base import Widget


class OptionContainer(Widget):
    def create(self):
        self.native = WinForms.TabControl()

    def add_content(self, label, widget):
        widget.viewport = WinFormsViewport(widget.native)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        item = WinForms.TabPage()
        item.Text = label

        # Enable AutoSize on the container to fill
        # the available space in the OptionContainer.
        widget.AutoSize = True

        item.Controls.Add(widget)

        self.native.Controls.Add(item)

    def set_on_select(self, handler):
        raise NotImplementedError()
