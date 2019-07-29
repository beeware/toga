from toga_winforms.libs import WinForms
from .base import Widget


class DetailedList(Widget):
    # Create the ListBox WinForms Widget
    def create(self):
        self._container = self
        self.native = WinForms.ListBox()

        self.native.SelectionMode = WinForms.SelectionMode.MultiExtended


    # Change the source of the Widget
    def change_source(self, source):
        self.native.Items.Clear()
        for i, row in enumerate(self.interface._data):
            item = ([
                getattr(row, attr) for attr in row._attrs
            ])
            self.native.Items.Insert(i, item[0])
            

    def set_on_refresh(self, handler):
        #doesnt exist for a listbox
        pass

    def after_on_refresh(self):
        #refresh doesnt exist for a listbox
        pass

    def set_on_delete(self, handler):
        #doesnt exist for a listbox
        pass

    def set_on_select(self, handler):
        if handler is None:
            pass
        else:
            self.native.SelectedIndexChanged += self.interface._on_select

    def scroll_to_row(self, row):
        self.native.SelectedItem = self.native.Items[row]
