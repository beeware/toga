from .libs import Gdk, Gtk


class TogaContainer(Gtk.Fixed):
    """A GTK container widget implementing Toga's layout.

    This is a GTK widget, with no Toga interface manifestation.
    """

    def __init__(self):
        super().__init__()
        self._content = None
        self.min_width = 100
        self.min_height = 100

        # GDK/GTK always renders at 96dpi. When HiDPI mode is enabled, it is
        # managed at the compositor level. See
        # https://wiki.archlinux.org/index.php/HiDPI#GDK_3_(GTK_3) for details
        self.dpi = 96
        self.baseline_dpi = self.dpi

        self.dirty = set()

    @property
    def width(self):
        # Treat `native=None` as a 0x0 viewport.
        if self._content is None:
            return 0
        return self.get_allocated_width()

    @property
    def height(self):
        # Treat `native=None` as a 0x0 viewport.
        if self._content is None:
            return 0
        return self.get_allocated_height()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        if self._content:
            self._content.container = None

        self._content = widget
        if widget:
            widget.container = self

    def recompute(self):
        if self._content and self.dirty:
            # If any of the widgets have been marked as dirty,
            # recompute their bounds, and re-evaluate the minimum
            # allowed size fo the layout.
            while self.dirty:
                widget = self.dirty.pop()
                widget.gtk_rehint()

            # Compute the layout using a 0-size container
            self._content.interface.style.layout(
                self._content.interface, TogaContainer()
            )

            # print(" computed min layout", self._content.interface.layout)
            self.min_width = self._content.interface.layout.width
            self.min_height = self._content.interface.layout.height

    def do_get_preferred_width(self):
        # Calculate the minimum and natural width of the container.
        # print("GET PREFERRED WIDTH", self._content)
        if self._content is None:
            return 0, 0

        # Ensure we have an accurate min layout size
        self.recompute()

        # The container will conform to the size of the allocation it is given,
        # so the min and preferred size are the same.
        return self.min_width, self.min_width

    def do_get_preferred_height(self):
        # Calculate the minimum and natural height of the container.
        # print("GET PREFERRED HEIGHT", self._content)
        if self._content is None:
            return 0, 0

        # Ensure we have an accurate min layout size
        self.recompute()

        # The container will conform to the size of the allocation it is given,
        # so the min and preferred size are the same.
        return self.min_height, self.min_height

    def do_size_allocate(self, allocation):
        # print(self._content, f"Container layout {allocation.width}x{allocation.height} @ {allocation.x}x{allocation.y}")

        # The container will occupy the full space it has been allocated.
        self.set_allocation(allocation)

        if self._content:
            # Re-evaluate the layout using the allocation size as the basis for geometry
            # print("REFRESH LAYOUT", allocation.width, allocation.height)
            self._content.interface.refresh()

            # WARNING! This is the list of children of the *container*, not
            # the Toga widget. Toga maintains a tree of children; all nodes
            # in that tree are direct children of the container.
            for widget in self.get_children():
                if not widget.get_visible():
                    # print("  not visible {widget.interface}")
                    pass
                else:
                    # Set the size of the child widget to the computed layout size.
                    # print(f"  allocate child {widget.interface}: {widget.interface.layout}")
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
