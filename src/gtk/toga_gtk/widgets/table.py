from gi.repository import Gtk

from toga.interface import Table as TableInterface

from .base import WidgetMixin


class Table(TableInterface, WidgetMixin):
    def __init__(self, headings, id=None, style=None):
        super(Table, self).__init__(headings, id=id, style=style)
        self._create()

    def create(self):
        self._data = Gtk.ListStore(*[str for h in self.headings])
        # Create a table view, and put it in a scroll view.
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
        self._impl._interface = self

    def insert(self, index, *data):
        if len(data) != len(self.headings):
            raise Exception('Data size does not match number of headings')

        if index is None:
            self._data.append(data)
        else:
            self._data.insert(index, data)
