from toga_cocoa.container import Container
from toga_cocoa.libs import *
from .base import Widget


class TogaSplitViewDelegate(NSObject):
    @objc_method
    def splitView_resizeSubviewsWithOldSize_(self, view, size: NSSize) -> None:
        view.adjustSubviews()

    @objc_method
    def splitViewDidResizeSubviews_(self, notification) -> None:
        # If the window is actually visible, and the split has moved,
        # a resize of all the content panels is required.
        if self.interface.window and self.interface.window._impl.native.isVisible:
            # print("SPLIT CONTAINER LAYOUT CHILDREN", self.interface._impl.containers[0].native.frame.size.width, self.interface._impl.containers[1].native.frame.size.width)
            self.interface._impl.apply_sub_layout()
            self.interface._impl.on_resize()


class SplitContainer(Widget):
    """ Cocoa SplitContainer implementation

    Todo:
        * update the minimum width of the whole SplitContainer based on the content of its sub layouts.
    """
    def create(self):
        self.native = NSSplitView.alloc().init()

        self.delegate = TogaSplitViewDelegate.alloc().init()
        self.delegate.interface = self.interface
        self.native.delegate = self.delegate

        # Add the layout constraints
        self.add_constraints()

        self.containers = []

    def add_content(self, position, widget):
        if widget.native is None:
            container = Container()
            container.content = widget
        else:
            container = widget

        self.containers.append(container)

        # Turn the autoresizing mask on the container widget
        # into constraints. This makes the container fill the
        # available space inside the SplitContainer.
        # FIXME Use Constrains to enforce min width and height of the containers otherwise width of 0 is possible.
        container.native.translatesAutoresizingMaskIntoConstraints = True
        self.native.addSubview(container.native)

    def apply_sub_layout(self):
        """ Force a layout update on the two sub layouts.
        """
        if self.interface.content:
            for i, (container, content) in enumerate(zip(self.containers, self.interface.content)):
                frame = container.native.frame
                content._update_layout(
                    width=frame.size.width,
                    height=frame.size.height
                )
        # Enforce a minimum size for the SplitContainer as a whole.
        self.min_width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.native, NSLayoutAttributeWidth,
            NSLayoutRelationGreaterThanOrEqual,
            None, NSLayoutAttributeNotAnAttribute,
            1.0, 300
        )
        self.native.addConstraint(self.min_width_constraint)

    def set_direction(self, value):
        self.native.vertical = value

    def on_resize(self):
        pass
