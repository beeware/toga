from rubicon.objc import objc_method

from .libs import (
    NSLayoutAttributeTop, NSLayoutAttributeLeft,
    NSLayoutAttributeRight, NSLayoutAttributeBottom,
    NSLayoutRelationEqual, NSLayoutConstraint,
    UIView, UIColor
)


class Constraints:
    def __init__(self, widget):
        self._widget = widget
        self._container = None

        self._width_constraint = None
        self._height_constraint = None

        self._left_constraint = None
        self._top_constraint = None

    @property
    def widget(self):
        return self._widget

    @widget.setter
    def widget(self, value):
        self._widget = value

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, value):
        self._container = value
        # print("Add constraints for", self._widget, 'in', self._container, self._widget.interface.layout)
        self._left_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._widget.native, NSLayoutAttributeLeft,
            NSLayoutRelationEqual,
            self._container.native, NSLayoutAttributeLeft,
            1.0, self._widget.interface.layout.absolute.left
        )
        self._container.native.addConstraint_(self._left_constraint)

        self._top_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._widget.native, NSLayoutAttributeTop,
            NSLayoutRelationEqual,
            self._container.native, NSLayoutAttributeTop,
            1.0, self._widget.interface.layout.absolute.top
        )
        self._container.native.addConstraint_(self._top_constraint)

        self._width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._widget.native, NSLayoutAttributeRight,
            NSLayoutRelationEqual,
            self._widget.native, NSLayoutAttributeLeft,
            1.0, self._widget.interface.layout.width
        )
        self._container.native.addConstraint_(self._width_constraint)

        self._height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._widget.native, NSLayoutAttributeBottom,
            NSLayoutRelationEqual,
            self._widget.native, NSLayoutAttributeTop,
            1.0, self._widget.interface.layout.height
        )
        self._container.native.addConstraint_(self._height_constraint)

    def update(self, x, y, width, height):
        # print("UPDATE", self._widget, 'in', self._container, 'to', self._widget.interface.layout, self._widget.interface.layout.absolute.top, self._widget.interface.layout.absolute.left)
        if self._container:
            # print("     in", self._container)
            self.top = y
            self.left = x

            self.width = width
            self.height = height
