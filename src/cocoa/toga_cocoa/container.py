from .libs import (
    objc_method,
    NSLayoutAttributeTop, NSLayoutAttributeLeft,
    NSLayoutAttributeRight, NSLayoutAttributeBottom,
    NSLayoutRelationEqual, NSLayoutConstraint,
    NSView
)


class Constraints:
    def __init__(self, widget):
        """

        Args:
            widget (:class: toga-cocoa.Widget): The widget that should be constraint.
        """
        self.widget = widget
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
        # print("Add constraints for", self.widget, 'in', self.container, self.widget.interface.layout)
        self._left_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.widget.native, NSLayoutAttributeLeft,
            NSLayoutRelationEqual,
            self.container.native, NSLayoutAttributeLeft,
            1.0, self.widget.interface.layout.absolute.left
        )
        self.container.native.addConstraint_(self._left_constraint)

        self._top_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.widget.native, NSLayoutAttributeTop,
            NSLayoutRelationEqual,
            self.container.native, NSLayoutAttributeTop,
            1.0, self.widget.interface.layout.absolute.top
        )
        self.container.native.addConstraint_(self._top_constraint)

        self._width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.widget.native, NSLayoutAttributeRight,
            NSLayoutRelationEqual,
            self.widget.native, NSLayoutAttributeLeft,
            1.0, self.widget.interface.layout.width
        )
        self.container.native.addConstraint_(self._width_constraint)

        self._height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.widget.native, NSLayoutAttributeBottom,
            NSLayoutRelationEqual,
            self.widget.native, NSLayoutAttributeTop,
            1.0, self.widget.interface.layout.height
        )
        self.container.native.addConstraint_(self._height_constraint)

    def update(self):
        # print("UPDATE", self.widget, 'in', self.container, 'to', self.widget.layout, self.widget.layout.absolute.top, self.widget.layout.absolute.left)
        if self.container:
            # print("     in", self.container)
            self.top = self.widget.interface.layout.absolute.top
            self.left = self.widget.interface.layout.absolute.left

            self.width = self.widget.interface.layout.width
            self.height = self.widget.interface.layout.height

    @property
    def width(self):
        if self._width_constraint:
            return self._width_constraint.constant

    @width.setter
    def width(self, value):
        if self._width_constraint:
            # print("SET WIDTH", self.widget, value)
            self._width_constraint.constant = value

    @property
    def height(self):
        if self._height_constraint:
            return self._height_constraint.constant

    @height.setter
    def height(self, value):
        if self._height_constraint:
            # print("SET HEIGHT", self.widget, value)
            self._height_constraint.constant = value

    @property
    def left(self):
        if self._left_constraint:
            return self._left_constraint.constant

    @left.setter
    def left(self, value):
        if self._left_constraint:
            # print("SET LEFT", self.widget, value)
            self._left_constraint.constant = value

    @property
    def top(self):
        if self._top_constraint:
            return self._top_constraint.constant

    @top.setter
    def top(self, value):
        if self._top_constraint:
            # print("SET TOP", self.widget, value)
            self._top_constraint.constant = value


class TogaContainer(NSView):
    @objc_method
    def isFlipped(self) -> bool:
        # Default Cocoa coordinate frame is around the wrong way.
        return True

    @objc_method
    def display(self) -> None:
        self.layer.setNeedsDisplay_(True)
        self.layer.displayIfNeeded()


class Container:
    """ The Container is the top level representation of toga.Box.
    """
    def __init__(self):
        self.native = TogaContainer.alloc().init()
        self.native.setTranslatesAutoresizingMaskIntoConstraints_(False)

        self._content = None
        self.constraints = Constraints(self)

    @property
    def content(self):
        """ Content holds the top level widget of the container in form of
        a (:class: 'toga-cocoa.Widget`).

        Returns:
            Returns a `toga-cocoa.Widget', None if no content was set.
        """
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.container = self

    def update_layout(self, **style):
        if self.content:
            self.constraints.width = self.content.interface.layout.width
            self.constraints.height = self.content.interface.layout.height

            self.content.interface._update_layout(**style)
