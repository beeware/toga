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

    def insert(self, parent, index, item, **kwargs):
        self.interface.factory.not_implemented('Tree.insert()')

    def change(self, item):
        self.interface.factory.not_implemented('Tree.change()')

    def remove(self, item):
        self.interface.factory.not_implemented('Tree.remove()')

    def clear(self):
        self.interface.factory.not_implemented('Tree.clear()')

    def set_on_select(self, handler):
        self.interface.factory.not_implemented('Tree.set_on_select()')

    def scroll_to_node(self, node):
        self.interface.factory.not_implemented('Tree.scroll_to_node()')
