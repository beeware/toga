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

        # This is the factory of the DetailedList implementation.
        self.factory = factory

        self._delete_button = None

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

        self._delete_button = Gtk.Button.new_from_icon_name("user-trash-symbolic", Gtk.IconSize.BUTTON)
        self._delete_button.connect("clicked", lambda w: self._on_delete())
        self.add_button(self._delete_button)

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
        handler = self._dl.on_delete
        if handler is not None:
            self.toggle_content()
