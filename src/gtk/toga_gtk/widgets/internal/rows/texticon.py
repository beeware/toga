import html

from toga_gtk.libs import Gtk, GLib
from toga_gtk.icons import Icon

from .base import HiddenButtonsRow


class TextIconRow(HiddenButtonsRow):
    """
    Create a TextIconRow from a toga.sources.Row.
    A reference to the original row is kept in self.toga_row, this is useful for comparisons.
    """
    def __init__(self, factory: callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_delete_handler = None

        # This is the factory of the DetailedList implementation.
        self.factory = factory

        icon = self.get_icon(self.interface, self.factory)

        text = Gtk.Label(xalign=0)
        text_markup = self.markup(self.interface)
        text.set_markup(text_markup)

        content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        vbox.pack_start(text, True, True, 0)
        
        if icon is not None:
            content.pack_start(icon, False, False, 6)

        content.pack_start(vbox, True, True, 5)

        self.add_content(content)

    def set_on_delete(self, on_delete: callable):
        self._on_delete_handler = on_delete

        if self._on_delete_handler is not None:
            delete_button = Gtk.Button.new_from_icon_name("user-trash-symbolic", Gtk.IconSize.BUTTON)
            delete_button.connect("clicked", lambda w: self._on_delete())
            self.add_button(delete_button)
        else:
            self.destroy_buttons()

    def _on_delete(self):
        self._on_delete_handler(self.interface)
        HiddenButtonsRow._hide_buttons_on_all = None

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

    def on_right_click(self, rect):
        self.toggle_content()
