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
        # The implementation of DetailedList needs to wait until
        # this widget is allocated to call "_do_scroll_to_row".
        # We keep the handler_id here for disconnecting later.
        self._scroll_handler_id = None

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

    @property
    def scroll_handler_id(self):
        return self._scroll_handler_id
    
    @scroll_handler_id.setter
    def scroll_handler_id(self, value):
        if self._scroll_handler_id is not None:
            self.disconnect(self._scroll_handler_id)

        self._scroll_handler_id = value
            
