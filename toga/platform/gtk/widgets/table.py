from __future__ import print_function, absolute_import, division

from gi.repository import Gtk

from .base import Widget


class Table(Widget):
    def __init__(self, headings):
        super(Table, self).__init__()
        self.headings = headings

        self._table = None
        self._columns = None
        self._data = Gtk.ListStore(*[str for h in headings])

        self.startup()

    def startup(self):
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

    def insert(self, index, *data):
        if len(data) != len(self.headings):
            raise Exception('Data size does not match number of headings')

        if index is None:
            self._data.append(data)
        else:
            self._data.insert(index, data)
