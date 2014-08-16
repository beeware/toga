from __future__ import print_function, absolute_import, division


class Constraint(object):
    LTE = -1
    EQUAL = 0
    GTE = 1

    def __init__(self, attr, relation, related_attr=None):
        self.attr = attr
        self.relation = relation
        self.related_attr = related_attr

    def __unicode__(self):
        return u'%s %s %s' % (self.attr, self.relation, self.related_attr)


class Attribute(object):
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
    BASELINE = 11

    def __init__(self, widget, identifier, multiplier=1, constant=0):
        self.widget = widget
        self.identifier = identifier
        self.multiplier = float(multiplier)
        self.constant = float(constant)

    def __unicode__(self):
        return u'Attr %s: %s * %s + %s' % (self.identifier, self.multiplier, self.widget, self.constant)

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

    def __div__(self, value):
        return self.copy(
            multiplier=self.multiplier / value,
            constant=self.constant / value
        )

    def __radd__(self, value):
        return self.__add__(value)

    def __add__(self, value):
        return self.copy(
            constant=self.constant + value
        )

    def __rsub__(self, value):
        return self.copy(
            multiplier=-1,
            constant=self.constant - value
        )

    def __sub__(self, value):
        return self.copy(
            constant=self.constant - value
        )

    def __gt__(self, other):
        return self.__ge__(other)

    def __ge__(self, other):
        if isinstance(other, Attribute):
            return Constraint(self, Constraint.GTE, other)
        elif isinstance(other, (int, float)):
            return Constraint(self.copy(constant=other), Constraint.GTE)
        else:
            raise Exception('Bad constraint')

    def __lt__(self, other):
        return self.__le__(other)

    def __le__(self, other):
        if isinstance(other, Attribute):
            return Constraint(self, Constraint.LTE, other)
        elif isinstance(other, (int, float)):
            return Constraint(self.copy(constant=other), Constraint.LTE)
        else:
            raise Exception('Bad constraint')

    def __eq__(self, other):
        if isinstance(other, Attribute):
            return Constraint(self, Constraint.EQUAL, other)
        elif isinstance(other, (int, float)):
            return Constraint(self.copy(constant=other), Constraint.EQUAL)
        else:
            raise Exception('Bad constraint')
