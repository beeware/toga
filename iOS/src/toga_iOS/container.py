from .libs import (
    NSLayoutAttributeBottom,
    NSLayoutAttributeLeft,
    NSLayoutAttributeRight,
    NSLayoutAttributeTop,
    NSLayoutConstraint,
    NSLayoutRelationGreaterThanOrEqual,
    UIApplication,
    UIColor,
    UINavigationController,
    UIView,
    UIViewController,
)


class BaseContainer:
    def __init__(self, content=None, on_refresh=None):
        """A base class for iOS containers.

        :param content: The widget impl that is the container's initial content.
        :param on_refresh: The callback to be notified when this container's layout is
            refreshed.
        """
        self._content = content
        self.on_refresh = on_refresh

        # iOS renders everything at 96dpi.
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


class Container(BaseContainer):
    def __init__(
        self,
        content=None,
        min_width=100,
        min_height=100,
        layout_native=None,
        on_refresh=None,
    ):
        """
        :param content: The widget impl that is the container's initial content.
        :param min_width: The minimum width to enforce on the container
        :param min_height: The minimum height to enforce on the container
        :param layout_native: The native widget that should be used to provide size
            hints to the layout. This will usually be the container widget itself;
            however, for widgets like ScrollContainer where the layout needs to be
            computed based on a different size to what will be rendered, the source of
            the size can be different.
        :param on_refresh: The callback to be notified when this container's layout is
            refreshed.
        """
        super().__init__(content=content, on_refresh=on_refresh)
        self.native = UIView.alloc().init()
        self.native.translatesAutoresizingMaskIntoConstraints = True

        self.layout_native = self.native if layout_native is None else layout_native

        try:
            # systemBackgroundColor() was introduced in iOS 13
            # We don't test on iOS 12, so mark the other branch as nocover
            self.native.backgroundColor = UIColor.systemBackgroundColor()
        except AttributeError:  # pragma: no cover
            self.native.backgroundColor = UIColor.whiteColor

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
        return self.native.bounds.size.width

    @property
    def height(self):
        return self.native.bounds.size.height

    @property
    def top_offset(self):
        return 0

    def set_min_width(self, width):
        self._min_width_constraint.constant = width

    def set_min_height(self, height):
        self._min_height_constraint.constant = height


class RootContainer(Container):
    def __init__(
        self,
        content=None,
        min_width=100,
        min_height=100,
        layout_native=None,
        on_refresh=None,
    ):
        """
        :param content: The widget impl that is the container's initial content.
        :param min_width: The minimum width to enforce on the container
        :param min_height: The minimum height to enforce on the container
        :param layout_native: The native widget that should be used to provide
            size hints to the layout. This will usually be the container widget
            itself; however, for widgets like ScrollContainer where the layout
            needs to be computed based on a different size to what will be
            rendered, the source of the size can be different.
        :param on_refresh: The callback to be notified when this container's
            layout is refreshed.
        """
        super().__init__(
            content=content,
            min_width=min_width,
            min_height=min_height,
            layout_native=layout_native,
            on_refresh=on_refresh,
        )

        # Construct a NavigationController that provides a navigation bar, and
        # is able to maintain a stack of navigable content. This is intialized
        # with a root UIViewController that is the actual content
        self.content_controller = UIViewController.alloc().init()
        self.controller = UINavigationController.alloc().initWithRootViewController(
            self.content_controller
        )

        # Set the controller's view to be the root content widget
        self.content_controller.view = self.native

    @property
    def height(self):
        return self.native.bounds.size.height - self.top_offset

    @property
    def top_offset(self):
        return (
            UIApplication.sharedApplication.statusBarFrame.size.height
            + self.controller.navigationBar.frame.size.height
        )

    @property
    def title(self):
        return self.controller.topViewController.title

    @title.setter
    def title(self, value):
        self.controller.topViewController.title = value
