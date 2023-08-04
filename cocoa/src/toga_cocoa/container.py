from rubicon.objc import objc_method

from .libs import (
    NSLayoutAttributeBottom,
    NSLayoutAttributeLeft,
    NSLayoutAttributeRight,
    NSLayoutAttributeTop,
    NSLayoutConstraint,
    NSLayoutRelationGreaterThanOrEqual,
    NSView,
)


class TogaView(NSView):
    @objc_method
    def isFlipped(self) -> bool:
        # Default Cocoa coordinate frame is around the wrong way.
        return True


class BaseContainer:
    def __init__(self, on_refresh=None):
        """A base class for macOS containers.

        :param on_refresh: The callback to be notified when this container's layout is
            refreshed.
        """
        self._content = None
        self.on_refresh = on_refresh
        # macOS always renders at 96dpi. Scaling is handled
        # transparently at the level of the screen compositor.
        self.dpi = 96
        self.baseline_dpi = self.dpi

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

    def refreshed(self):
        if self.on_refresh:
            self.on_refresh()


class MinimumContainer(BaseContainer):
    def __init__(self):
        """A container for evaluating the minimum possible size for a layout"""
        super().__init__()
        self.width = 0
        self.height = 0


class Container(BaseContainer):
    def __init__(
        self,
        min_width=100,
        min_height=100,
        layout_native=None,
        on_refresh=None,
    ):
        """A container for real layouts.

        Creates and enforces minimum size constraints on the container widget.

        :param min_width: The minimum width to enforce on the container
        :param min_height: The minimum height to enforce on the container
        :param layout_native: The native widget that should be used to provide size
            hints to the layout. By default, this will usually be the container widget
            itself; however, for widgets like ScrollContainer where the layout needs to
            be computed based on a different size to what will be rendered, the source
            of the size can be different.
        :param on_refresh: The callback to be notified when this container's layout is
            refreshed.
        """
        super().__init__(on_refresh=on_refresh)

        self.native = TogaView.alloc().init()
        self.layout_native = self.native if layout_native is None else layout_native

        # Enforce a minimum size based on the content size.
        # This is enforcing the *minimum* size; the container might actually be
        # bigger. If the window is resizable, using >= allows the window to
        # be dragged larger; if not resizable, it enforces the smallest
        # size that can be programmatically set on the window.
        self._min_width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # noqa: E501
            self.native,
            NSLayoutAttributeRight,
            NSLayoutRelationGreaterThanOrEqual,
            self.native,
            NSLayoutAttributeLeft,
            1.0,
            min_width,
        )
        self.native.addConstraint(self._min_width_constraint)

        self._min_height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # noqa: E501
            self.native,
            NSLayoutAttributeBottom,
            NSLayoutRelationGreaterThanOrEqual,
            self.native,
            NSLayoutAttributeTop,
            1.0,
            min_height,
        )
        self.native.addConstraint(self._min_height_constraint)

    @property
    def width(self):
        return self.layout_native.frame.size.width

    @property
    def height(self):
        return self.layout_native.frame.size.height

    @property
    def min_width(self):
        return self._min_width_constraint.constant

    @min_width.setter
    def min_width(self, width):
        self._min_width_constraint.constant = width

    @property
    def min_height(self):
        return self._min_height_constraint.constant

    @min_height.setter
    def min_height(self, height):
        self._min_height_constraint.constant = height
