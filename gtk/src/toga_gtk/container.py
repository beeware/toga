from .libs import Gdk, Gtk

#######################################################################################
# Implementation notes:
#
# GDK/GTK renders everything at 96dpi. When HiDPI mode is enabled, it is managed at the
# compositor level. See https://wiki.archlinux.org/index.php/HiDPI#GDK_3_(GTK_3) for
# details.
#######################################################################################


class TogaContainerLayoutManager(Gtk.LayoutManager):
    def __init__(self):
        super().__init__()

    def do_get_request_mode(self, container):
        return Gtk.SizeRequestMode.CONSTANT_SIZE

    def do_measure(self, container, orientation, for_size):
        """Return (recomputing if necessary) the preferred size for the container.

        The preferred size of the container is its minimum size. This preference
        will be overridden with the layout size when the layout is applied.

        If the container does not yet have content, the minimum size is set to 0x0.
        """
        # print("GET PREFERRED SIZE", self._content)
        if container._content is None:
            return 0, 0, -1, -1

        # Ensure we have an accurate min layout size
        container.recompute()

        # The container will conform to the size of the allocation it is given,
        # so the min and preferred size are the same.
        if orientation == Gtk.Orientation.HORIZONTAL:
            return container.min_width, container.min_width, -1, -1
        elif orientation == Gtk.Orientation.VERTICAL:
            return container.min_height, container.min_height, -1, -1

    def do_allocate(self, container, width, height, baseline):
        """Perform the actual layout for the all widget's children.

        The manager will assume whatever size it has been given by GTK - usually the
        full space of the window that holds the container (`widget`). The layout will
        then be re-computed based on this new available size, and that new geometry
        will be applied to all child widgets of the container.
        """
        # print(widget._content, f"Container layout {width}x{height} @ 0x0")

        if container._content:
            # Re-evaluate the layout using the  size as the basis for geometry
            # print("REFRESH LAYOUT", width, height)
            container._content.interface.style.layout(
                container._content.interface, container
            )

            # Ensure the minimum content size from the layout is retained
            container.min_width = container._content.interface.layout.min_width
            container.min_height = container._content.interface.layout.min_height

            # WARNING! This is the list of children of the *container*, not
            # the Toga widget. Toga maintains a tree of children; all nodes
            # in that tree are direct children of the container.
            child_widget = container.get_last_child()
            while child_widget is not None:
                if child_widget.get_visible():
                    # Set the allocation of the child widget to the computed
                    # layout size.
                    # print(
                    #     f" allocate child {child_widget.interface}: {child_widget.interface.layout}"
                    # )
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

        # The layout has been redrawn
        container.needs_redraw = False


class TogaContainer(Gtk.Box):
    """A GTK container widget implementing Toga's layout.

    This is a GTK widget, with no Toga interface manifestation.
    """

    def __init__(self):
        super().__init__()

        # Because we don’t have access to the existing layout manager, we must
        # create our custom layout manager class.
        layout_manager = TogaContainerLayoutManager()
        self.set_layout_manager(layout_manager)

        self._content = None
        self.min_width = 100
        self.min_height = 100

        self.dpi = 96
        self.baseline_dpi = self.dpi

        # NOTE: These following two properties were added primarily to help in
        # testing process, we adapted them later to improve the performance in
        # determining when re-hinting the widget is needed.
        #
        # A flag that can be used to explicitly flag that a redraw is required.
        self.needs_redraw = True
        # The dirty widgets are the set of widgets that are known to need
        # re-hinting before any redraw occurs.
        self._dirty_widgets = set()

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
        return self.compute_bounds(self)[1].get_width()

    @property
    def height(self):
        """The display height of the container.

        If the container doesn't have any content yet, the height is 0.
        """
        if self._content is None:
            return 0
        return self.compute_bounds(self)[1].get_height()

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
        """Rehint and re-layout the container's content.

        The minimum possible layout size for the container will also
        be recomputed.

        Note: This must be used wisely because it's relatively expensive.
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
