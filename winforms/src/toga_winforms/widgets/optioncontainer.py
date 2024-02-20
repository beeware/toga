from System.Windows.Forms import TabControl, TabPage

from ..container import Container
from ..libs.wrapper import WeakrefCallable
from .base import Widget


class OptionContainer(Widget):
    uses_icons = False

    def create(self):
        self.native = TabControl()
        self.native.Selected += WeakrefCallable(self.winforms_selected)
        self.panels = []

    def add_option(self, index, text, widget, icon):
        page = TabPage(text)
        self.native.TabPages.Insert(index, page)

        panel = Container(page)
        self.panels.insert(index, panel)
        panel.set_content(widget)

        # ClientSize is set correctly for a newly-added tab, but is only updated on
        # resize for the selected tab. And when the selection changes, the
        # newly-selected tab's ClientSize is not updated until some time after the
        # Selected event fires.
        self.resize_content(panel)

        page.ClientSizeChanged += WeakrefCallable(self.winforms_client_size_changed)

    def remove_option(self, index):
        panel = self.panels.pop(index)
        panel.clear_content()

        self.native.TabPages.RemoveAt(index)

    def set_option_enabled(self, index, enabled):
        """Winforms documentation states that Enabled is not meaningful for this
        control.

        Disabling option only disables the content of the tab, not the tab itself.
        """
        self.native.TabPages[index].Enabled = enabled

    def is_option_enabled(self, index):
        return self.native.TabPages[index].Enabled

    def set_option_text(self, index, value):
        self.native.TabPages[index].Text = value

    def get_option_text(self, index):
        return self.native.TabPages[index].Text

    def set_option_icon(self, index, value):  # pragma: nocover
        # This shouldn't ever be invoked, but it's included for completeness.
        pass

    def get_option_icon(self, index):
        # Icons aren't supported
        return None

    def get_current_tab_index(self):
        return self.native.SelectedIndex

    def set_current_tab_index(self, current_tab_index):
        self.native.SelectedIndex = current_tab_index

    def winforms_selected(self, sender, event):
        self.interface.on_select()

    def winforms_client_size_changed(self, sender, event):
        for panel in self.panels:
            self.resize_content(panel)

    def resize_content(self, panel):
        size = panel.native_parent.ClientSize
        panel.resize_content(size.Width, size.Height)
