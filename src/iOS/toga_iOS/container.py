from .libs import (
    objc_method,
    NSLayoutAttributeTop, NSLayoutAttributeLeft,
    NSLayoutAttributeRight, NSLayoutAttributeBottom,
    NSLayoutRelationEqual, NSLayoutRelationGreaterThanOrEqual, NSLayoutRelationLessThanOrEqual,
    NSLayoutConstraint,
    NSLayoutPriority,
    NSRect, NSPoint, NSSize,
    UIView, UIColor
)


class Constraints:
    def __init__(self, widget):
        self.widget = widget
        self.__container = None

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
    def _container(self):
        return self.__container

    @_container.setter
    def _container(self, value):
        self.__container = value
        # print("Add constraints for", self._widget, 'in', self._container, self._widget.style.layout)
        self._left_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._widget._impl, NSLayoutAttributeLeft,
            NSLayoutRelationEqual,
            self._container._impl, NSLayoutAttributeLeft,
            1.0, self._widget.style.layout.absolute.left
        )
        self._container._impl.addConstraint_(self._left_constraint)

        self._top_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._widget._impl, NSLayoutAttributeTop,
            NSLayoutRelationEqual,
            self._container._impl, NSLayoutAttributeTop,
            1.0, self._widget.style.layout.absolute.top
        )
        self._container._impl.addConstraint_(self._top_constraint)

        self._width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._widget._impl, NSLayoutAttributeRight,
            NSLayoutRelationEqual,
            self._widget._impl, NSLayoutAttributeLeft,
            1.0, self._widget.style.layout.width
        )
        self._container._impl.addConstraint_(self._width_constraint)

        self._height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._widget._impl, NSLayoutAttributeBottom,
            NSLayoutRelationEqual,
            self._widget._impl, NSLayoutAttributeTop,
            1.0, self._widget.style.layout.height
        )
        self._container._impl.addConstraint_(self._height_constraint)

    def make_root(self):
        self.__container = None
        # print("Make ", self._widget, 'a root container')
        self._height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._widget._impl, NSLayoutAttributeBottom,
            NSLayoutRelationEqual,
            self._widget._impl, NSLayoutAttributeTop,
            1, 0,
        )
        self._widget._impl.addConstraint_(self._height_constraint)

        self._width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._widget._impl, NSLayoutAttributeRight,
            NSLayoutRelationEqual,
            self._widget._impl, NSLayoutAttributeLeft,
            1, 0,
        )
        self._widget._impl.addConstraint_(self._width_constraint)

    def update(self):
        # print("UPDATE", self._widget, 'in', self._container, 'to', self._widget.style.layout)
        if self._container:
            # print("     in", self._container)
            self.top = self._widget.style.layout.absolute.top
            self.left = self._widget.style.layout.absolute.left

            self.width = self._widget.style.layout.width
            self.height = self._widget.style.layout.height

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
        self._impl = TogaContainer.alloc().init()
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setBackgroundColor_(UIColor.whiteColor())

        self._content = None
        self._constraints = Constraints(self)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content._container = self

    @property
    def root_content(self):
        return self._content

    @root_content.setter
    def root_content(self, widget):
        self._content = widget
        self._content._container = self
        # Make the constraints object a root container.
        self._constraints.make_root()

    def _update_layout(self, **style):
        if self._content:
            self._constraints.width = self._content.style.layout.width
            self._constraints.height = self._content.style.layout.height

            self._content._update_layout(**style)
