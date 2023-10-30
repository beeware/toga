from .libs import (
    NSLayoutAttributeBottom,
    NSLayoutAttributeLeft,
    NSLayoutAttributeRight,
    NSLayoutAttributeTop,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
)


class Constraints:
    def __init__(self, widget):
        """A wrapper object storing the constraints required to position a widget at a
        precise location in its container.

        :param widget: The Widget implementation to be constrained.
        """
        self.widget = widget
        self.widget.native.translatesAutoresizingMaskIntoConstraints = False

        self._container = None
        self._container_native = None

        self.width_constraint = None
        self.height_constraint = None

        self.left_constraint = None
        self.top_constraint = None

    # Deletion isn't an event we can programmatically invoke; deletion
    # of constraints can take several iterations before it occurs.
    def __del__(self):  # pragma: nocover
        self._remove_constraints()

    def _remove_constraints(self):
        if self._container_native:
            # print(f"Remove constraints for {self.widget} in {self.container}")
            self._container_native.removeConstraint(self.width_constraint)
            self._container_native.removeConstraint(self.height_constraint)
            self._container_native.removeConstraint(self.left_constraint)
            self._container_native.removeConstraint(self.top_constraint)

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, value):
        # This will *always* remove and then add constraints. It relies on the base widget to
        # *not* invoke this setter unless the container is actually changing.

        self._remove_constraints()
        self._container = value
        if value is None:
            self._container_native = None
        else:
            self._container_native = value.native
            # print(f"Add constraints for {self.widget} in {self.container} {self.widget.interface.layout})
            self.left_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # noqa: E501
                self.widget.native,
                NSLayoutAttributeLeft,
                NSLayoutRelationEqual,
                self._container_native,
                NSLayoutAttributeLeft,
                1.0,
                10,  # Use a dummy, non-zero value for now
            )
            self._container_native.addConstraint(self.left_constraint)

            self.top_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # noqa: E501
                self.widget.native,
                NSLayoutAttributeTop,
                NSLayoutRelationEqual,
                self._container_native,
                NSLayoutAttributeTop,
                1.0,
                5,  # Use a dummy, non-zero value for now
            )
            self._container_native.addConstraint(self.top_constraint)

            self.width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # noqa: E501
                self.widget.native,
                NSLayoutAttributeRight,
                NSLayoutRelationEqual,
                self.widget.native,
                NSLayoutAttributeLeft,
                1.0,
                50,  # Use a dummy, non-zero value for now
            )
            self._container_native.addConstraint(self.width_constraint)

            self.height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # noqa: E501
                self.widget.native,
                NSLayoutAttributeBottom,
                NSLayoutRelationEqual,
                self.widget.native,
                NSLayoutAttributeTop,
                1.0,
                30,  # Use a dummy, non-zero value for now
            )
            self._container_native.addConstraint(self.height_constraint)

    def update(self, x, y, width, height):
        # print(f"UPDATE CONSTRAINTS {self.widget} in {self.container} {width}x{height}@{x},{y}")
        self.left_constraint.constant = x
        self.top_constraint.constant = y

        self.width_constraint.constant = width
        self.height_constraint.constant = height
