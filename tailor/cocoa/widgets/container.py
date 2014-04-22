from tailor.cocoa.libs import *
from tailor.constraint import Attribute, Constraint
from tailor.cocoa.widgets.base import Widget


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
        self._impl = NSView.alloc().init()
        self.children = []
        self.constraints = {}

    def add(self, widget):
        self.children.append(widget)
        self._impl.addSubview_(widget._impl)

    def constrain(self, constraint):
        "Add the given constraint to the widget."
        if constraint in self.constraints:
            return

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
