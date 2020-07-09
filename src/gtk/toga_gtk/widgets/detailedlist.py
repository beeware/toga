import html

from ..icons import Icon
from ..libs import GdkPixbuf, Gtk, Pango
from .base import Widget
from .sourcetreemodel import SourceTreeModel


class DetailedListRenderer:
    """ Implement this in layout variations, since they are related """

    def __init__(self, interface):
        self.interface = interface

    def row_field_types(self):
        """ return column type tuple """

    def create_columns(self, treeview):
        """ to create column(s) """
        raise NotImplementedError("implement create_columns")

    @staticmethod
    def icon_size():
        return Icon.SIZES[0]

    @classmethod
    def pixbuf(clazz, interface, icon):
        pixbuf = None
        # TODO: see get_scale_factor() to choose 72 px on hidpi
        if icon and icon.bind(interface.factory):
            pixbuf = getattr(icon.bind(interface.factory), 'native_%i' % clazz.icon_size()).get_pixbuf()
        return pixbuf


class IconTextRenderer(DetailedListRenderer):
    """ DetailedList customization (choose to render icon/title/subtitle) """
    ICON, TITLE, TITLE_SUBTITLE = range(3)
    """ """
    STYLES = {
        'default': [ICON, TITLE_SUBTITLE],
        'icon-title-subtitle': [ICON, TITLE_SUBTITLE],
        'icon-title': [ICON, TITLE],
        'title-icon': [TITLE, ICON],
        'title-subtitle-icon': [TITLE_SUBTITLE, ICON],
        'title-subtitle': [TITLE_SUBTITLE],
        'title': [TITLE],
        'icon': [ICON],
    }

    def __init__(self, interface, fields=None):
        super().__init__(interface)
        if fields is None:
            fields = self.STYLES['default']
        self.fields = fields

    def row_field_types(self):
        ret = [object]
        for f in self.fields:
            if f == self.ICON:
                ret.append(GdkPixbuf.Pixbuf)
            elif f in (self.TITLE, self.TITLE_SUBTITLE):
                ret.append(str)
        return ret

    def row_columns(self):
        ret = []
        for f in self.fields:
            if f == self.ICON:
                ret.append({
                    'type': GdkPixbuf.Pixbuf,
                    'attr': 'icon',
                })
            elif f in (self.TITLE, self.TITLE_SUBTITLE):
                ret.append({
                    'type': str,
                    'attr': 'title',
                })
                ret.append(str)
        return ret

    def create_columns(self, treeview):
        # single column with icon + markup (dep. on init options)
        column = Gtk.TreeViewColumn('')
        row_data_index = 1  # first element in the row is always the item itself

        for i, f in enumerate(self.fields):
            if f == self.ICON:
                iconcell = Gtk.CellRendererPixbuf()
                iconcell.set_property('width', self.icon_size() + 10)
                column.set_cell_data_func(iconcell, self.icon, i)
                column.pack_start(iconcell, False)
            elif f == self.TITLE:
                namecell = Gtk.CellRendererText()
                namecell.set_property('ellipsize', Pango.EllipsizeMode.END)
                column.pack_start(namecell, True)
                column.add_attribute(namecell, 'text', row_data_index)
            elif f == self.TITLE_SUBTITLE:
                namecell = Gtk.CellRendererText()
                namecell.set_property('ellipsize', Pango.EllipsizeMode.END)
                column.set_cell_data_func(namecell, self.markup, i)
                column.pack_start(namecell, True)
            row_data_index += 1

        treeview.append_column(column)

    @staticmethod
    def markup(tree_column, cell, tree_model, iter_, index):
        item = tree_model.do_get_value(iter_, 0)
        markup = [
            html.escape(item.title or ''),
            '\n',
            '<small>', html.escape(item.subtitle or ''), '</small>',
        ]
        cell.set_property('markup', ''.join(markup))

    def icon(self, tree_column, cell, tree_model, iter_, index):
        item = tree_model.do_get_value(iter_, 0)
        cell.set_property('pixbuf', self.pixbuf(self.interface, item.icon))

    @classmethod
    def from_style(clazz, interface, style='default'):
        return clazz(interface, fields=clazz.STYLES.get(style))


class DetailedList(Widget):
    """
    gtk DetailedList implementation.
    This is based on a Gtk.TreeView because the contents is still basic.
    Should the need arise for more complex contents (buttons on each row, etc.),
    we should use a Gtk.ListBox (see gtk3-demo).
    """

    def create(self):
        self.renderer = IconTextRenderer.from_style(self.interface)

        self.store = SourceTreeModel(self.renderer.row_columns(), is_tree=False)

        self.treeview = Gtk.TreeView(model=self.store)
        self.treeview.set_headers_visible(False)
        self.selection = self.treeview.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.selection.connect("changed", self.gtk_on_select)

        self.renderer.create_columns(self.treeview)

        self.native = Gtk.ScrolledWindow()
        self.native.interface = self.interface
        # same scrolling policies as in the tree widget
        self.native.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.native.add(self.treeview)
        self.native.set_min_content_width(self.interface.MIN_WIDTH)
        self.native.set_min_content_height(self.interface.MIN_HEIGHT)

    def change_source(self, source):
        self.treeview.set_model(None)
        self.store.change_source(source)
        for i, node in enumerate(source):
            self.insert(i, node)

        self.treeview.set_model(self.store)

    def insert(self, index, item):
        self.store.insert(item)

    def change(self, item):
        self.store.change(item)

    def remove(self, item, index):
        self.store.remove(item, index)

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

    def gtk_on_select(self, selection):
        if self.interface.on_select:
            tree_model, tree_iter = selection.get_selected()
            if tree_iter:
                node = tree_model.get(tree_iter, 0)[0]
            else:
                node = None
            # FIXME: shouldn't DetailedList have a _selection attribute like Tree?
            #self.interface._selection = node
            self.interface.on_select(self.interface, row=node)
