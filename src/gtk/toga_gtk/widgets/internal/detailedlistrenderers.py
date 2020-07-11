import html

from toga_gtk.icons import Icon
from toga_gtk.libs import GdkPixbuf, Gtk, Pango


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
