from __future__ import print_function, absolute_import, division

from toga.constraint import Attribute, Constraint

from ..libs import *
from .base import Widget


class Container(Widget):

    _IDENTIFIER = {
        None: NSLayoutAttributeNotAnAttribute,
        Attribute.LEFT: NSLayoutAttributeLeft,
        Attribute.RIGHT: NSLayoutAttributeRight,
        Attribute.TOP: NSLayoutAttributeTop,
        Attribute.BOTTOM: NSLayoutAttributeBottom,
        Attribute.LEADING: NSLayoutAttributeLeading,
        Attribute.TRAILING: NSLayoutAttributeTrailing,
        Attribute.WIDTH: NSLayoutAttributeWidth,
        Attribute.HEIGHT: NSLayoutAttributeHeight,
        Attribute.CENTER_X: NSLayoutAttributeCenterX,
        Attribute.CENTER_Y: NSLayoutAttributeCenterY,
        # Attribute.BASELINE: NSLayoutAttributeBaseline,
    }

    _RELATION = {
        Constraint.LTE: NSLayoutRelationLessThanOrEqual,
        Constraint.EQUAL: NSLayoutRelationEqual,
        Constraint.GTE: NSLayoutRelationGreaterThanOrEqual,
    }

    def __init__(self):
        super(Container, self).__init__()
        self.children = []
        self.constraints = {}
        self._impl = None

    def _startup(self):
        self._impl = NSView.alloc().init()
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        for child in self.children:
            self._add(child)

        for constraint, impl in ((c, i) for c, i in self.constraints.items() if i is None):
            self._constrain(constraint)

    def add(self, widget):
        self.children.append(widget)
        if self._impl:
            self._add(widget)

    def _add(self, widget):
        # Assign the widget to the same app as the window.
        # This initiates startup logic.
        widget.app = self.app
        self._impl.addSubview_(widget._impl)

    def constrain(self, constraint):
        "Add the given constraint to the widget."
        if constraint in self.constraints:
            return

        if self._impl:
            self._constrain(constraint)

        else:
            self.constraints[constraint] = None

    def _constrain(self, constraint):
        widget = constraint.attr.widget._impl
        identifier = constraint.attr.identifier

        if constraint.related_attr:
            related_widget = constraint.related_attr.widget._impl
            related_identifier = constraint.related_attr.identifier

            multiplier = constraint.related_attr.multiplier / constraint.attr.multiplier
            constant = (constraint.related_attr.constant - constraint.attr.constant) / constraint.attr.multiplier

        else:
            related_widget = None
            related_identifier = None

            multiplier = constraint.attr.multiplier
            constant = constraint.attr.constant

        constraint._impl = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            widget, self._IDENTIFIER[identifier],
            self._RELATION[constraint.relation],
            related_widget, self._IDENTIFIER[related_identifier],
            multiplier, constant,
        )

        self._impl.addConstraint_(constraint._impl)
        self.constraints[constraint] = constraint._impl
