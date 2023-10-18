from System.Windows.Forms import TabControl, TabPage
from travertino.size import at_least

from ..container import Container
from ..libs.wrapper import WeakrefCallable
from .base import Widget


class OptionContainer(Widget):
    def create(self):
        self.native = TabControl()
        self.native.Selected += WeakrefCallable(self.winforms_selected)
        self.panels = []

    def add_content(self, index, text, widget):
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

    def remove_content(self, index):
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

    def get_current_tab_index(self):
        return self.native.SelectedIndex

    def set_current_tab_index(self, current_tab_index):
        self.native.SelectedIndex = current_tab_index

    def winforms_selected(self, sender, event):
        self.interface.on_select(None)

    def winforms_client_size_changed(self, sender, event):
        for panel in self.panels:
            self.resize_content(panel)

    def resize_content(self, panel):
        size = panel.native_parent.ClientSize
        panel.resize_content(size.Width, size.Height)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
