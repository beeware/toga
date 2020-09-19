from toga_winforms.libs import WinForms

from .base import Widget


class Tree(Widget):
    def create(self):
        self.native = WinForms.TreeView()

    def row_data(self, item):
        self.interface.factory.not_implemented('Tree.row_data()')

    def on_select(self, selection):
        self.interface.factory.not_implemented('Tree.on_select()')

    def change_source(self, source):
        self.interface.factory.not_implemented('Tree.change_source()')

    def insert(self, parent, index, item):
        self.interface.factory.not_implemented('Tree.insert()')

    def change(self, item):
        self.interface.factory.not_implemented('Tree.change()')

    def remove(self, parent, index, item):
        self.interface.factory.not_implemented('Tree.remove()')

    def clear(self):
        self.interface.factory.not_implemented('Tree.clear()')

    def get_selection(self):
        self.interface.factory.not_implemented('Tree.get_selection()')

    def set_on_select(self, handler):
        self.interface.factory.not_implemented('Tree.set_on_select()')

    def set_on_double_click(self, handler):
        self.interface.factory.not_implemented('Table.set_on_double_click()')

    def scroll_to_node(self, node):
        self.interface.factory.not_implemented('Tree.scroll_to_node()')
