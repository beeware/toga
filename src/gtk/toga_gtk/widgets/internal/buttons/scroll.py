from toga_gtk.libs import Gtk
from .base import ParentPosition

class ScrollButton(ParentPosition):
    def __init__(self, adj: Gtk.Adjustment, bottom_margin=12, right_margin=20, *args, **kwargs):
        super().__init__(adj, *args, **kwargs)
        self.bottom_margin = bottom_margin
        self.right_margin = right_margin

        self._parent = None
        self._do_scroll = None

        self._button = Gtk.Button.new_with_label("Bottom")
        self._button.set_valign(Gtk.Align.END)
        self._button.set_halign(Gtk.Align.END)
        self._button.set_margin_bottom(self.bottom_margin)
        self._button.set_margin_end(self.right_margin)

        self._button_handler = self._button.connect(
            "clicked",
            lambda w: self._on_clicked())

        self.adj_handler = self.adj.connect(
            "value-changed",
            lambda adj: self.list_changed())

    def overlay_over(self, parent):
        self._parent = parent
        parent.add_overlay(self._button)
        self.list_changed()

    def set_scroll(self, do_scroll: callable):
        self._do_scroll = do_scroll

    def list_changed(self):
        is_at_top = self._is_parent_at_top()
        is_at_bottom = self._is_parent_at_bottom()

        is_distant_from_top = self._is_parent_distant_from_top()
        is_distant_from_bottom = self._is_parent_distant_from_bottom()

        if not is_at_top and not is_at_bottom \
           and is_distant_from_top and is_distant_from_bottom:
            self._button.show()
        else:
            self._button.hide()

    def _on_clicked(self):
        if self._do_scroll is not None:
            self._do_scroll()
