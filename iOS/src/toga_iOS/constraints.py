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
        """A wrapper object storing the constraints required to position a widget at a
        precise location in its container.

        :param widget: The Widget implementation to be constrained.
        """
        self.widget = widget
        self.widget.native.translatesAutoresizingMaskIntoConstraints = False

        self._container = None

        self.width_constraint = None
        self.height_constraint = None

        self.left_constraint = None
        self.top_constraint = None

    # Deletion isn't an event we can programmatically invoke; deletion
    # of constraints can take several iterations before it occurs.
    def __del__(self):  # pragma: nocover
        self._remove_constraints()

    def _remove_constraints(self):
        if self.container:
            # print(f"Remove constraints for {self.widget} in {self.container}")
            self.container.native.removeConstraint(self.width_constraint)
            self.container.native.removeConstraint(self.height_constraint)
            self.container.native.removeConstraint(self.left_constraint)
            self.container.native.removeConstraint(self.top_constraint)

            self.width_constraint.release()
            self.height_constraint.release()
            self.left_constraint.release()
            self.top_constraint.release()

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, value):
        # This will *always* remove and then add constraints. It relies on the base widget to
        # *not* invoke this setter unless the container is actually changing.

        self._remove_constraints()
        self._container = value
        if value is not None:
            # print(f"Add constraints for {self.widget} in {self.container} {self.widget.interface.layout}")
            self.left_constraint = NSLayoutConstraint.constraintWithItem(
                self.widget.native,
                attribute__1=NSLayoutAttributeLeft,
                relatedBy=NSLayoutRelationEqual,
                toItem=self.container.native,
                attribute__2=NSLayoutAttributeLeft,
                multiplier=1.0,
                constant=10,  # Use a dummy, non-zero value for now
            ).retain()
            self.container.native.addConstraint(self.left_constraint)

            self.top_constraint = NSLayoutConstraint.constraintWithItem(
                self.widget.native,
                attribute__1=NSLayoutAttributeTop,
                relatedBy=NSLayoutRelationEqual,
                toItem=self.container.native,
                attribute__2=NSLayoutAttributeTop,
                multiplier=1.0,
                constant=5,  # Use a dummy, non-zero value for now
            ).retain()
            self.container.native.addConstraint(self.top_constraint)

            self.width_constraint = NSLayoutConstraint.constraintWithItem(
                self.widget.native,
                attribute__1=NSLayoutAttributeRight,
                relatedBy=NSLayoutRelationEqual,
                toItem=self.widget.native,
                attribute__2=NSLayoutAttributeLeft,
                multiplier=1.0,
                constant=50,  # Use a dummy, non-zero value for now
            ).retain()
            self.container.native.addConstraint(self.width_constraint)

            self.height_constraint = NSLayoutConstraint.constraintWithItem(
                self.widget.native,
                attribute__1=NSLayoutAttributeBottom,
                relatedBy=NSLayoutRelationEqual,
                toItem=self.widget.native,
                attribute__2=NSLayoutAttributeTop,
                multiplier=1.0,
                constant=30,  # Use a dummy, non-zero value for now
            ).retain()
            self.container.native.addConstraint(self.height_constraint)

    def update(self, x, y, width, height):
        # print(f"UPDATE CONSTRAINTS {self.widget} in {self.container} {width}x{height}@{x},{y}")
        self.left_constraint.constant = x
        self.top_constraint.constant = y

        self.width_constraint.constant = width
        self.height_constraint.constant = height
