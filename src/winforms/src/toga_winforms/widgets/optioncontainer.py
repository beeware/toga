from toga_winforms.libs import WinForms
from toga_winforms.window import WinFormsViewport

from .base import Widget


class OptionContainer(Widget):
    def create(self):
        self.native = WinForms.TabControl()
        self.native.Selected += self.winforms_selected

    def add_content(self, index, text, widget):
        widget.viewport = WinFormsViewport(self.native, self)
        widget.frame = self
        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        item = WinForms.TabPage()
        item.Text = text

        # Enable AutoSize on the container to fill
        # the available space in the OptionContainer.
        widget.AutoSize = True

        item.Controls.Add(widget.native)
        if index < self.native.TabPages.Count:
            self.native.TabPages.Insert(index, item)
        else:
            self.native.TabPages.Add(item)

    def remove_content(self, index):
        tab_page = self.native.TabPages[index]
        self.native.TabPages.Remove(self.native.TabPages[index])
        tab_page.Dispose()

    def set_on_select(self, handler):
        pass

    def set_option_enabled(self, index, enabled):
        """
        Winforms documentation states that Enabled is not meaningful for this control.
        Disabling option only disables the content of the tab, not the tab itself.
        """
        self.native.TabPages[index].Enabled = enabled

    def is_option_enabled(self, index):
        return self.native.TabPages[index].Enabled

    def set_option_text(self, index, value):
        self.native.TabPages[index].Text = value

    def get_option_text(self, index):
        return self.native.TabPages[index].Text

    def get_current_tab_index(self):
        return self.native.SelectedIndex

    def set_current_tab_index(self, current_tab_index):
        self.native.SelectedIndex = current_tab_index

    def winforms_selected(self, sender, event):
        if self.interface.on_select:
            self.interface.on_select(
                self.interface,
                option=self.interface.content[self.native.SelectedIndex]
            )

    def set_font(self, font):
        if font:
            self.native.Font = font.bind(self.interface.factory).native
