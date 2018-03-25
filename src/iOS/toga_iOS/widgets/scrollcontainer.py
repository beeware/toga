from rubicon.objc import CGSizeMake
from toga_iOS.libs import (
    NSLayoutAttributeBottom,
    NSLayoutAttributeLeading,
    NSLayoutAttributeTop,
    NSLayoutAttributeTrailing,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
    UIScrollView
)
from toga_iOS.window import (
    iOSViewport,
    UIColor
)
from travertino.size import at_least
from .base import Widget


class ScrollContainer(Widget):
    def update_content_size(self):
        # We need a layout pass to figure out how big the scrollable area should be
        self.current_content.interface.refresh()
        
        content_width = 0
        padding_horizontal = 0
        content_height = 0
        padding_vertical = 0
        
        if self.horizontal_enabled:
            content_width = self.current_content.interface.layout.width
            padding_horizontal = self.current_content.interface.style.padding_left + self.current_content.interface.style.padding_right
        else:
            content_width = self.native.frame.size.width
        
        if self.vertical_enabled:
            content_height = self.current_content.interface.layout.height
            padding_vertical = self.current_content.interface.style.padding_top + self.current_content.interface.style.padding_bottom
            # pad the scrollview for the statusbar offset
            padding_vertical = padding_vertical + self.current_content.viewport.statusbar_height
        else:
            content_height = self.native.frame.size.height

        self.native.setContentSize_(CGSizeMake(content_width + padding_horizontal,
                                               content_height + padding_vertical))

    def constrain_to_scrollview(self, widget):
        # The scrollview should know the content size as long as the
        # view contained has an intrinsic size and the constraints are
        # not ambiguous in any axis.
        view = widget.native
        leading_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            view,
            NSLayoutAttributeLeading,
            NSLayoutRelationEqual,
            self.native,
            NSLayoutAttributeLeading,
            1.0,
            0
        )
        trailing_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.native,
            NSLayoutAttributeTrailing,
            NSLayoutRelationEqual,
            view,
            NSLayoutAttributeTrailing,
            1.0,
            0
        )
        top_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            view,
            NSLayoutAttributeTop,
            NSLayoutRelationEqual,
            self.native,
            NSLayoutAttributeTop,
            1.0,
            0
        )
        bottom_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
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
        self.current_content = None
        self.vertical_enabled = True
        self.horizontal_enabled = True
        self.native = UIScrollView.alloc().init()
        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.native.backgroundColor = UIColor.whiteColor
        self.add_constraints()

    def set_content(self, widget):
        if self.current_content != None:
            self.current_content.removeFromSuperview()
        self.current_content = widget
        self.native.addSubview(widget.native)
        widget.viewport = iOSViewport(self.native)

        for child in widget.interface.children:
            child._impl.container = widget

        self.constrain_to_scrollview(widget)

    def set_vertical(self, value):
        self.vertical_enabled = value
        if self.current_content:
            self.update_content_size()

    def set_horizontal(self, value):
        self.horizontal_enabled = value
        if self.current_content:
            self.update_content_size()

    def rehint(self):
        self.update_content_size()
