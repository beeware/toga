from toga_gtk.libs import Gtk

from .base import ParentPosition


class ScrollButton(ParentPosition):
    def __init__(
        self, adj: Gtk.Adjustment, bottom_margin=12, right_margin=20, *args, **kwargs
    ):
        super().__init__(adj, *args, **kwargs)
        self.bottom_margin = bottom_margin
        self.right_margin = right_margin

        self._parent = None
        self._is_attached_to_parent = False
        self._do_scroll = None

        self.button = Gtk.Button.new_from_icon_name(
            "go-bottom-symbolic", Gtk.IconSize.BUTTON
        )

        self.button.set_can_focus(False)

        button_context = self.button.get_style_context()
        button_context.add_class("osd")
        button_context.add_class("toga-detailed-list-floating-buttons")

        self.revealer = Gtk.Revealer()

        self.revealer.set_can_focus(False)
        self.revealer.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
        self.revealer.set_valign(Gtk.Align.END)
        self.revealer.set_halign(Gtk.Align.END)
        self.revealer.set_margin_bottom(self.bottom_margin)
        self.revealer.set_margin_end(self.right_margin)

        self.revealer.add(self.button)
        self.revealer.set_reveal_child(False)

        self.button.connect("clicked", self.gtk_on_clicked)

        self.adj.connect("value-changed", self.gtk_on_value_changed)

    def overlay_over(self, parent):
        self._parent = parent
        parent.add_overlay(self.revealer)
        self.list_changed()

    def set_scroll(self, do_scroll: callable):
        self._do_scroll = do_scroll

    def show(self):
        self.revealer.set_reveal_child(True)

    def hide(self):
        self.revealer.set_reveal_child(False)

    def gtk_on_clicked(self, w: Gtk.Button):
        if self._do_scroll is not None:
            self._do_scroll()

    def gtk_on_value_changed(self, adj: Gtk.Alignment):
        self.list_changed()

    def list_changed(self):
        is_scrollable = self.is_parent_scrollable()
        is_at_top = self.is_parent_at_top()
        is_at_bottom = self.is_parent_at_bottom()

        is_distant_from_top = self.is_parent_distant_from_top()
        is_distant_from_bottom = self.is_parent_distant_from_bottom()

        if (
            is_scrollable
            and not is_at_top
            and not is_at_bottom
            and is_distant_from_top
            and is_distant_from_bottom
        ):
            self.show()
        else:
            self.hide()
