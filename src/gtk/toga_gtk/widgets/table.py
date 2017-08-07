from gi.repository import Gtk
from .base import Widget


class Table(Widget):
    def create(self):
        self.data = Gtk.ListStore(*[str for h in self.interface.headings])
        # Create a table view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
        self.table = Gtk.TreeView(self.data)

        self.columns = []
        for heading in self.interface.headings:
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(heading, renderer, text=0)
            self.table.append_column(column)

        self.native = Gtk.ScrolledWindow()
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.native.add(self.table)
        self.native.set_min_content_width(200)
        self.native.set_min_content_height(200)
        self.native.interface = self.interface

    def insert(self, index, *data):
        if len(data) != len(self.interface.headings):
            raise Exception('Data size does not match number of headings')

        if index is None:
            self.data.append(data)
        else:
            self.data.insert(index, data)
