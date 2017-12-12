from toga_cocoa.container import Container
from toga_cocoa.libs import *

from .base import Widget


class ScrollContainer(Widget):
    def create(self):
        self.native = NSScrollView.alloc().init()
        self.native.autohidesScrollers = True
        self.native.borderType = NSNoBorder
        self.native.backgroundColor = NSColor.windowBackgroundColor
        # self.native.backgroundColor = NSColor.blueColor

        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.native.autoresizesSubviews = True

        # Add the layout constraints
        self.add_constraints()

        self.min_width_constraint = None
        self.min_height_constraint = None

    def set_content(self, widget):
        if widget.native is None:
            self.inner_container = Container()
            self.inner_container.content = widget
        else:
            self.inner_container = widget
        self.native.documentView = self.inner_container.native

        # We consider the width of the scrollbar to prevent content occlusion.
        self.vertical_scrollbar_width = 15 if self.interface.vertical else 0
        self.horizontal_scrollbar_width = 15 if self.interface.horizontal else 0

        # Enforce a minimum size based on the inner_container
        self.min_width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.native, NSLayoutAttributeWidth,
            NSLayoutRelationGreaterThanOrEqual,
            None, NSLayoutAttributeNotAnAttribute,
            1.0, self.inner_container.content.interface.layout.width + self.vertical_scrollbar_width
        )
        self.native.addConstraint(self.min_width_constraint)

        self.min_height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.native, NSLayoutAttributeHeight,
            NSLayoutRelationGreaterThanOrEqual,
            None, NSLayoutAttributeNotAnAttribute,
            1.0, 100 + self.horizontal_scrollbar_width
        )
        self.native.addConstraint(self.min_height_constraint)

    def apply_sub_layout(self):
        # TODO update minimum width after layout change.
        if self.interface.content is not None:
            self.inner_container.update_layout()
            # self.min_width_constraint.constant = self.inner_container.content.interface.layout.width + self.horizontal_scrollbar_width
            # self.min_height_constraint.constant = self.inner_container.content.interface.layout.height + self.vertical_scrollbar_width

    def set_vertical(self, value):
        self.native.hasVerticalScroller = value

    def set_horizontal(self, value):
        self.native.hasHorizontalScroller = value
