import html
import warnings

from toga_gtk.libs import Gtk, Pango

from .base import HiddenButtonsRow


class TextIconRow(HiddenButtonsRow):
    """Create a TextIconRow from a toga.sources.Row.

    A reference to the original row is kept in self.toga_row, this is
    useful for comparisons.
    """

    def __init__(self, factory: callable, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # This is the factory of the DetailedList implementation.
        self.factory = factory

        self.icon = self.get_icon(self.interface, self.factory)

        text = Gtk.Label(xalign=0)

        # The three line below are necessary for right to left text.
        text.set_hexpand(True)
        text.set_ellipsize(Pango.EllipsizeMode.END)
        text.set_margin_end(12)

        text_markup = self.markup(self.interface)
        text.set_markup(text_markup)

        content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        vbox.pack_start(text, True, True, 0)

        if self.icon is not None:
            content.pack_start(self.icon, False, False, 6)

        content.pack_start(vbox, True, True, 5)

        self.add_content(content)

        self._delete_button = Gtk.Button.new_from_icon_name(
            "user-trash-symbolic", Gtk.IconSize.BUTTON
        )
        self._delete_button.connect("clicked", self.gtk_on_delete_clicked)
        self.add_button(self._delete_button)

    @property
    def title(self):
        return self.interface.title

    @property
    def subtitle(self):
        return self.interface.subtitle

    def get_icon(
        self,
        row,
        factory=None,  # DEPRECATED!
    ):
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        if getattr(row, "icon") is None:
            return None
        else:
            dpr = self.get_scale_factor()
            return getattr(row.icon._impl, "native_" + str(32 * dpr))

    @staticmethod
    def markup(row):
        markup = [
            html.escape(row.title or ""),
            "\n",
            "<small>",
            html.escape(row.subtitle or ""),
            "</small>",
        ]
        return "".join(markup)

    def on_right_click(self, rect):
        handler = self._dl.interface.on_delete
        if handler is not None:
            self.toggle_content()

    def gtk_on_delete_clicked(self, w: Gtk.ListBoxRow):
        self._dl.interface.data.remove(self.interface)
