from toga_gtk.libs import GLib, Gtk


class ScrollableRow(Gtk.ListBoxRow):
    """You can use and inherit from this class as if it were Gtk.ListBoxRow,
    nothing from the original implementation is changed.

    There are three new public methods: scroll_to_top(),
    scroll_to_center() and scroll_to_bottom(). 'top', 'center' and
    'bottom' are with respect to where in the visible region the row
    will move to.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We need to wait until this widget is allocated to scroll it in,
        # for that we use signals and callbacks. The handler_is of the
        # signal is used to disconnect, and we store it here.
        self._gtk_scroll_handler_id_value = None

        # The animation function will use this variable to control whether the animation is
        # progressing, whether the user manually scrolled the list during the animation and whether
        # the list size changed.
        # In any case the animation will be stopped.
        self._animation_control = None

    def scroll_to_top(self):
        self.scroll_to_position("TOP")

    def scroll_to_center(self):
        self.scroll_to_position("CENTER")

    def scroll_to_bottom(self):
        self.scroll_to_position("BOTTOM")

    def scroll_to_position(self, position):
        """Scrolls the parent Gtk.ListBox until child is in the center of the
        view.

        `position` is one of "TOP", "CENTER" or "BOTTOM"
        """
        if position not in ("TOP", "CENTER", "BOTTOM"):
            return False

        # Test whether the widget has already been allocated.
        list_box = self.get_parent()
        _, y = self.translate_coordinates(list_box, 0, 0)
        if y >= 0:
            self.gtk_do_scroll_to_position(position)
        else:
            # Wait for 'size-allocate' because we will need the
            # dimensions of the widget. At this point
            # widget.size_request is already available but that's
            # only the requested size, not the size it will get.
            self._scroll_handler_id = self.connect(
                "size-allocate",
                # We don't need `wdiget` and `gpointer` but we do need to capture `position`
                lambda widget, gpointer: self.gtk_do_scroll_to_position(position),
            )

        return True

    def gtk_do_scroll_to_position(self, position):
        # Disconnect from the signal that called us
        self._gtk_scroll_handler_id = None

        list_box = self.get_parent()
        adj = list_box.get_adjustment()

        page_size = adj.get_page_size()

        # `height` and `y` are always valid because we are
        # being called after `size-allocate`
        row_height = self.get_allocation().height
        # `y` is the position of the top of the row in the frame of
        # reference of the parent Gtk.ListBox
        _, y = self.translate_coordinates(list_box, 0, 0)

        # `offset` is the remaining space in the visible region
        offset = page_size - row_height

        value_at_top = y
        value_at_center = value_at_top - offset / 2
        value_at_bottom = value_at_top - offset

        # `value` is the position the parent Gtk.ListBox will put at the
        # top of the visible region.
        value = 0.0

        if position == "TOP":
            value = value_at_top

        if position == "CENTER":
            value = value_at_center

        if position == "BOTTOM":
            value = value_at_bottom

        if value > 0:
            # We need to capture `value`
            GLib.idle_add(lambda: self.gtk_animate_scroll_to_position(value))

    def gtk_animate_scroll_to_position(self, final):
        # If this function returns True it is executed again.
        # If this function returns False, it is not executed anymore.
        # Set self._animation_control to None after the animation is over.
        list_box = self.get_parent()
        adj = list_box.get_adjustment()

        list_height = self.get_allocation().height
        current = adj.get_value()
        step = 1
        tol = 1e-9

        if self._animation_control is not None:
            # Whether the animation is progressing as planned or the user scrolled the list.
            position_change = abs(current - self._animation_control["last_position"])
            # Whether the list size changed.
            size_change = list_height - self._animation_control["list_height"]

            if position_change == 0 or position_change > step + tol or size_change != 0:
                self._animation_control = None
                return False

        self._animation_control = {"last_position": current, "list_height": list_height}

        distance = final - current

        if abs(distance) < step:
            adj.set_value(final)
            self._animation_control = None
            return False

        if distance > step:
            adj.set_value(current + step)
            return True

        if distance < -step:
            adj.set_value(current - step)
            return True

    @property
    def _gtk_scroll_handler_id(self):
        return self._gtk_scroll_handler_id_value

    @_gtk_scroll_handler_id.setter
    def _gtk_scroll_handler_id(self, value):
        if self._gtk_scroll_handler_id_value is not None:
            self.disconnect(self._gtk_scroll_handler_id_value)

        self._gtk_scroll_handler_id_value = value
