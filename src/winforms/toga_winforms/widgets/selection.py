from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget


class TogaComboBox(WinForms.ComboBox):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.DropDownStyle = WinForms.ComboBoxStyle.DropDownList
        self.SelectedIndexChanged += self.winforms_selected_index_changed

    def winforms_selected_index_changed(self, sender, event):
        if self.interface.on_select:
            self.interface.on_select(self.interface)


class Selection(Widget):
    def create(self):
        self.native = TogaComboBox(self.interface)

    def remove_all_items(self):
        self.native.Items.Clear()

    def add_item(self, item):
        self.native.Items.Add(item)

        # WinfForm.ComboBox does not select the first item, so it's done here.
        if not self.get_selected_item():
            self.native.SelectedIndex = 0

    def select_item(self, item):
        self.native.SelectedItem = item

    def get_selected_item(self):
        return self.native.SelectedItem

    def set_on_select(self, handler):
        pass

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
