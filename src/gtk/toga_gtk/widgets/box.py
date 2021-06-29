from travertino.constants import COLUMN, ROW
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
        # print(self.interface, "HAS", self.interface.children)
        if self.interface.style.direction == ROW:
            if min_width == 0:
                for widget in self.interface.children:
                    if str(type(widget)) == "<class 'toga.widgets.box.Box'>":
                        # Use previously calculated min width from widget._impl.native.get_preferred_width()[0]
                        if widget.style.width:
                            min_width += (
                                widget.style.padding_right
                                + widget.layout.width
                                + widget.style.padding_left
                            )
                        else:
                            min_width += (
                                widget.style.padding_right
                                + widget._impl.native.get_preferred_width()[0]
                                + widget.style.padding_left
                            )
                        # print(".... BOX WIDGET WITH ROW DIRECTION", widget, widget.children, min_width)
                    else:
                        if widget.style.flex:
                            if widget.style.width:
                                # The widget is flex but it has width
                                min_width += (
                                    widget.style.padding_right
                                    + widget.layout.width
                                    + widget.style.padding_left
                                )
                                # print(".... NOT BOX WIDGET WITH ROW DIRECTION, FLEX AND HEIGHT", widget, widget.children, min_width)
                            else:
                                min_width += (
                                    widget.style.padding_right
                                    + widget.intrinsic.width.value
                                    if hasattr(widget.intrinsic.width, "value")
                                    else widget.intrinsic.width
                                    + widget.style.padding_left
                                )
                                # print(".... NOT BOX WIDGET WITH ROW DIRECTION, FLEX AND NO HEIGHT", widget, widget.children, min_width)
                        else:
                            if widget.style.width:
                                # The widget is flex but it has width
                                min_width += (
                                    widget.style.padding_right
                                    + widget.layout.width
                                    + widget.style.padding_left
                                )
                                # print(".... NOT BOX WIDGET WITH ROW DIRECTION, NOT FLEX AND HEIGHT", widget, widget.children, min_width)
                            else:
                                # The widget is flex and it has not width
                                min_width += (
                                    widget.style.padding_right
                                    + widget.intrinsic.width.value
                                    if hasattr(widget.intrinsic.width, "value")
                                    else widget.intrinsic.width
                                    + widget.style.padding_left
                                )
                                # print(".... NOT BOX WIDGET WITH ROW DIRECTION, NOT FLEX AND NO HEIGHT", widget, widget.children, min_width)
        elif self.interface.style.direction == COLUMN:
            for widget in self.interface.children:
                if str(type(widget)) == "<class 'toga.widgets.box.Box'>":
                    if (
                        min_width
                        <= widget.style.padding_right
                        + widget._impl.native.get_preferred_width()[0]
                        + widget.style.padding_left
                    ):
                        min_width = (
                            widget.style.padding_right
                            + widget._impl.native.get_preferred_width()[0]
                            + widget.style.padding_left
                        )
                    # print(".... BOX WIDGET WITH COLUMN DIRECTION", widget, widget.children, min_width)
                else:
                    if widget.style.flex:
                        if widget.style.width:
                            # The widget is flex but it has width
                            if (
                                min_width
                                <= widget.style.padding_right
                                + widget.layout.width
                                + widget.style.padding_left
                            ):
                                min_width = (
                                    widget.style.padding_right
                                    + widget.layout.width
                                    + widget.style.padding_left
                                )
                            # print(".... NOT BOX WIDGET WITH COLUMN DIRECTION, FLEX AND HEIGHT", widget, widget.children, min_width)
                        else:
                            # The widget is flex and it does not has width
                            if (
                                min_width
                                <= widget.style.padding_right
                                + widget.intrinsic.width.value
                                if hasattr(widget.intrinsic.width, "value")
                                else widget.intrinsic.width + widget.style.padding_left
                            ):
                                min_width = (
                                    widget.style.padding_right
                                    + widget.intrinsic.width.value
                                    if hasattr(widget.intrinsic.width, "value")
                                    else widget.intrinsic.width
                                    + widget.style.padding_left
                                )
                            # print(".... NOT BOX WIDGET WITH COLUMN DIRECTION, FLEX AND NO HEIGHT", widget, widget.children, min_width)
                    else:
                        # The widget is flex but it has width
                        if widget.style.width:
                            # The widget is flex but it has width
                            if (
                                min_width
                                <= widget.style.padding_right
                                + widget.layout.width
                                + widget.style.padding_left
                            ):
                                min_width = (
                                    widget.style.padding_right
                                    + widget.layout.width
                                    + widget.style.padding_left
                                )
                            # print(".... NOT BOX WIDGET WITH COLUMN DIRECTION, NOT FLEX AND HEIGHT", widget, widget.children, min_width)
                        else:
                            # The widget is flex and it has not width
                            if (
                                min_width
                                <= widget.style.padding_right
                                + widget.intrinsic.width.value
                                if hasattr(widget.intrinsic.width, "value")
                                else widget.intrinsic.width + widget.style.padding_left
                            ):
                                min_width = (
                                    widget.style.padding_right
                                    + widget.intrinsic.width.value
                                    if hasattr(widget.intrinsic.width, "value")
                                    else widget.intrinsic.width
                                    + widget.style.padding_left
                                )
                            # print(".... NOT BOX WIDGET WITH COLUMN DIRECTION, NOT FLEX AND NO HEIGHT", widget, widget.children, min_width)

        min_width += (
            self.interface.style.padding_right + self.interface.style.padding_left
        )
        if min_width > width:
            width = min_width

        # print(".... .... MIN WIDTH OF THE BOX", min_width)

        return min_width, width

    def do_get_preferred_height(self):
        # Calculate the minimum and natural height of the container.
        # print("GET PREFERRED HEIGHT", self._impl.native)
        height = self._impl.interface.layout.height
        min_height = 0 if self._impl.min_height is None else self._impl.min_height
        # print(self.interface, "HAS", self.interface.children)
        if self.interface.style.direction == COLUMN:
            if min_height == 0:
                for widget in self.interface.children:
                    if str(type(widget)) == "<class 'toga.widgets.box.Box'>":
                        # Use previously calculated min height from widget._impl.native.get_preferred_height()[0]
                        if widget.style.height:
                            min_height += (
                                widget.style.padding_top
                                + widget.layout.height
                                + widget.style.padding_bottom
                            )
                        else:
                            min_height += (
                                widget.style.padding_top
                                + widget._impl.native.get_preferred_height()[0]
                                + widget.style.padding_bottom
                            )
                        # print(".... BOX WIDGET WITH COLUMN DIRECTION", widget, widget.children, min_height)
                    else:
                        if widget.style.flex:
                            if widget.style.height:
                                # The widget is flex but it has height
                                min_height += (
                                    widget.style.padding_top
                                    + widget.layout.height
                                    + widget.style.padding_bottom
                                )
                                # print(".... NOT BOX WIDGET WITH COLUMN DIRECTION, FLEX AND HEIGHT", widget, widget.children, min_height)
                            else:
                                min_height += (
                                    widget.style.padding_top
                                    + widget.intrinsic.height.value
                                    if hasattr(widget.intrinsic.height, "value")
                                    else widget.intrinsic.height
                                    + widget.style.padding_bottom
                                )
                                # print(".... NOT BOX WIDGET WITH COLUMN DIRECTION, FLEX AND NO HEIGHT", widget, widget.children, min_height)
                        else:
                            if widget.style.height:
                                # The widget is flex but it has height
                                min_height += (
                                    widget.style.padding_top
                                    + widget.layout.height
                                    + widget.style.padding_bottom
                                )
                                # print(".... NOT BOX WIDGET WITH COLUMN DIRECTION, NOT FLEX AND HEIGHT", widget, widget.children, min_height)
                            else:
                                # The widget is flex and it has not height
                                min_height += (
                                    widget.style.padding_top
                                    + widget.intrinsic.height.value
                                    if hasattr(widget.intrinsic.height, "value")
                                    else widget.intrinsic.height
                                    + widget.style.padding_bottom
                                )
                                # print(".... NOT BOX WIDGET WITH COLUMN DIRECTION, NOT FLEX AND NO HEIGHT", widget, widget.children, min_height)
        elif self.interface.style.direction == ROW:
            for widget in self.interface.children:
                if str(type(widget)) == "<class 'toga.widgets.box.Box'>":
                    if (
                        min_height
                        <= widget.style.padding_top
                        + widget._impl.native.get_preferred_height()[0]
                        + widget.style.padding_bottom
                    ):
                        min_height = (
                            widget.style.padding_top
                            + widget._impl.native.get_preferred_height()[0]
                            + widget.style.padding_bottom
                        )
                    # print(".... BOX WIDGET WITH ROW DIRECTION", widget, widget.children, min_height)
                else:
                    if widget.style.flex:
                        if widget.style.height:
                            # The widget is flex but it has height
                            if (
                                min_height
                                <= widget.style.padding_top
                                + widget.layout.height
                                + widget.style.padding_bottom
                            ):
                                min_height = (
                                    widget.style.padding_top
                                    + widget.layout.height
                                    + widget.style.padding_bottom
                                )
                            # print(".... NOT BOX WIDGET WITH ROW DIRECTION, FLEX AND HEIGHT", widget, widget.children, min_height)
                        else:
                            # The widget is flex and it does not has height
                            if (
                                min_height
                                <= widget.style.padding_top
                                + widget.intrinsic.height.value
                                if hasattr(widget.intrinsic.height, "value")
                                else widget.intrinsic.height
                                + widget.style.padding_bottom
                            ):
                                min_height = (
                                    widget.style.padding_top
                                    + widget.intrinsic.height.value
                                    if hasattr(widget.intrinsic.height, "value")
                                    else widget.intrinsic.height
                                    + widget.style.padding_bottom
                                )
                            # print(".... NOT BOX WIDGET WITH ROW DIRECTION, FLEX AND NO HEIGHT", widget, widget.children, min_height)
                    else:
                        # The widget is flex but it has height
                        if widget.style.height:
                            # The widget is flex but it has height
                            if (
                                min_height
                                <= widget.style.padding_top
                                + widget.layout.height
                                + widget.style.padding_bottom
                            ):
                                min_height = (
                                    widget.style.padding_top
                                    + widget.layout.height
                                    + widget.style.padding_bottom
                                )
                            # print(".... NOT BOX WIDGET WITH ROW DIRECTION, NOT FLEX AND HEIGHT", widget, widget.children, min_height)
                        else:
                            # The widget is flex and it has not height
                            if (
                                min_height
                                <= widget.style.padding_top
                                + widget.intrinsic.height.value
                                if hasattr(widget.intrinsic.height, "value")
                                else widget.intrinsic.height
                                + widget.style.padding_bottom
                            ):
                                min_height = (
                                    widget.style.padding_top
                                    + widget.intrinsic.height.value
                                    if hasattr(widget.intrinsic.height, "value")
                                    else widget.intrinsic.height
                                    + widget.style.padding_bottom
                                )
                            # print(".... NOT BOX WIDGET WITH ROW DIRECTION, NOT FLEX AND NO HEIGHT", widget, widget.children, min_height)

        min_height += (
            self.interface.style.padding_bottom + self.interface.style.padding_top
        )
        if min_height > height:
            height = min_height

        # print(".... .... MIN HEIGHT OF THE BOX", min_height)

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
                    widget_allocation.x = (
                        widget.interface.layout.absolute_content_left + allocation.x
                    )
                    widget_allocation.y = (
                        widget.interface.layout.absolute_content_top + allocation.y
                    )
                    widget_allocation.width = widget.interface.layout.content_width
                    widget_allocation.height = widget.interface.layout.content_height

                    widget.size_allocate(widget_allocation)


class Box(Widget):
    def create(self):
        self.min_width = None
        self.min_height = None
        self.native = TogaBox(self)
