from toga_gtk.libs import Gtk
from .base import ParentPosition

class ScrollButton(ParentPosition):
    def __init__(self, adj: Gtk.Adjustment, bottom_margin=12, right_margin=20, *args, **kwargs):
        super().__init__(adj, *args, **kwargs)
        self.bottom_margin = bottom_margin
        self.right_margin = right_margin

        self._parent = None
        self._is_attached_to_parent = False
        self._do_scroll = None

        self._button = Gtk.Button.new_from_icon_name(
            "go-bottom-symbolic", Gtk.IconSize.BUTTON)

        self._button.set_can_focus(False)

        button_context = self._button.get_style_context()
        button_context.add_class("osd")
        button_context.add_class("toga-detailed-list-floating-buttons")

        self._revealer = Gtk.Revealer()

        self._revealer.set_can_focus(False)

        self._revealer.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
        self._revealer.set_valign(Gtk.Align.END)
        self._revealer.set_halign(Gtk.Align.END)
        self._revealer.set_margin_bottom(self.bottom_margin)
        self._revealer.set_margin_end(self.right_margin)

        self._revealer.add(self._button)
        self._revealer.set_reveal_child(False)

        self._button_handler = self._button.connect(
            "clicked",
            lambda w: self._on_clicked())

        self.adj_handler = self.adj.connect(
            "value-changed",
            lambda adj: self.list_changed())

    def overlay_over(self, parent):
        self._parent = parent
        parent.add_overlay(self._revealer)
        self.list_changed()

    def set_scroll(self, do_scroll: callable):
        self._do_scroll = do_scroll

    def show(self):
        self._revealer.set_reveal_child(True)

    def hide(self):
        self._revealer.set_reveal_child(False)

    def list_changed(self):
        is_scrollable = self._is_parent_scrollable()
        is_at_top = self._is_parent_at_top()
        is_at_bottom = self._is_parent_at_bottom()

        is_distant_from_top = self._is_parent_distant_from_top()
        is_distant_from_bottom = self._is_parent_distant_from_bottom()

        if is_scrollable and \
           not is_at_top and not is_at_bottom \
           and is_distant_from_top and is_distant_from_bottom:
            self.show()
        else:
            self.hide()

    def _on_clicked(self):
        if self._do_scroll is not None:
            self._do_scroll()
