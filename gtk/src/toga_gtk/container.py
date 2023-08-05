from .libs import Gdk, Gtk


class TogaContainerLayoutManager(Gtk.LayoutManager):
    def __init__(self):
        super().__init__()

    def do_get_request_mode(self, widget):
        return Gtk.SizeRequestMode.CONSTANT_SIZE

    def do_measure(self, widget, orientation, for_size):
        """Return (recomputing if necessary) the preferred size for the container.

        The preferred size of the container is its minimum size. This preference
        will be overridden with the layout size when the layout is applied.

        If the container does not yet have content, the minimum size is set to 0x0.
        """
        # print("GET PREFERRED SIZE", self._content)
        if widget._content is None:
            return 0, 0, -1, -1

        # Ensure we have an accurate min layout size
        widget.recompute()

        # The container will conform to the size of the allocation it is given,
        # so the min and preferred size are the same.
        if orientation == Gtk.Orientation.HORIZONTAL:
            return widget.min_width, widget.min_width, -1, -1
        elif orientation == Gtk.Orientation.VERTICAL:
            return widget.min_height, widget.min_height, -1, -1

    def do_allocate(self, widget, width, height, baseline):
        """Perform the actual layout for the all widget's children.

        The container will assume whatever size it has been given by GTK - usually the
        full space of the window that holds the container. The layout will then be re-
        computed based on this new available size, and that new geometry will be applied
        to all child widgets of the container.
        """
        # print(widget._content, f"Container layout {width}x{height} @ 0x0")

        if widget._content:
            # The issue of calling this virtual method in response to
            # irrelevant events like button clicks has been solved.
            #
            # Re-evaluate the layout using the provided dimensions as
            # the basis for geometry.
            # print("REFRESH LAYOUT", width, height)
            widget._content.interface.refresh()

            # WARNING! This is the list of children of the *container*, not
            # the Toga widget. Toga maintains a tree of children; all nodes
            # in that tree are direct children of the container.
            child_widget = widget.get_last_child()
            while child_widget is not None:
                if not child_widget.get_visible():
                    # print("  not visible {child_widget.interface}")
                    pass
                else:
                    # Set the size of the child widget to the computed layout size.
                    # print(f"  allocate child {child_widget.interface}: {child_widget.interface.layout}")
                    child_widget_allocation = Gdk.Rectangle()
                    child_widget_allocation.x = (
                        child_widget.interface.layout.absolute_content_left
                    )
                    child_widget_allocation.y = (
                        child_widget.interface.layout.absolute_content_top
                    )
                    child_widget_allocation.width = (
                        child_widget.interface.layout.content_width
                    )
                    child_widget_allocation.height = (
                        child_widget.interface.layout.content_height
                    )
                    child_widget.size_allocate(child_widget_allocation, -1)

                    child_widget = child_widget.get_prev_sibling()


class TogaContainer(Gtk.Fixed):
    """A GTK container widget implementing Toga's layout.

    This is a GTK widget, with no Toga interface manifestation.
    """

    def __init__(self):
        super().__init__()

        # We don’t have access to the existing layout manager, we must create
        # our custom layout manager class.
        layout_manager = TogaContainerLayoutManager()
        self.set_layout_manager(layout_manager)

        self._content = None
        self.min_width = 100
        self.min_height = 100

        # GDK/GTK always renders at 96dpi. When HiDPI mode is enabled, it is
        # managed at the compositor level. See
        # https://wiki.archlinux.org/index.php/HiDPI#GDK_3_(GTK_3) for details
        self.dpi = 96
        self.baseline_dpi = self.dpi

    @property
    def width(self):
        """The display width of the container.

        If the container doesn't have any content yet, the width is 0.
        """
        if self._content is None:
            return 0

        is_possible, bounds = self.compute_bounds(self)
        if is_possible:
            return bounds.get_width()
        return self.get_width()

    @property
    def height(self):
        """The display height of the container.

        If the container doesn't have any content yet, the height is 0.
        """
        if self._content is None:
            return 0

        is_possible, bounds = self.compute_bounds(self)
        if is_possible:
            return bounds.get_height()
        return self.get_height()

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

        Any widgets known to be dirty will be rehinted. The minimum possible
        layout size for the container will also be recomputed.
        """
        if self._content:
            # If any of the widgets have been marked as dirty,
            # recompute their bounds, and re-evaluate the minimum
            # allowed size of the layout.
            child_widget = self.get_last_child()
            while child_widget is not None:
                child_widget._impl.rehint()
                child_widget = child_widget.get_prev_sibling()

            # Compute the layout using a 0-size container
            self._content.interface.style.layout(
                self._content.interface, TogaContainer()
            )

            # print(" computed min layout", self._content.interface.layout)
            self.min_width = self._content.interface.layout.width
            self.min_height = self._content.interface.layout.height
