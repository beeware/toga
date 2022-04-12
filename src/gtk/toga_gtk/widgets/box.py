from ..libs import Gdk, Gtk
from .base import Widget


class TogaBox(Gtk.Fixed):
    def __init__(self, impl):
        super().__init__()
        self._impl = impl
        self.interface = self._impl.interface

    def do_get_preferred_width(self):
        # Calculate the minimum and natural width of the container.
        # print("GET PREFERRED WIDTH", self._impl.native)
        width = self._impl.interface.layout.width
        min_width = 0 if self._impl.min_width is None else self._impl.min_width
        for widget in self.get_children():
            if (
                min_width
                <= widget.interface.layout.absolute_content_right
                + widget.interface.style.padding_right
            ):
                min_width = (
                    widget.interface.layout.absolute_content_right
                    + widget.interface.style.padding_right
                )
        if min_width > width:
            width = min_width

        return min_width, width

    def do_get_preferred_height(self):
        # Calculate the minimum and natural height of the container.
        # print("GET PREFERRED HEIGHT", self._impl.native)
        height = self._impl.interface.layout.height
        min_height = 0 if self._impl.min_height is None else self._impl.min_height
        for widget in self.get_children():
            if (
                min_height
                <= widget.interface.layout.absolute_content_bottom
                + widget.interface.style.padding_bottom
            ):
                min_height = (
                    widget.interface.layout.absolute_content_bottom
                    + widget.interface.style.padding_bottom
                )
        if min_height > height:
            height = min_height

        return min_height, height

    def do_size_allocate(self, allocation):
        # print(self._impl, "Container layout",
        #     allocation.width, 'x', allocation.height,
        #     ' @ ', allocation.x, 'x', allocation.y
        # )
        if self._impl.viewport is not None:
            self.set_allocation(allocation)
            self.interface.refresh()

            # WARNING! This list of children is *not* the same
            # as the list provided by the interface!
            # For GTK's layout purposes, all widgets in the tree
            # are children of the *container* - that is, the impl
            # object of the root object in the tree of widgets.
            for widget in self.get_children():
                if not widget.get_visible():
                    # print("CHILD NOT VISIBLE", widget.interface)
                    pass
                else:
                    # print("update ", widget.interface, widget.interface.layout)
                    widget.interface._impl.rehint()
                    widget_allocation = Gdk.Rectangle()
                    widget_allocation.x = widget.interface.layout.absolute_content_left + allocation.x
                    widget_allocation.y = widget.interface.layout.absolute_content_top + allocation.y
                    widget_allocation.width = widget.interface.layout.content_width
                    widget_allocation.height = widget.interface.layout.content_height

                    widget.size_allocate(widget_allocation)


class Box(Widget):
    def create(self):
        self.min_width = None
        self.min_height = None
        self.native = TogaBox(self)
