from toga_gtk.libs import Gtk, GLib
from .scrollable import ScrollableRow


class BaseRow(ScrollableRow):
    def __init__(self, interface: 'Row', *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep a reference to the original core.toga.sources.list_source.Row
        self.interface = interface


class HiddenButtonsRow(BaseRow):
    """
    You can add a content box and a set of buttons to this row. You can toggle the content with
    `toggle_content()`.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Replace class method with signal.
        # This will be used to hide buttons on any other row.
        HiddenButtonsRow._hide_buttons_on_all = None

        self._content_name = "content"
        self._buttons_name = "buttons"
        self._has_buttons = False

        self.content = None
        self.buttons = None

        self.stack = Gtk.Stack()

        self.add(self.stack)

    def create_buttons(self):
        self.buttons = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.buttons_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
        self.buttons.pack_start(self.buttons_hbox, True, False, 0)

    def destroy_buttons(self):
        self.buttons.destroy()
        self.create_buttons()

    def destroy_button(self, button: Gtk.Widget):
        pass

    def destroy(self, *args, **kwargs):
        self.buttons.destroy()
        self.content.destroy()
        HiddenButtonsRow._hide_buttons_on_all = None
        super().destroy(*args, **kwargs)

    def show_buttons(self):
        # When we show the buttons no other row is showing it too.
        if HiddenButtonsRow._hide_buttons_on_all is not None:
            HiddenButtonsRow._hide_buttons_on_all()
        
        self.stack.set_visible_child_name(self._buttons_name)
        HiddenButtonsRow._hide_buttons_on_all = self.hide_buttons

    def hide_buttons(self):
        self.stack.set_visible_child_name(self._content_name)
        HiddenButtonsRow._hide_buttons_on_all = None

    def toggle_content(self):
        visible_child = self.stack.get_visible_child_name()

        if visible_child == self._content_name and self.buttons is not None:
            self.show_buttons()

        if visible_child == self._buttons_name:
            self.hide_buttons()

    def add_content(self, content: Gtk.Widget):
        self.content = content
        self.stack.add_named(content, self._content_name)

    def add_button(self, button: Gtk.Button):
        if self.buttons is None:
            self.create_buttons()
            self.stack.add_named(self.buttons, self._buttons_name)

        self.buttons_hbox.pack_start(button, True, False, 10)
