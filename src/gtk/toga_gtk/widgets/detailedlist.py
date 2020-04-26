import html

from ..icons import Icon
from ..libs import Gdk, GdkPixbuf, Gtk, Pango
from .base import Widget


class DetailedList(Widget):
    """
    gtk DetailedList implementation.
    This is based on a Gtk.TreeView because the contents is still basic.
    Should the need arise for more complex contents (buttons on each row, etc.),
    we should use a Gtk.ListBox (see gtk3-demo).
    Also the model is a Gtk.ListStore. It may be more efficient to implement GtkTreeModel
    on top of the source directly instead of copying the data.
    """
    C_ITEM, C_PIXBUF, C_MARKUP = range(3)
    """ what is in the ListStore """

    def create(self):
        self.store = Gtk.ListStore(object, GdkPixbuf.Pixbuf, str)

        self.treeview = Gtk.TreeView(model=self.store)
        self.treeview.set_headers_visible(False)
        self.selection = self.treeview.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.selection.connect("changed", self.gtk_on_select)

        # single column with icon + markup
        column = Gtk.TreeViewColumn('')

        size = Icon.SIZES[0]
        iconcell = Gtk.CellRendererPixbuf()
        iconcell.set_property('width', size + 10)
        column.pack_start(iconcell, False)
        column.add_attribute(iconcell, 'pixbuf', self.C_PIXBUF)

        namecell = Gtk.CellRendererText()
        namecell.set_property('ellipsize', Pango.EllipsizeMode.END)
        column.pack_start(namecell, True)
        column.add_attribute(namecell, 'markup', self.C_MARKUP)

        self.treeview.append_column(column)

        self.native = Gtk.ScrolledWindow()
        self.native.interface = self.interface
        # same scrolling policies as in the tree widget
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.native.add(self.treeview)
        self.native.set_min_content_width(self.interface.MIN_WIDTH)
        self.native.set_min_content_height(self.interface.MIN_HEIGHT)

    def change_source(self, source):
        self.treeview.set_model(None)

        self.store.clear()
        for i, node in enumerate(self.interface.data):
            self.insert(i, node)

        self.treeview.set_model(self.store)

    def insert(self, index, item):
        impl = self.store.insert(
            index,
            self.row_data(item)
        )
        try:
            item._impl[self] = impl
        except AttributeError:
            item._impl = {self: impl}

    def change(self, item):
        self.store[item._impl[self]] = self.row_data(item)

    def remove(self, item):
        del self.store[item._impl[self]]
        del item._impl[self]

    def clear(self):
        self.store.clear()

    def set_on_refresh(self, handler):
        pass

    def after_on_refresh(self):
        # No special handling required
        pass

    def set_on_select(self, handler):
        # No special handling required
        pass

    def set_on_delete(self, handler):
        pass

    def scroll_to_row(self, row):
        path = Gtk.TreePath.new_from_indices([row])
        print(path)
        # to verify actual effect, set row_align=0 to let it move to top
        # self.treeview.scroll_to_cell(path, None, use_align=True, row_align=0., col_align=0.)
        self.treeview.scroll_to_cell(path)

    def row_data(self, item):
        pixbuf = None
        if item.icon and item.icon.bind(self.interface.factory):
            pixbuf = getattr(item.icon.bind(self.interface.factory), 'native_%i' % Icon.SIZES[0]).get_pixbuf()
        markup = ''.join([
            html.escape(item.title or ''), '\n',
            '<small>', html.escape(item.subtitle or ''), '</small>'
        ])
        return [item, pixbuf, markup]

    def gtk_on_select(self, selection):
        if self.interface.on_select:
            tree_model, tree_iter = selection.get_selected()
            if tree_iter:
                node = tree_model.get(tree_iter, 0)[0]
            else:
                node = None
            self.interface._selection = node
            self.interface.on_select(None, node=node)
