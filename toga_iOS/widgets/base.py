from ..libs import (
    NSLayoutAttributeTop, NSLayoutAttributeLeft,
    NSLayoutAttributeRight, NSLayoutAttributeBottom,
    NSLayoutRelationEqual,
    NSLayoutConstraint,
    NSRect, NSPoint, NSSize
)


class Constraints:
    def __init__(self, view):
        self._view = view
        self._container = None

        self._width_constraint = None
        self._height_constraint = None

        self._left_constraint = None
        self._top_constraint = None

    @property
    def view(self):
        return self._view

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, value):
        self._container = value
        # print("Add constraints for", self._view, 'in', self._container)
        self._width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._view._impl, NSLayoutAttributeRight,
            NSLayoutRelationEqual,
            self._view._impl, NSLayoutAttributeLeft,
            1.0, self._view.style.layout.width
        )
        self._container._impl.addConstraint_(self._width_constraint)

        self._height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._view._impl, NSLayoutAttributeBottom,
            NSLayoutRelationEqual,
            self._view._impl, NSLayoutAttributeTop,
            1.0, self._view.style.layout.height
        )
        self._container._impl.addConstraint_(self._height_constraint)

        self._left_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._view._impl, NSLayoutAttributeLeft,
            NSLayoutRelationEqual,
            self._container._impl, NSLayoutAttributeLeft,
            1.0, self._view.style.layout.left
        )
        self._container._impl.addConstraint_(self._left_constraint)

        self._top_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self._view._impl, NSLayoutAttributeTop,
            NSLayoutRelationEqual,
            self._container._impl, NSLayoutAttributeTop,
            1.0, self._view.style.layout.top
        )
        self._container._impl.addConstraint_(self._top_constraint)

    def update(self):
        if self._container:
            # print("UPDATE", self._view, 'in', self._container, 'to', self._view.style.layout)
            self.width = self._view.style.layout.width
            self.height = self._view.style.layout.height
            self.top = self._view.style.layout.top
            self.left = self._view.style.layout.left
        else:
            # If the widget doesn't have a container, it is a top level widget.
            # Set the frame instead of the constraints.
            # print("SET FRAME", self._view, 'to', self._view.style.layout)
            frame = NSRect(
                NSPoint(self._view.style.layout.left, self._view.style.layout.top),
                NSSize(self._view.style.layout.width, self._view.style.layout.height)
            )
            self._view._impl.setFrame_(frame)

    @property
    def width(self):
        if self._width_constraint:
            return self._width_constraint.constant

    @width.setter
    def width(self, value):
        if self._width_constraint:
            # print("SET WIDTH", self._view, value)
            self._width_constraint.constant = value

    @property
    def height(self):
        if self._height_constraint:
            return self._height_constraint.constant

    @height.setter
    def height(self, value):
        if self._height_constraint:
            # print("SET HEIGHT", self._view, value)
            self._height_constraint.constant = value

    @property
    def left(self):
        if self._left_constraint:
            return self._left_constraint.constant

    @left.setter
    def left(self, value):
        if self._left_constraint:
            # print("SET LEFT", self._view, value)
            self._left_constraint.constant = value

    @property
    def top(self):
        if self._top_constraint:
            return self._top_constraint.constant

    @top.setter
    def top(self, value):
        if self._top_constraint:
            # print("SET TOP", self._view, value)
            self._top_constraint.constant = value


class WidgetMixin:
    def _set_app(self, app):
        pass

    def _set_window(self, window):
        pass

    def _add_child(self, child):
        self._impl.addSubview_(child._impl)
        child._constraints.container = self

    def _add_constraints(self):
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._constraints = Constraints(self)

    def _apply_layout(self):
        # print("SET WIDGET FRAME", self, self.style.layout)
        self._constraints.update()
