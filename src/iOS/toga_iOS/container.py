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

    def make_root(self):
        self._container = None
        # print("Make ", self._widget, 'a root container')
        self._height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._widget.native, NSLayoutAttributeBottom,
            NSLayoutRelationEqual,
            self._widget.native, NSLayoutAttributeTop,
            1, 0,
        )
        self._widget.native.addConstraint_(self._height_constraint)

        self._width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._widget.native, NSLayoutAttributeRight,
            NSLayoutRelationEqual,
            self._widget.native, NSLayoutAttributeLeft,
            1, 0,
        )
        self._widget.native.addConstraint_(self._width_constraint)

    def update(self):
        # print("UPDATE", self._widget, 'in', self._container, 'to', self._widget.interface.layout, self._widget.interface.layout.absolute.top, self._widget.interface.layout.absolute.left)
        if self._container:
            # print("     in", self._container)
            self.top = self._widget.interface.layout.absolute.top
            self.left = self._widget.interface.layout.absolute.left

            self.width = self._widget.interface.layout.width
            self.height = self._widget.interface.layout.height

    @property
    def width(self):
        if self._width_constraint:
            return self._width_constraint.constant

    @width.setter
    def width(self, value):
        if self._width_constraint:
            # print("SET WIDTH", self._widget, value)
            self._width_constraint.constant = value

    @property
    def height(self):
        if self._height_constraint:
            return self._height_constraint.constant

    @height.setter
    def height(self, value):
        if self._height_constraint:
            # print("SET HEIGHT", self._widget, value)
            self._height_constraint.constant = value

    @property
    def left(self):
        if self._left_constraint:
            return self._left_constraint.constant

    @left.setter
    def left(self, value):
        if self._left_constraint:
            # print("SET LEFT", self._widget, value)
            self._left_constraint.constant = value

    @property
    def top(self):
        if self._top_constraint:
            return self._top_constraint.constant

    @top.setter
    def top(self, value):
        if self._top_constraint:
            # print("SET TOP", self._widget, value)
            self._top_constraint.constant = value


class TogaContainer(UIView):
    @objc_method
    def isFlipped(self) -> bool:
        # Default Cocoa coordinate frame is around the wrong way.
        return True

    @objc_method
    def display(self) -> None:
        self.layer.setNeedsDisplay_(True)
        self.layer.displayIfNeeded()


class Container:
    def __init__(self):
        self.native = TogaContainer.alloc().init()
        self.native.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self.native.setBackgroundColor_(UIColor.whiteColor)

        self._content = None
        self.constraints = Constraints(self)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.container = self

    @property
    def root_content(self):
        return self.content

    @root_content.setter
    def root_content(self, widget):
        self._content = widget
        self._content.container = self
        # Make the constraints object a root container.
        self.constraints.make_root()

    def update_layout(self, **style):
        if self._content:
            self.constraints.width = self._content.interface.layout.width
            self.constraints.height = self._content.interface.layout.height

            self._content.interface._update_layout(**style)
