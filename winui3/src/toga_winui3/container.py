from math import ceil

from win32more.Microsoft.UI.Xaml import HorizontalAlignment, VerticalAlignment
from win32more.Microsoft.UI.Xaml.Controls import Canvas

from .widgets.properties.staged import StagingArea


class ContainerWidgets:
    """A class used to add, remove and keep a record of the Container's widgets."""

    def __init__(self, container):
        self._container = container
        self._widgets = []

    @property
    def _native(self):
        return self._container.native

    def add(self, widget):
        self._widgets.append(widget)
        self._native.Children.Append(widget.native)

    def remove(self, widget):
        index = self._widgets.index(widget)
        self._widgets.remove(widget)
        self._native.Children.RemoveAt(index)


class Container:
    """A container used for laying out WinUI 3 Toga widgets.

    A Container represents a region of window where the dimensions are controlled by
    the native runtime. It primarily does:
        - Reports the dimensions of the region to the Toga core interface.
        - Notifies the Toga core interface when the dimensions change.
        - Provides a native panel where the widgets.native classes can be attached.

    The actual layout of the widgets attached to a Container is determined by the style
    applicator of the Toga core interface.

    Attributes:
        native: The WinUI 3 panel where the widgets.native classes will be attached.
        on_refresh: A callback to be notified when this container's layout is refreshed.
        staging_area: A ContainerStagingArea instance which is used to stage widgets
            that require a native panel to calculate content-based constraints.
        widgets: A ContainerWidgets instance which adds, removes and keeps a record of
            the widgets attached to the native panel.
    """

    def __init__(self, native_panel: Canvas, on_refresh=None):
        """Initialize a Container using a given native panel.

        :param native_panel: The native panel where the widgets.native classes can be
            attached.
        :param on_refresh: A callback to be notified when this container's layout is
            refreshed.
        """
        self.native = native_panel
        self.native.HorizontalAlignment = HorizontalAlignment.Stretch
        self.native.VerticalAlignment = VerticalAlignment.Stretch
        self.native.event_handler.SizeChanged += self.native_event_size_changed

        self._content = None
        self._on_refresh = on_refresh

        self.widgets = ContainerWidgets(self)
        self.staging_area = StagingArea(self)

    ####################################################################################
    # Container geometry
    #
    # Note: WinUI 3 sizes are given in CSS pixels and can be factional valued. However,
    #       the Toga core interface uses whole CSS pixels for layouts. When the native
    #       values are rounded down noticeable bars appear at the right side and bottom
    #       of the container during resize. Rounding up causing the content to overlap
    #       with the edge and the bars disappear. This is judged to be the lesser of two
    #       evils.
    ####################################################################################

    @property
    def width(self):
        return ceil(self.native.ActualSize.X)

    @property
    def height(self):
        return ceil(self.native.ActualSize.Y)

    ####################################################################################
    # Container content
    ####################################################################################

    @property
    def content(self):
        """The root widget for the tree of widgets laid out by the container.

        All children of the root widget will also be added to the container as a result
        of assigning content.

        If the container already has content, the old content will be replaced. The old
        root widget and all its children will be removed from the container.
        """
        return self._content

    @content.setter
    def content(self, widget):
        if self._content:
            self._content.container = None

        self._content = widget
        # FIXME: Remove the 'no branch' when ScrollContainer is implemented.
        if widget:  # pragma: no branch
            widget.container = self

    ####################################################################################
    # Container refreshing
    ####################################################################################

    def native_event_size_changed(self, sender, args):
        if self.content is not None:
            self.content.interface.refresh()

    def refreshed(self):
        self._on_refresh()
