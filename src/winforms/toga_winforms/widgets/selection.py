from toga_winforms.libs import WinForms

from .base import Widget


class TogaComboBox(WinForms.ComboBox):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.SelectedIndexChanged += self.on_select

    def on_select(self, sender, event):
        if self.interface.on_select:
            self.interface.on_select(self.interface)


class Selection(Widget):
    def create(self):
        self.native = TogaComboBox(self.interface)

    def remove_all_items(self):
        self.native.Items.Clear()

    def add_item(self, item):
        self.native.Items.Add(item)

    def select_item(self, item):
        print('Item: ', item)
        index = self.native.FindString(item)
        self.native.SelectedItem = index

    def get_selected_item(self):
        return self.native.SelectedItem

    def set_on_select(self, handler):
        pass

    def rehint(self):
        self.interface.intrinsic.width = 120
        self.interface.intrinsic.height = 32
