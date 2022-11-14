from toga_gtk.libs import Gtk

from .scrollable import ScrollableRow


class BaseRow(ScrollableRow):
    def __init__(self, interface, *args, **kwargs):
        """
        Args:
            interface (:obj:`Row`)
        """
        super().__init__(*args, **kwargs)
        # Keep a reference to the original core.toga.sources.list_source.Row
        self.interface = interface
        interface._impl = self


class HiddenButtonsRow(BaseRow):
    """You can add a content box and a set of buttons to this row.

    You can toggle the content with `toggle_content()`.
    """

    def __init__(self, dl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dl = dl

        self._content_name = "content"
        self._buttons_name = "buttons"

        self.stack = Gtk.Stack()

        self.content = Gtk.Box()

        self.buttons = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.buttons_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.buttons.pack_start(self.buttons_hbox, True, False, 0)

        self.stack.add_named(self.content, self._content_name)
        self.stack.add_named(self.buttons, self._buttons_name)

        self.add(self.stack)

    def add_content(self, content: Gtk.Widget):
        self.content.add(content)

    def add_button(self, button: Gtk.Button):
        self.buttons_hbox.pack_start(button, True, False, 10)

    def show_buttons(self):
        self.stack.set_visible_child_name(self._buttons_name)

    def hide_buttons(self):
        self.stack.set_visible_child_name(self._content_name)

    def toggle_content(self):
        visible_child = self.stack.get_visible_child_name()

        if visible_child == self._content_name:
            self.show_buttons()

        if visible_child == self._buttons_name:
            self.hide_buttons()
