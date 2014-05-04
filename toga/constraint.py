from __future__ import print_function, absolute_import, division


class InvalidConstraint(Exception):
    "Raised when a constraint cannot be satisfied"
    pass


class Constraint(object):
    """A formal description of a relationship between 2 attributes, or 1 attribute and a constant.
    """
    LTE = -1
    EQUAL = 0
    GTE = 1

    def __init__(self, attr, relation, related_attr=None):
        self.attr = attr
        self.relation = relation
        self.related_attr = related_attr

    @property
    def relation_label(self):
        return {
            Constraint.LTE: '<=',
            Constraint.EQUAL: '==',
            Constraint.GTE: '>=',
        }[self.relation]

    def __repr__(self):
        if self.related_attr is not None:
            return '<Constraint: %s%s.%s%s %s %s%s.%s%s>' % (
                '%s * ' % self.attr.multiplier if self.attr.multiplier != 1 else '',
                self.attr.widget, self.attr.identifier_label,
                ' + %s' % self.attr.constant if self.attr.constant else '',
                self.relation_label,
                '%s * ' % self.related_attr.multiplier if self.related_attr.multiplier != 1 else '',
                self.related_attr.widget, self.related_attr.identifier_label,
                ' + %s' % self.related_attr.constant if self.related_attr.constant else '',
            )
        else:
            return '<Constraint: %s%s.%s %s %s>' % (
                '%s * ' % self.attr.multiplier if self.attr.multiplier != 1 else '',
                self.attr.widget, self.attr.identifier_label, self.relation_label, self.attr.constant,
            )


class Attribute(object):
    """A representation of an attribute of a rendered widget.

    If two attributes are compared using ==, <= or >=, a constraint enforcing the
    queried relationship is created. A constraint will also be created if an attribute
    is compared with a constant.

    Attributes can be combined mathematically with constants (through multiplication
    and addition). These constants are stored on the attribute, and form the basis
    for the aX + b = cY + d constants used to construct constraints.
    """
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4
    LEADING = 5
    TRAILING = 6
    WIDTH = 7
    HEIGHT = 8
    CENTER_X = 9
    CENTER_Y = 10
    # BASELINE = 11

    def __init__(self, widget, identifier, multiplier=1, constant=0):
        self.widget = widget
        self.identifier = identifier
        self.multiplier = float(multiplier)
        self.constant = float(constant)

    @property
    def identifier_label(self):
        return {
            Attribute.LEFT: "LEFT",
            Attribute.RIGHT: "RIGHT",
            Attribute.TOP: "TOP",
            Attribute.BOTTOM: "BOTTOM",
            Attribute.LEADING: "LEADING",
            Attribute.TRAILING: "TRAILING",
            Attribute.WIDTH: "WIDTH",
            Attribute.HEIGHT: "HEIGHT",
            Attribute.CENTER_X: "CENTER_X",
            Attribute.CENTER_Y: "CENTER_Y",
            # Attribute.BASELINE: "BASELINE",
        }[self.identifier]

    def __repr__(self):
        return '<Attr %s * %s.%s + %s>' % (self.multiplier, self.widget, self.identifier_label, self.constant)

    def copy(self, multiplier=None, constant=None):
        attr = Attribute(self.widget, self.identifier)
        if multiplier is not None:
            attr.multiplier = multiplier
        if constant is not None:
            attr.constant = constant
        return attr

    def __rmul__(self, value):
        return self.__mul__(value)

    def __mul__(self, value):
        return self.copy(
            multiplier=self.multiplier * value,
            constant=self.constant * value
        )

    def __truediv__(self, value):
        return self.__div__(value)

    def __div__(self, value):
        return self.copy(
            multiplier=self.multiplier / value,
            constant=self.constant / value
        )

    def __radd__(self, value):
        return self.__add__(value)

    def __add__(self, value):
        return self.copy(
            multiplier=self.multiplier,
            constant=self.constant + value
        )

    def __rsub__(self, value):
        return self.copy(
            multiplier=-self.multiplier,
            constant=value - self.constant
        )

    def __sub__(self, value):
        return self.copy(
            multiplier=self.multiplier,
            constant=self.constant - value
        )

    def __gt__(self, other):
        return self.__ge__(other)

    def __ge__(self, other):
        if isinstance(other, Attribute):
            return Constraint(self, Constraint.GTE, other)
        elif isinstance(other, (int, float)):
            return Constraint(self.copy(multiplier=self.multiplier, constant=(other - self.constant)), Constraint.GTE)
        else:
            raise InvalidConstraint('Cannot build a constraint with an object of type %s' % type(other))

    def __lt__(self, other):
        return self.__le__(other)

    def __le__(self, other):
        if isinstance(other, Attribute):
            return Constraint(self, Constraint.LTE, other)
        elif isinstance(other, (int, float)):
            return Constraint(self.copy(multiplier=self.multiplier, constant=(other - self.constant)), Constraint.LTE)
        else:
            raise InvalidConstraint('Cannot build a constraint with an object of type %s' % type(other))

    __hash__ = object.__hash__

    def __eq__(self, other):
        if isinstance(other, Attribute):
            return Constraint(self, Constraint.EQUAL, other)
        elif isinstance(other, (int, float)):
            return Constraint(self.copy(multiplier=self.multiplier, constant=(other - self.constant)), Constraint.EQUAL)
        else:
            raise InvalidConstraint('Cannot build a constraint with an object of type %s' % type(other))

