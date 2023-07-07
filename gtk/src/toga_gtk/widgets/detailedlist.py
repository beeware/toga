import html

from travertino.size import at_least

from toga_gtk.libs import Gdk, Gio, Gtk, Pango

from .base import Widget


class DetailedListRow(Gtk.ListBoxRow):
    """A row in a DetailedList."""

    def __init__(self, dl, row):
        super().__init__()
        self.row = row
        self.row._impl = self

        # The row is a built as a stack, so that the action buttons can be pushed onto
        # the stack as required.
        self.stack = Gtk.Stack()
        self.stack.set_homogeneous(True)
        self.add(self.stack)

        self.content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        # Initial Icon is empty; it will be populated on the initial update
        self.icon = None

        self.text = Gtk.Label(xalign=0)

        # The three line below are necessary for right to left text.
        self.text.set_hexpand(True)
        self.text.set_ellipsize(Pango.EllipsizeMode.END)
        self.text.set_margin_end(12)

        self.content.pack_end(self.text, True, True, 5)

        # Update the content for the row.
        self.update(dl, row)

        self.stack.add_named(self.content, "content")

    def update(self, dl, row):
        """Update the contents of the rendered row, using data from `row`, and accessors from the detailedList"""

        # Set the title and subtitle as a block of HTML text.
        try:
            title = getattr(self.row, dl.accessors[0])
            if title is not None:
                title = str(title)
            else:
                title = dl.missing_value
        except AttributeError:
            title = dl.missing_value

        try:
            subtitle = getattr(self.row, dl.accessors[1])
            if subtitle is not None:
                subtitle = str(subtitle)
            else:
                subtitle = dl.missing_value
        except AttributeError:
            subtitle = dl.missing_value

        markup = "".join(
            [
                html.escape(title),
                "\n",
                "<small>",
                html.escape(subtitle),
                "</small>",
            ]
        )
        self.text.set_markup(markup)

        # Update the icon
        if self.icon:
            self.content.remove(self.icon)

        try:
            pixbuf = getattr(self.row, dl.accessors[2])._impl.native_32
        except AttributeError:
            pixbuf = None

        if pixbuf is not None:
            self.icon = Gtk.Image.new_from_pixbuf(pixbuf)
            self.content.pack_start(self.icon, False, False, 6)
        else:
            self.icon = None

    def show_actions(self, action_buttons):
        self.stack.add_named(action_buttons, "actions")
        self.stack.set_visible_child_name("actions")

    def hide_actions(self):
        self.stack.set_visible_child_name("content")
        self.stack.remove(self.stack.get_child_by_name("actions"))


