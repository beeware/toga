from rubicon.objc import CGSizeMake

from toga_iOS.libs import (
    NSLayoutAttributeBottom,
    NSLayoutAttributeLeading,
    NSLayoutAttributeTop,
    NSLayoutAttributeTrailing,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
    UIColor,
    UIScrollView
)
from toga_iOS.widgets.base import Widget
from toga_iOS.window import iOSViewport


class ScrollContainer(Widget):
    def update_content_size(self):
        # We need a layout pass to figure out how big the scrollable area should be
        scrollable_content = self.interface.content._impl
        scrollable_content.interface.refresh()

        content_width = 0
        padding_horizontal = 0
        content_height = 0
        padding_vertical = 0

        if self.interface.horizontal:
            content_width = scrollable_content.interface.layout.width
            padding_horizontal = (
                scrollable_content.interface.style.padding_left
                + scrollable_content.interface.style.padding_right
            )
        else:
            content_width = self.native.frame.size.width

        if self.interface.vertical:
            content_height = scrollable_content.interface.layout.height
            padding_vertical = (
                scrollable_content.interface.style.padding_top
                + scrollable_content.interface.style.padding_bottom
            )
            # pad the scrollview for the statusbar offset
            padding_vertical = padding_vertical + scrollable_content.viewport.statusbar_height
        else:
            content_height = self.native.frame.size.height

        self.native.setContentSize_(
            CGSizeMake(
                content_width + padding_horizontal,
                content_height + padding_vertical,
            )
        )

    def constrain_to_scrollview(self, widget):
        # The scrollview should know the content size as long as the
        # view contained has an intrinsic size and the constraints are
        # not ambiguous in any axis.
        view = widget.native
        leading_constraint = \
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                view,
                NSLayoutAttributeLeading,
                NSLayoutRelationEqual,
                self.native,
                NSLayoutAttributeLeading,
                1.0,
                0
            )
        trailing_constraint = \
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.native,
                NSLayoutAttributeTrailing,
                NSLayoutRelationEqual,
                view,
                NSLayoutAttributeTrailing,
                1.0,
                0
            )
        top_constraint = \
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                view,
                NSLayoutAttributeTop,
                NSLayoutRelationEqual,
                self.native,
                NSLayoutAttributeTop,
                1.0,
                0
            )
        bottom_constraint = \
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.native,
                NSLayoutAttributeBottom,
                NSLayoutRelationEqual,
                view,
                NSLayoutAttributeBottom,
                1.0,
                0
            )
        self.native.addConstraints_([
            leading_constraint,
            trailing_constraint,
            top_constraint,
            bottom_constraint
        ])

    def create(self):
        self.native = UIScrollView.alloc().init()
        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.native.backgroundColor = UIColor.whiteColor
        self.add_constraints()

    def set_content(self, widget):
        if self.interface.content is not None:
            self.interface.content._impl.native.removeFromSuperview()
        self.native.addSubview(widget.native)
        widget.viewport = iOSViewport(self.native)

        for child in widget.interface.children:
            child._impl.container = widget

        self.constrain_to_scrollview(widget)

    def set_vertical(self, value):
        if self.interface.content:
            self.update_content_size()

    def set_horizontal(self, value):
        if self.interface.content:
            self.update_content_size()

    def rehint(self):
        if self.interface.content:
            self.update_content_size()

    def set_on_scroll(self, on_scroll):
        self.interface.factory.not_implemented("ScrollContainer.set_on_scroll()")

    def get_vertical_position(self):
        self.interface.factory.not_implemented(
            "ScrollContainer.get_vertical_position()"
        )
        return 0

    def set_vertical_position(self, vertical_position):
        self.interface.factory.not_implemented(
            "ScrollContainer.set_vertical_position()"
        )

    def get_horizontal_position(self):
        self.interface.factory.not_implemented(
            "ScrollContainer.get_horizontal_position()"
        )
        return 0

    def set_horizontal_position(self, horizontal_position):
        self.interface.factory.not_implemented(
            "ScrollContainer.set_horizontal_position()"
        )
