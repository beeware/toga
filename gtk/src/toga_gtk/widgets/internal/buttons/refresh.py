from toga_gtk.libs import Gtk

from .base import ParentPosition


class RefreshButtonWidget(Gtk.Revealer):
    def __init__(self, position: Gtk.Align, margin: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = None

        self.refresh_btn = Gtk.Button.new_from_icon_name(
            "view-refresh-symbolic", Gtk.IconSize.BUTTON
        )
        self.refresh_btn.set_can_focus(False)
        refresh_btn_context = self.refresh_btn.get_style_context()
        refresh_btn_context.add_class("osd")
        refresh_btn_context.add_class("toga-detailed-list-floating-buttons")
        refresh_btn_context.remove_class("button")

        self.close_btn = Gtk.Button.new_from_icon_name(
            "close-symbolic", Gtk.IconSize.BUTTON
        )
        self.close_btn.set_can_focus(False)
        close_btn_context = self.close_btn.get_style_context()
        close_btn_context.add_class("osd")
        close_btn_context.add_class("toga-detailed-list-floating-buttons")

        self.hbox = Gtk.HBox()
        self.hbox.add(self.refresh_btn)
        self.hbox.add(self.close_btn)

        self.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
        self.set_valign(position)
        self.set_halign(Gtk.Align.CENTER)
        self.set_margin_top(margin)
        self.set_margin_bottom(margin)

        self.set_reveal_child(False)
        self.add(self.hbox)

    def set_on_refresh(self, gtk_on_refresh: callable):
        self.refresh_btn.connect("clicked", gtk_on_refresh)

    def set_on_close(self, gtk_on_close: callable):
        self.close_btn.connect("clicked", gtk_on_close)

    def show(self):
        self.set_reveal_child(True)

    def hide(self):
        self.refresh_btn.hide()
        self.close_btn.hide()
        self.set_reveal_child(False)

    def show_close(self):
        return self.close_btn.show_now()

    def hide_close(self):
        return self.close_btn.hide()

    def show_refresh(self):
        return self.refresh_btn.show_now()

    def is_visible(self):
        return self.get_reveal_child()


class RefreshButton(ParentPosition):
    """Shows a refresh button at the top of a list when the user is at the
    bottom of the list. Shows a refresh button at the bottom of a list when the
    user is at the top of the list. When there is not enough content to scroll,
    show the button at the bottom and have a side button to move it to the top.
    After moving the button to the top, show a button to move it to the bottom.

    Example:
     -------------
    | Refresh | X |
     -------------
    """

    def __init__(self, adj: Gtk.Adjustment, margin=12, *args, **kwargs):
        super().__init__(adj, *args, **kwargs)
        self.margin = margin
        self._parent = None
        self.on_refresh = None

        self.button_top = RefreshButtonWidget(Gtk.Align.START, self.margin)
        self.button_top.set_on_refresh(self.gtk_on_refresh_clicked)
        self.button_top.set_on_close(self.gtk_on_close_clicked)

        self.button_bottom = RefreshButtonWidget(Gtk.Align.END, self.margin)
        self.button_bottom.set_on_refresh(self.gtk_on_refresh_clicked)
        self.button_bottom.set_on_close(self.gtk_on_close_clicked)

        self.gtk_adj_handler = self.adj.connect(
            "value-changed", self.gtk_on_value_changed
        )

    def overlay_over(self, parent):
        self._parent = parent
        self.list_changed()
        parent.add_overlay(self.button_top)
        parent.add_overlay(self.button_bottom)

    def destroy(self, *args, **kwargs):
        self.adj.disconnect(self.gtk_adj_handler)
        self.button_top.destroy()
        self.button_bottom.destroy()
        return super().destroy(*args, **kwargs)

    def set_on_refresh(self, on_refresh: callable):
        self.on_refresh = on_refresh

    def gtk_on_value_changed(self, adj: Gtk.Adjustment):
        self.list_changed()

    def gtk_on_refresh_clicked(self, w: Gtk.Button):
        if self.on_refresh is not None:
            self.on_refresh()

    def gtk_on_close_clicked(self, w: Gtk.Button):
        is_top_visible = self.button_top.is_visible()
        is_bottom_visible = self.button_bottom.is_visible()

        if not is_top_visible:
            self._show_top_full()

        if not is_bottom_visible:
            self._show_bottom_full()

    def _hide_all(self):
        self.button_top.hide()
        self.button_bottom.hide()

    def _show_top_full(self):
        self._hide_all()

        self.button_top.show()
        self.button_top.show_close()
        self.button_top.show_refresh()

    def _show_top_refresh(self):
        self._hide_all()

        self.button_top.show()
        self.button_top.hide_close()
        self.button_top.show_refresh()

    def _show_bottom_full(self):
        self._hide_all()

        self.button_bottom.show()
        self.button_bottom.show_close()
        self.button_bottom.show_refresh()

    def _show_bottom_refresh(self):
        self._hide_all()

        self.button_bottom.show()
        self.button_bottom.show_refresh()
        self.button_bottom.hide_close()

    def _show_both_full(self):
        self._hide_all()
        self._show_bottom_full()

    def list_changed(self):
        if self.on_refresh is None:
            self._hide_all()
            return

        is_scrollable = self.is_parent_scrollable()
        is_at_top = self.is_parent_at_top()
        is_at_bottom = self.is_parent_at_bottom()

        if not is_scrollable:
            self._show_both_full()
            return

        if is_at_top:
            self._show_bottom_refresh()
            return

        if is_at_bottom:
            self._show_top_refresh()
            return

        if not is_at_top and not is_at_bottom:
            self._hide_all()
            return