class DetailedList(Widget):
    def create(self):
        # Not the same as selected row. _active_row is the one with its buttons exposed.
        self._active_row = None

        # Main functional widget is a ListBox.
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.list_box.connect("row-selected", self.gtk_on_row_selected)

        self.store = Gio.ListStore()
        # We need to provide a function that transforms whatever is in the store into a
        # `Gtk.ListBoxRow`, but the items in the store already are `Gtk.ListBoxRow`, so
        # this is the identity function.
        self.list_box.bind_model(self.store, lambda a: a)

        # Put the ListBox into a vertically scrolling window.
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.set_min_content_width(self.interface._MIN_WIDTH)
        self.scrolled_window.set_min_content_height(self.interface._MIN_HEIGHT)
        self.scrolled_window.add(self.list_box)

        self.native_vadj = self.scrolled_window.get_vadjustment()
        self.native_vadj.connect("value-changed", self.gtk_on_value_changed)

        # Define a revealer widget that can be used to show/hide with a crossfade.
        self.revealer = Gtk.Revealer()
        self.revealer.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
        self.revealer.set_valign(Gtk.Align.END)
        self.revealer.set_halign(Gtk.Align.CENTER)
        self.revealer.set_margin_bottom(12)
        self.revealer.set_reveal_child(False)

        # Define a refresh button.
        self.refresh_button = Gtk.Button.new_from_icon_name(
            "view-refresh-symbolic", Gtk.IconSize.BUTTON
        )
        self.refresh_button.set_can_focus(False)
        self.refresh_button.connect("clicked", self.gtk_on_refresh_clicked)

        style_context = self.refresh_button.get_style_context()
        style_context.add_class("osd")
        style_context.add_class("toga-detailed-list-floating-buttons")
        style_context.remove_class("button")

        # Add the refresh button to the revealer
        self.revealer.add(self.refresh_button)

        # The actual native widget is an overlay, made up of the scrolled window, with
        # the revealer over the top.
        self.native = Gtk.Overlay()
        self.native.add_overlay(self.scrolled_window)
        self.native.add_overlay(self.revealer)

        # Set up a gesture to capture right clicks;
        # don't connect the signal handler until an actions is enabled.
        self.right_click_gesture = Gtk.GestureMultiPress.new(self.list_box)
        self.right_click_gesture.set_button(3)
        self.right_click_gesture.set_propagation_phase(Gtk.PropagationPhase.BUBBLE)
        self.right_click_gesture.connect("pressed", self.gtk_on_right_click)

        # Set up a box that contains action buttons. This widget can be can be re-used
        # for any row when it is activated.
        self.action_buttons = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.action_buttons_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        # self.primary_action_button = Gtk.Button.new_from_icon_name(
        #     "user-trash-symbolic", Gtk.IconSize.BUTTON
        # )
        self.action_buttons_hbox.pack_start(Gtk.Box(), True, True, 0)

        self.primary_action_button = Gtk.Button.new_with_label(
            self.interface._primary_action
        )
        self.primary_action_button.connect("clicked", self.gtk_on_primary_clicked)
        self.action_buttons_hbox.pack_start(
            self.primary_action_button, False, False, 10
        )

        # self.secondary_action_button = Gtk.Button.new_from_icon_name(
        #     "user-trash-symbolic", Gtk.IconSize.BUTTON
        # )
        self.secondary_action_button = Gtk.Button.new_with_label(
            self.interface._secondary_action
        )
        self.secondary_action_button.connect("clicked", self.gtk_on_secondary_clicked)
        self.action_buttons_hbox.pack_start(
            self.secondary_action_button, False, False, 10
        )

        self.action_buttons_hbox.pack_start(Gtk.Box(), True, True, 0)

        self.action_buttons.pack_start(self.action_buttons_hbox, True, False, 0)
        self.action_buttons.show_all()

    def row_factory(self, item):
        return DetailedListRow(self.interface, item)

    def change_source(self, source):
        self.store.remove_all()
        for item in source:
            self.store.append(self.row_factory(item))

    def insert(self, index, item):
        self.hide_actions()
        item_impl = self.row_factory(item)
        self.store.insert(index, item_impl)
        self.list_box.show_all()
        self.update_refresh_button()

    def change(self, item):
        item._impl.update(self.interface, item)

    def remove(self, item, index):
        self.hide_actions()
        self.store.remove(index)
        self.update_refresh_button()

    def clear(self):
        self.hide_actions()
        self.store.remove_all()
        self.update_refresh_button()

    def get_selection(self):
        item_impl = self.list_box.get_selected_row()
        if item_impl is None:
            return None
        else:
            return item_impl.get_index()

    def scroll_to_row(self, row: int):
        upper = self.native_vadj.get_upper()
        self.native_vadj.set_value(
            min(
                row / len(self.store) * upper + self.native.get_allocation().height,
                upper,
            )
        )

    def set_refresh_enabled(self, enabled):
        self.update_refresh_button()

    @property
    def refresh_enabled(self):
        return self.interface.on_refresh._raw is not None

    def set_primary_action_enabled(self, enabled):
        self.primary_action_button.set_visible(enabled)

    def set_secondary_action_enabled(self, enabled):
        self.secondary_action_button.set_visible(enabled)

    @property
    def primary_action_enabled(self):
        return self.interface.on_primary_action._raw is not None

    @property
    def secondary_action_enabled(self):
        return self.interface.on_secondary_action._raw is not None

    @property
    def actions_enabled(self):
        return self.primary_action_enabled or self.secondary_action_enabled

    def after_on_refresh(self, widget, result):
        pass

    def gtk_on_value_changed(self, adj):
        # The vertical scroll value has changed.
        # Update the refresh button; hide the buttons on the active row (if they're active)
        self.update_refresh_button()
        self.hide_actions()

    def gtk_on_refresh_clicked(self, widget):
        self.interface.on_refresh(self.interface)

    def gtk_on_row_selected(self, w: Gtk.ListBox, item_impl: Gtk.ListBoxRow):
        self.hide_actions()
        self.interface.on_select(self.interface)

    def gtk_on_right_click(self, gesture, n_press, x, y):
        item_impl = self.list_box.get_row_at_y(y)
        if item_impl is None or self._active_row == item_impl:
            return

        rect = Gdk.Rectangle()
        rect.x, rect.y = item_impl.translate_coordinates(self.list_box, x, y)

        self.hide_actions()

        if self.actions_enabled:
            self.list_box.select_row(item_impl)
            self._active_row = item_impl
            self._active_row.show_actions(self.action_buttons)

    def hide_actions(self):
        if self._active_row is not None:
            self._active_row.hide_actions()
            self._active_row = None

    def gtk_on_primary_clicked(self, widget):
        self.interface.on_primary_action(None, row=self._active_row.row)

    def gtk_on_secondary_clicked(self, widget):
        self.interface.on_secondary_action(None, row=self._active_row.row)

    def update_refresh_button(self):
        # If the scroll is currently at the top, and refresh is currently enabled,
        # reveal the refresh widget.
        show_refresh = self.refresh_enabled and (
            self.native_vadj.get_value() == self.native_vadj.get_lower()
        )
        self.revealer.set_reveal_child(show_refresh)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
