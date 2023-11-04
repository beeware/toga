from .libs import Gdk, Gtk

#######################################################################################
# Implementation notes:
#
# GDK/GTK renders everything at 96dpi. When HiDPI mode is enabled, it is managed at the
# compositor level. See https://wiki.archlinux.org/index.php/HiDPI#GDK_3_(GTK_3) for
# details.
#######################################################################################


class TogaContainer(Gtk.Fixed):
    """A GTK container widget implementing Toga's layout.

    This is a GTK widget, with no Toga interface manifestation.
    """

    def __init__(self):
        super().__init__()
        self._content = None
        self.min_width = 100
        self.min_height = 100

        self.dpi = 96
        self.baseline_dpi = self.dpi

        # The dirty widgets are the set of widgets that are known to need
        # re-hinting before any redraw occurs.
        self._dirty_widgets = set()

        # A flag that can be used to explicitly flag that a redraw is required.
        self.needs_redraw = True

    def refreshed(self):
        pass

    def make_dirty(self, widget=None):
        """Mark the container (or a specific widget in the container) as dirty.

        :param widget: If provided, this widget will be rehinted before the next layout.
        """
        self.needs_redraw = True
        if widget is not None:
            self._dirty_widgets.add(widget)
        self.queue_resize()

    @property
    def width(self):
        """The display width of the container.

        If the container doesn't have any content yet, the width is 0.
        """
        if self._content is None:
            return 0
        return self.get_allocated_width()

    @property
    def height(self):
        """The display height of the container.

        If the container doesn't have any content yet, the height is 0.
        """
        if self._content is None:
            return 0
        return self.get_allocated_height()

    @property
    def content(self):
        """The Toga implementation widget that is the root content of this container.

        All children of the root content will also be added to the container as a result
        of assigning content.

        If the container already has content, the old content will be replaced. The old
        root content and all it's children will be removed from the container.
        """
        return self._content

    @content.setter
    def content(self, widget):
        if self._content:
            self._content.container = None

        self._content = widget
        if widget:
            widget.container = self
            self.make_dirty(widget)
        else:
            self.make_dirty()

    def recompute(self):
        """Rehint and re-layout the container's content, if necessary.

        Any widgets known to be dirty will be rehinted. The minimum possible layout size
        for the container will also be recomputed.
        """
        if self._content and self._dirty_widgets:
            # If any of the widgets have been marked as dirty,
            # recompute their bounds, and re-evaluate the minimum
            # allowed size for the layout.
            while self._dirty_widgets:
                widget = self._dirty_widgets.pop()
                widget.rehint()

            # Recompute the layout
            self._content.interface.style.layout(self._content.interface, self)

            self.min_width = self._content.interface.layout.min_width
            self.min_height = self._content.interface.layout.min_height

    def do_get_preferred_width(self):
        """Return (recomputing if necessary) the preferred width for the container.

        The preferred size of the container is its minimum size. This
        preference will be overridden with the layout size when the layout is
        applied.

        If the container does not yet have content, the minimum width is set to
        0.
        """
        # print("GET PREFERRED WIDTH", self._content)
        if self._content is None:
            return 0, 0

        # Ensure we have an accurate min layout size
        self.recompute()

        # The container will conform to the size of the allocation it is given,
        # so the min and preferred size are the same.
        return self.min_width, self.min_width

    def do_get_preferred_height(self):
        """Return (recomputing if necessary) the preferred height for the container.

        The preferred size of the container is its minimum size. This preference will be
        overridden with the layout size when the layout is applied.

        If the container does not yet have content, the minimum height is set to 0.
        """
        # print("GET PREFERRED HEIGHT", self._content)
        if self._content is None:
            return 0, 0

        # Ensure we have an accurate min layout size
        self.recompute()

        # The container will conform to the size of the allocation it is given,
        # so the min and preferred size are the same.
        return self.min_height, self.min_height

    def do_size_allocate(self, allocation):
        """Perform the actual layout for the widget, and all it's children.

        The container will assume whatever size it has been given by GTK - usually the
        full space of the window that holds the container. The layout will then be re-
        computed based on this new available size, and that new geometry will be applied
        to all child widgets of the container.
        """
        # print(self._content, f"Container layout {allocation.width}x{allocation.height} @ {allocation.x}x{allocation.y}")  # noqa: E501

        # The container will occupy the full space it has been allocated.
        resized = (allocation.width, allocation.height) != (self.width, self.height)
        self.set_allocation(allocation)

        if self._content:
            # This function may be called in response to irrelevant events like button clicks,
            # so only refresh if we really need to.
            if resized or self.needs_redraw:
                # Re-evaluate the layout using the allocation size as the basis for geometry
                # print("REFRESH LAYOUT", allocation.width, allocation.height)
                self._content.interface.style.layout(self._content.interface, self)

                # Ensure the minimum content size from the layout is retained
                self.min_width = self._content.interface.layout.min_width
                self.min_height = self._content.interface.layout.min_height

            # WARNING! This is the list of children of the *container*, not
            # the Toga widget. Toga maintains a tree of children; all nodes
            # in that tree are direct children of the container.
            for widget in self.get_children():
                if widget.get_visible():
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

        # The layout has been redrawn
        self.needs_redraw = False
