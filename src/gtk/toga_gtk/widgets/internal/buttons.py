from toga_gtk.libs import Gtk


# RefreshButton explanation:

# If the user is at the top of the list, then they are probably interested in the content at
# the top and we put the button at the bottom.
# If the user is at the botom of the list, then they are probably interested in the content at
# the bottom and we put the button at the top.

# If the user is scrolling through the list then don't show the button at all.
# If there is not enough content to scroll, show the button at the bottom and have a side button to
# move it to the top. After moving the button to the top, show a button to move it to the bottom.

# Example:

#  -------------
# | Refresh | X |
#  -------------

# To get whether the list is scrollable use `adj.get_page_size() == 0`.
# To get notified when the list is scrolled use `adj.connect(value_changed)` and use 
# `adj.get_value() + adj.get_page_size() == adj.get_upper()` to know if it is at the bottom and
# `adj.get_value() == adj.get_lower()` to know if it is at the top. This might not work well 
# when there is a hovering button, it seems that then scrolling is not immediately performed 
# when the mouse wheel is turned.

class RefreshButton(Gtk.HBox):
    """
    Shows a refresh button at the top of a list when the user is at the bottom of the list.
    Shows a refresh button at the bottom of a list when the user is at the top of the list.
    When there is not enough content to scroll, show the button at the bottom and have a side button 
    to move it to the top. After moving the button to the top, show a button to move it to the bottom.

    Example:

     -------------
    | Refresh | X |
     -------------
    """
    def __init__(self, position: str, on_refresh=None, margin=12, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if position in ("TOP", None,):
            self.position = Gtk.Align.START

        if position is "BOTTOM":
            self.position = Gtk.Align.END

        self.on_refresh = on_refresh
        self.on_close = None

        self.set_valign(self.position)
        self.set_halign(Gtk.Align.CENTER)
        self.set_margin_top(margin)
        self.set_margin_bottom(margin)

        left_btn = Gtk.Button.new_with_label("Refresh")
        left_btn_context = left_btn.get_style_context()
        left_btn_context.add_class("toga-refresh-button")

        right_btn = Gtk.Button.new_with_label("Close")
        right_btn_context = right_btn.get_style_context()
        right_btn_context.add_class("toga-refresh-button")
        
        left_btn.connect("clicked",
                         self._on_refresh_clicked)
        
        right_btn.connect("clicked", 
                          self._on_close_clicked)
        
        self.add(left_btn)
        self.add(right_btn)

    def _on_refresh_clicked(self, widget):
        if self.on_refresh is not None:
            self.on_refresh()

    @classmethod
    def _on_close_clicked(cls, widget):
        current_position = widget.get_parent().get_valign()
        box = widget.get_parent()
        overlay = box.get_parent()

        if current_position == Gtk.Align.END:
            new_button = cls("TOP", box.on_refresh)
        
        if current_position == Gtk.Align.START:
            new_button = cls("BOTTOM", box.on_refresh)

        # Better make this function a class method since we are going to destroy the instance.
        box.destroy()
        overlay.add_overlay(new_button)
        overlay.show_all()


    def _on_parent_list_scrolled(self, adj):
        pass
