from System.Windows.Forms import TabControl

from .base import SimpleProbe


class OptionContainerProbe(SimpleProbe):
    native_class = TabControl
    disabled_tab_selectable = True

    def select_tab(self, index):
        self.native.SelectedIndex = index

    def tab_enabled(self, index):
        return self.native.TabPages[index].Enabled
