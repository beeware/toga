from toga_iOS.libs import (
    NSLayoutAttributeBottom,
    NSLayoutAttributeLeft,
    NSLayoutAttributeRight,
    NSLayoutAttributeTop,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
)


class Constraints:
    def __init__(self, widget):
        """
        A wrapper object storing the constraints required to position a widget
        at a precise location in its container.

        :param widget: The Widget implementation to be constrained.
        """
        self.widget = widget
        self._container = None

        self.width_constraint = None
        self.height_constraint = None

        self.left_constraint = None
        self.top_constraint = None

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, value):
        if value is None and self.container:
            # print("Remove constraints")
            self.container.native.removeConstraint(self.width_constraint)
            self.container.native.removeConstraint(self.height_constraint)
            self.container.native.removeConstraint(self.left_constraint)
            self.container.native.removeConstraint(self.top_constraint)
            self._container = value
        else:
            self._container = value
            # print("Add constraints for", self.widget, "in", self.container, self.widget.interface.layout)
            self.left_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # noqa: E501
                self.widget.native,
                NSLayoutAttributeLeft,
                NSLayoutRelationEqual,
                self.container.native,
                NSLayoutAttributeLeft,
                1.0,
                10,  # Use a dummy, non-zero value for now
            )
            self.container.native.addConstraint(self.left_constraint)

            self.top_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # noqa: E501
                self.widget.native,
                NSLayoutAttributeTop,
                NSLayoutRelationEqual,
                self.container.native,
                NSLayoutAttributeTop,
                1.0,
                5,  # Use a dummy, non-zero value for now
            )
            self.container.native.addConstraint(self.top_constraint)

            self.width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # noqa: E501
                self.widget.native,
                NSLayoutAttributeRight,
                NSLayoutRelationEqual,
                self.widget.native,
                NSLayoutAttributeLeft,
                1.0,
                50,  # Use a dummy, non-zero value for now
            )
            self.container.native.addConstraint(self.width_constraint)

            self.height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # noqa: E501
                self.widget.native,
                NSLayoutAttributeBottom,
                NSLayoutRelationEqual,
                self.widget.native,
                NSLayoutAttributeTop,
                1.0,
                30,  # Use a dummy, non-zero value for now
            )
            self.container.native.addConstraint(self.height_constraint)

    def update(self, x, y, width, height):
        if self.container:
            # print(f"UPDATE CONSTRAINTS {self.widget} {width}x{height}@{x},{y}")
            self.left_constraint.constant = x
            self.top_constraint.constant = y

            self.width_constraint.constant = width
            self.height_constraint.constant = height
