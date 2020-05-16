from toga_winforms.libs import WinForms
from toga_winforms.window import WinFormsViewport

from .base import Widget


class OptionContainer(Widget):
    def create(self):
        self.native = WinForms.TabControl()

    def add_content(self, label, widget):
        widget.viewport = WinFormsViewport(self.native, self)
        widget.frame = self
        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        item = WinForms.TabPage()
        item.Text = label

        # Enable AutoSize on the container to fill
        # the available space in the OptionContainer.
        widget.AutoSize = True

        item.Controls.Add(widget.native)
        self.native.Controls.Add(item)

    def remove_content(self, index):
        self.interface.factory.not_implemented('OptionContainer.remove_content()')

    def set_on_select(self, handler):
        self.interface.factory.not_implemented('OptionContainer.set_on_select()')

    def set_option_enabled(self, index, value):
        self.interface.factory.not_implemented('OptionContainer.is_option_enabled()')

    def is_option_enabled(self, index):
        self.interface.factory.not_implemented('OptionContainer.is_option_enabled()')

    def set_option_label(self, index, value):
        self.interface.factory.not_implemented('OptionContainer.set_option_label()')

    def get_option_label(self, index):
        self.interface.factory.not_implemented('OptionContainer.get_option_label()')
