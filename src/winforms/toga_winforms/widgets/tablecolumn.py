from toga_winforms.libs import WinForms

from .base import Widget


class Column(Widget):
    def create(self):
        self.native = WinForms.ColumnHeader()

    def set_editable(self, value):
        pass

    def set_title(self, value):
        self.native.Text = value

    def set_on_toggle(self, handler):
        pass

    def set_on_change(self, handler):
        pass
