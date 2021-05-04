import html

from toga_gtk.libs import Gtk
from toga_gtk.icons import Icon


class ScrollableRow(Gtk.ListBoxRow):
    """
    You can use and inherit from this class as if it were Gtk.ListBoxRow, nothing 
    from the original implementation is changed.
    There are three new public methods: scroll_to_top(), scroll_to_center() and 
    scroll_to_bottom(). 'top', 'center' and 'bottom' are with respect to where in the
    visible region the row will move to.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We need to wait until this widget is allocated to scroll it in,
        # for that we use signals and callbacks. The handler_is of the
        # signal is used to disconnect and we store it here.
        self._scroll_handler_id_value = None

    def scroll_to_top(self):
        self.scroll_to_position("TOP")

    def scroll_to_center(self):
        self.scroll_to_position("CENTER")

    def scroll_to_bottom(self):
        self.scroll_to_position("BOTTOM")

    def scroll_to_position(self, position):
        """
        Scrolls the parent Gtk.ListBox until child is in the center of the
        view.
        `position` is one of "TOP", "CENTER" or "BOTTOM"
        """
        if position not in ("TOP", "CENTER", "BOTTOM"):
            return False

        # Test whether the widget has already been allocated.
        list_box = self.get_parent()
        _, y = self.translate_coordinates(list_box, 0, 0)
        if y >= 0:
            self._do_scroll_to_position(position)
        else:
            # Wait for 'size-allocate' because we will need the
            # dimensions of the widget. At this point 
            # widget.size_request is already available but that's
            # only the requested size, not the size it will get.
            self._scroll_handler_id = self.connect(
                'size-allocate',
                # We don't need 'wdiget' and 'gpointer'
                lambda widget, gpointer: self._do_scroll_to_position(position)
            )

        return True

    def _do_scroll_to_position(self, position):
        # Disconnect the from the signal that called us
        self._scroll_handler_id = None

        list_box = self.get_parent()

        adj = list_box.get_adjustment()
        page_size = adj.get_page_size()

        # 'height' and 'y' are always valid because we are
        # being called after 'size-allocate'
        height = self.get_allocation().height
        # `y` is the position of the top of the row in the frame of
        # reference of the parent Gtk.ListBox
        _, y = self.translate_coordinates(list_box, 0, 0)

        # `offset` is the remaining space in the visible region
        offset = page_size - height

        top = y
        center = top - offset/2
        bottom = top - offset

        # `value` is the position the parent Gtk.ListBox will put at the
        # top of the visible region.
        value = 0.0
        if position == "TOP":
            value = top

        if position == "CENTER":
            value = center

        if position == "BOTTOM":
            value = bottom
            
        if value > 0:
            adj.set_value(value)


    @property
    def _scroll_handler_id(self):
        return self._scroll_handler_id_value
    
    @_scroll_handler_id.setter
    def _scroll_handler_id(self, value):
        if self._scroll_handler_id_value is not None:
            self.disconnect(self._scroll_handler_id_value)

        self._scroll_handler_id_value = value
            

class TextIconRow(ScrollableRow):
    """
    Create a TextIconRow from a toga.sources.Row.
    A reference to the original row is kept in self.toga_row, this is useful for comparisons.
    """
    def __init__(self, interface: 'Row', parent_impl: 'DetailedList', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent_impl = parent_impl
        # Keep a reference to the original core.toga.sources.list_source.Row
        self.interface = interface
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
      
        self.text = Gtk.Label(xalign=0)
        text_markup = self.markup(self.interface)
        self.text.set_markup(text_markup)

        self.icon = self.get_icon(self.interface, self.parent_impl.interface.factory)

        self.vbox.pack_start(self.text, True, True, 0)
        
        if self.icon is not None:
            self.hbox.pack_start(self.icon, False, False, 6)

        self.hbox.pack_start(self.vbox, True, True, 0)

        self.add(self.hbox)

    def get_icon(self, row, factory):
        if getattr(row, "icon") is None:
            return None
        else:
            row.icon.bind(factory)
            # TODO: see get_scale_factor() to choose 72 px on hidpi
            return getattr(row.icon._impl, "native_" + str(32))

    @staticmethod
    def markup(row):
        markup = [
            html.escape(row.title or ''),
            '\n',
            '<small>', html.escape(row.subtitle or ''), '</small>',
        ]
        return ''.join(markup)
