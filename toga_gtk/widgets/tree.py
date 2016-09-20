from gi.repository import Gtk

from toga.interface import Tree as TreeInterface

from .base import WidgetMixin


class Tree(TreeInterface, WidgetMixin):
    def __init__(self, headings, id=None, style=None):
        super(Tree, self).__init__(headings, id=id, style=style)

        self._tree = None
        self._columns = None

        self._data = Gtk.TreeStore(*[str for h in headings])

        self._create()

    def create(self):
        # Create a tree view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self._table = Gtk.TreeView(self._data)

        self._columns = []
        for heading in self.headings:
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(heading, renderer, text=0)
            self._table.append_column(column)

        self._impl = Gtk.ScrolledWindow()
        self._impl.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self._impl.add(self._table)
        self._impl.set_min_content_width(200)
        self._impl.set_min_content_height(200)

    def insert(self, parent, index, *data):
        if len(data) != len(self.headings):
            raise Exception('Data size does not match number of headings')

        if index is None:
            node = self._data.append(parent, data)
        else:
            node = self._data.insert(parent, index, data)
        return node
