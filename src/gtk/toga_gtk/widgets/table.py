from gi.repository import Gtk
from .base import Widget


class Table(Widget):
    def create(self):
        self._connections = []

        self.data = Gtk.ListStore(*[str for h in self.interface.headings])
        # Create a table view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
        self.table = Gtk.TreeView(self.data)

        self.columns = []
        for i, heading in enumerate(self.interface.headings):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(heading, renderer, text=i)
            self.table.append_column(column)

        self.native = Gtk.ScrolledWindow()
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.native.add(self.table)
        self.native.set_min_content_width(200)
        self.native.set_min_content_height(200)
        self.native.interface = self.interface

    def refresh(self):
        self.data.clear()

        for row in self.interface.data.rows:
            self.data.append(row.data)

    def set_on_select(self, handler):

        for conn_id in self._connections:
            # Disconnect all other on_select handlers, so that if you reassign
            # the on_select, it doesn't trigger the old ones too.
            self.table.disconnect(conn_id)

        if handler is None:
            return

        def _handler(widget, *args):
            selection = widget.get_selection()
            selection.set_mode(Gtk.SelectionMode.SINGLE)
            tree_model, tree_iter = selection.get_selected()
            tree_path = tree_model.get_path(tree_iter)
            index = tree_path.get_indices()[0]

            handler(widget, row=index)

        self._connections.append(self.table.connect("cursor-changed", _handler))
