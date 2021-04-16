import html

from toga_gtk.libs import Gtk
from toga_gtk.icons import Icon


class TextIconRow(Gtk.ListBoxRow):
    """
    Create a TextIconRow from a toga.sources.Row.
    A reference to the original row is kept in self.row, this is useful for comparisons.
    """
    def __init__(self, row, interface, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We need to wait until this widget is allocated to scroll it in,
        # for that we use signal and callbacks. The handler_is of the
        # signal is used to disconnect and we store it here.
        self._scroll_handler_id_value = None

        self.interface = interface
        self.row = row
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
      
        self.text = Gtk.Label(xalign=0)
        text_markup = self.markup(row)
        self.text.set_markup(text_markup)

        self.icon = self.get_icon(self.row)

        self.vbox.pack_start(self.text, True, True, 0)
        
        self.hbox.pack_start(self.icon, False, False, 6)
        self.hbox.pack_start(self.vbox, True, True, 0)

        self.add(self.hbox)

    def get_icon(self, row):
        row.icon.bind(self.interface.factory)
        # TODO: see get_scale_factor() to choose 72 px on hidpi
        return getattr(self.row.icon._impl, "native_" + str(32))

    @staticmethod
    def markup(row):
        markup = [
            html.escape(row.title or ''),
            '\n',
            '<small>', html.escape(row.subtitle or ''), '</small>',
        ]
        return ''.join(markup)

    def scroll_to_center(self):
        """
        Scrolls the parent Gtk.ListBox until child is in the center of the
        view.
        """
        # Wait for 'size-allocate' because we will need the
        # dimensions of the widget. At this point 
        # widget.size_request is already available but that's
        # only the requested size, not the size it will get.
        self._scroll_handler_id = self.connect(
            'size-allocate',
            # We don't need 'wdiget' and 'gpointer'
            lambda widget, gpointer: self._do_scroll_to_center()
            )

    def _do_scroll_to_center(self):
        # Disconnect the from the signal that called us
        self._scroll_handler_id = None

        list_box = self.get_parent()

        adj = list_box.get_adjustment()
        page_size = adj.get_page_size()

        # 'height' and 'y' are always valid because we are
        # being called after 'size-allocate'
        height = self.get_allocation().height
        _, y = self.translate_coordinates(list_box, 0, 0)

        adj.set_value(y - (page_size - height)/2)

    @property
    def _scroll_handler_id(self):
        return self._scroll_handler_id_value
    
    @_scroll_handler_id.setter
    def _scroll_handler_id(self, value):
        if self._scroll_handler_id_value is not None:
            self.disconnect(self._scroll_handler_id_value)

        self._scroll_handler_id_value = value
            
