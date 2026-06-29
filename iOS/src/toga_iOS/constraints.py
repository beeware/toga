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

        self.constraints_created = False

    # Deletion isn't an event we can programmatically invoke; deletion
    # of constraints can take several iterations before it occurs.
    def __del__(self):  # pragma: nocover
        self._remove_constraints()

    def _remove_constraints(self):
        if self.container:
            # print(f"Remove constraints for {self.widget} in {self.container}")
            # Due to the unpredictability of garbage collection, it's possible for
            # the native object of the window's container to be deleted on the ObjC
            # side before the constraints for the window have been removed. Protect
            # against this possibility.
            # Also protect against the possibility that the constraints have
            # already been cleared.
            if self.container.native and self.constraints_created:
                self.container.native.removeConstraint(self.width_constraint)
                self.container.native.removeConstraint(self.height_constraint)
                self.container.native.removeConstraint(self.left_constraint)
                self.container.native.removeConstraint(self.top_constraint)

                self.constraints_created = False

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, value):
        # This will invalidate our created constraints, as the container would've
        # changed.  Constraints are not created until the actual first layout
        # update, as we do not want the native layer performing any layout passes
        # with wrong initial dummy constrained values.
        self._remove_constraints()
        self._container = value

    def update(self, x, y, width, height):
        # print(
        #     f"UPDATE CONSTRAINTS {self.widget} in {self.container} "
        #     f"{width}x{height}@{x},{y}"
        # )
        y += self.container.top_inset
        x += self.container.left_inset

        if self.constraints_created:
            # We already have constraints set up; reuse them.
            self.left_constraint.constant = x
            self.top_constraint.constant = y

            self.width_constraint.constant = width
            self.height_constraint.constant = height

        else:
            self.left_constraint = NSLayoutConstraint.constraintWithItem(
                self.widget.native,
                attribute__1=NSLayoutAttributeLeft,
                relatedBy=NSLayoutRelationEqual,
                toItem=self.container.native,
                attribute__2=NSLayoutAttributeLeft,
                multiplier=1.0,
                constant=x,
            )
            self.container.native.addConstraint(self.left_constraint)

            self.top_constraint = NSLayoutConstraint.constraintWithItem(
                self.widget.native,
                attribute__1=NSLayoutAttributeTop,
                relatedBy=NSLayoutRelationEqual,
                toItem=self.container.native,
                attribute__2=NSLayoutAttributeTop,
                multiplier=1.0,
                constant=y,
            )
            self.container.native.addConstraint(self.top_constraint)

            self.width_constraint = NSLayoutConstraint.constraintWithItem(
                self.widget.native,
                attribute__1=NSLayoutAttributeRight,
                relatedBy=NSLayoutRelationEqual,
                toItem=self.widget.native,
                attribute__2=NSLayoutAttributeLeft,
                multiplier=1.0,
                constant=width,
            )
            self.container.native.addConstraint(self.width_constraint)

            self.height_constraint = NSLayoutConstraint.constraintWithItem(
                self.widget.native,
                attribute__1=NSLayoutAttributeBottom,
                relatedBy=NSLayoutRelationEqual,
                toItem=self.widget.native,
                attribute__2=NSLayoutAttributeTop,
                multiplier=1.0,
                constant=height,
            )
            self.container.native.addConstraint(self.height_constraint)

            self.constraints_created = True
