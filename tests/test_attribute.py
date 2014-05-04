from unittest import TestCase
if not hasattr(TestCase, 'assertIsNotNone'):
    # For Python2.6 compatibility
    from unittest2 import TestCase

from toga.constraint import Attribute, Constraint, InvalidConstraint


class AttributeTestCase(TestCase):
    def assertAttributeEqual(self, attr, multiplier, constant):
        self.assertEqual(attr.multiplier, multiplier)
        self.assertEqual(attr.constant, constant)

    def assertSimpleConstraintEqual(self, constraint, relation, multiplier, constant):
        self.assertEqual(constraint.relation, relation)
        self.assertAttributeEqual(constraint.attr, multiplier, constant)
        self.assertIsNone(constraint.related_attr)

    def assertRelatedConstraintEqual(self, constraint, relation, multiplier, constant, related_multiplier, related_constant):
        self.assertEqual(constraint.relation, relation)
        self.assertEqual(constraint.attr, multiplier, constant)
        self.assertEqual(constraint.related_attr, related_multiplier, related_constant)

    def test_add(self):
        "A constant can be added to an attribute"

        # A simple, empty attribute
        attr = Attribute(object(), Attribute.WIDTH)

        self.assertAttributeEqual(attr + 2, 1, 2)
        self.assertAttributeEqual(2 + attr, 1, 2)

        # A complex attribute
        attr = Attribute(object(), Attribute.WIDTH, 3, 7)

        self.assertAttributeEqual(attr + 2, 3, 9)
        self.assertAttributeEqual(2 + attr, 3, 9)

    def test_mult(self):
        "An attribute can be multiplied by a constant"

        # A simple, empty attribute
        attr = Attribute(object(), Attribute.WIDTH)

        self.assertAttributeEqual(attr * 2, 2, 0)
        self.assertAttributeEqual(2 * attr, 2, 0)

        # A complex attribute
        attr = Attribute(object(), Attribute.WIDTH, 3, 7)

        self.assertAttributeEqual(attr * 2, 6, 14)
        self.assertAttributeEqual(2 * attr, 6, 14)

    def test_div(self):
        "An attribute can be divided by a constant"

        # A simple, empty attribute
        attr = Attribute(object(), Attribute.WIDTH)

        self.assertAttributeEqual(attr / 2, 0.5, 0)

        # A complex attribute
        attr = Attribute(object(), Attribute.WIDTH, 3, 7)

        self.assertAttributeEqual(attr / 2, 1.5, 3.5)

    def test_sub(self):
        "A constant can be subtracted from an attribute"

        # A simple, empty attribute
        attr = Attribute(object(), Attribute.WIDTH)

        self.assertAttributeEqual(attr - 2, 1, -2)
        self.assertAttributeEqual(2 - attr, -1, 2)

        # A complex attribute
        attr = Attribute(object(), Attribute.WIDTH, 3, 5)

        self.assertAttributeEqual(attr - 2, 3, 3)
        self.assertAttributeEqual(2 - attr, -3, -3)

    def test_equality_constant(self):
        "When compared for equality with a constant, a single-attribute constraint is generated"

        self.assertSimpleConstraintEqual(
            Attribute(object(), Attribute.WIDTH) == 2,
            Constraint.EQUAL, 1, 2
        )

        self.assertSimpleConstraintEqual(
            3 * Attribute(object(), Attribute.WIDTH) + 7 == 9,
            Constraint.EQUAL, 3, 2
        )

        # Equality works both ways
        self.assertSimpleConstraintEqual(
            2 == Attribute(object(), Attribute.WIDTH),
            Constraint.EQUAL, 1, 2
        )

        self.assertSimpleConstraintEqual(
            9 == 3 * Attribute(object(), Attribute.WIDTH) + 7,
            Constraint.EQUAL, 3, 2
        )

    def test_less_than_constant(self):
        "When compared for less than or equal to a constant, a single-attribute constraint is generated"

        self.assertSimpleConstraintEqual(
            Attribute(object(), Attribute.WIDTH) <= 2,
            Constraint.LTE, 1, 2
        )

        self.assertSimpleConstraintEqual(
            3 * Attribute(object(), Attribute.WIDTH) + 7 <= 9,
            Constraint.LTE, 3, 2
        )

        # Operator works both ways
        self.assertSimpleConstraintEqual(
            2 >= Attribute(object(), Attribute.WIDTH),
            Constraint.LTE, 1, 2
        )

        self.assertSimpleConstraintEqual(
            9 >= 3 * Attribute(object(), Attribute.WIDTH) + 7,
            Constraint.LTE, 3, 2
        )

        # It's lazy, but the logic for < and <= are identical.
        self.assertSimpleConstraintEqual(
            3 * Attribute(object(), Attribute.WIDTH) + 7 < 9,
            Constraint.LTE, 3, 2
        )
        self.assertSimpleConstraintEqual(
            Attribute(object(), Attribute.WIDTH) < 2,
            Constraint.LTE, 1, 2
        )

    def test_greater_than_constant(self):
        "When compared for greater than or equal to a constant, a single-attribute constraint is generated"

        self.assertSimpleConstraintEqual(
            Attribute(object(), Attribute.WIDTH) >= 2,
            Constraint.GTE, 1, 2
        )

        self.assertSimpleConstraintEqual(
            3 * Attribute(object(), Attribute.WIDTH) + 7 >= 9,
            Constraint.GTE, 3, 2
        )

        # Operator works both ways
        self.assertSimpleConstraintEqual(
            2 <= Attribute(object(), Attribute.WIDTH),
            Constraint.GTE, 1, 2
        )

        self.assertSimpleConstraintEqual(
            9 <= 3 * Attribute(object(), Attribute.WIDTH) + 7,
            Constraint.GTE, 3, 2
        )

        # It's lazy, but the logic for > and >= are identical.
        self.assertSimpleConstraintEqual(
            3 * Attribute(object(), Attribute.WIDTH) + 7 > 9,
            Constraint.GTE, 3, 2
        )
        self.assertSimpleConstraintEqual(
            Attribute(object(), Attribute.WIDTH) > 2,
            Constraint.GTE, 1, 2
        )

    def test_equality_attribute(self):
        "When compared for equality with another attribute, a related constraint is generated"

        self.assertRelatedConstraintEqual(
            Attribute(object(), Attribute.WIDTH) == Attribute(object(), Attribute.WIDTH),
            Constraint.EQUAL, 1, 0, 1, 0
        )

        self.assertRelatedConstraintEqual(
            Attribute(object(), Attribute.WIDTH, 3, 7) == Attribute(object(), Attribute.WIDTH, 2, 5),
            Constraint.EQUAL, 3, 7, 2, 5
        )

    def test_less_than_attribute(self):
        "When compared for less than or equal to another attribute, a related constraint is generated"

        self.assertRelatedConstraintEqual(
            Attribute(object(), Attribute.WIDTH) <= Attribute(object(), Attribute.WIDTH),
            Constraint.LTE, 1, 0, 1, 0
        )

        self.assertRelatedConstraintEqual(
            Attribute(object(), Attribute.WIDTH, 3, 7) <= Attribute(object(), Attribute.WIDTH, 2, 5),
            Constraint.LTE, 3, 7, 2, 5
        )

        # It's lazy, but the logic for > and >= are identical.
        self.assertRelatedConstraintEqual(
            Attribute(object(), Attribute.WIDTH) < Attribute(object(), Attribute.WIDTH),
            Constraint.LTE, 1, 0, 1, 0
        )

        self.assertRelatedConstraintEqual(
            Attribute(object(), Attribute.WIDTH, 3, 7) < Attribute(object(), Attribute.WIDTH, 2, 5),
            Constraint.LTE, 3, 7, 2, 5
        )

    def test_greater_than_attribute(self):
        "When compared for greater than or equal to another attribute, a related constraint is generated"

        self.assertRelatedConstraintEqual(
            Attribute(object(), Attribute.WIDTH) >= Attribute(object(), Attribute.WIDTH),
            Constraint.GTE, 1, 0, 1, 0
        )

        self.assertRelatedConstraintEqual(
            Attribute(object(), Attribute.WIDTH, 3, 7) >= Attribute(object(), Attribute.WIDTH, 2, 5),
            Constraint.GTE, 3, 7, 2, 5
        )

        # It's lazy, but the logic for > and >= are identical.
        self.assertRelatedConstraintEqual(
            Attribute(object(), Attribute.WIDTH) > Attribute(object(), Attribute.WIDTH),
            Constraint.GTE, 1, 0, 1, 0
        )

        self.assertRelatedConstraintEqual(
            Attribute(object(), Attribute.WIDTH, 3, 7) > Attribute(object(), Attribute.WIDTH, 2, 5),
            Constraint.GTE, 3, 7, 2, 5
        )

    def test_invalid_comparisons(self):

        with self.assertRaises(InvalidConstraint):
            result = Attribute(object(), Attribute.WIDTH) == object()

        with self.assertRaises(InvalidConstraint):
            result = Attribute(object(), Attribute.WIDTH) > object()

        with self.assertRaises(InvalidConstraint):
            result = Attribute(object(), Attribute.WIDTH) >= object()

        with self.assertRaises(InvalidConstraint):
            result = Attribute(object(), Attribute.WIDTH) < object()

        with self.assertRaises(InvalidConstraint):
            result = Attribute(object(), Attribute.WIDTH) <= object()

        with self.assertRaises(InvalidConstraint):
            result = object() == Attribute(object(), Attribute.WIDTH)

        with self.assertRaises(InvalidConstraint):
            result = object() > Attribute(object(), Attribute.WIDTH)

        with self.assertRaises(InvalidConstraint):
            result = object() >= Attribute(object(), Attribute.WIDTH)

        with self.assertRaises(InvalidConstraint):
            result = object() < Attribute(object(), Attribute.WIDTH)

        with self.assertRaises(InvalidConstraint):
            result = object() <= Attribute(object(), Attribute.WIDTH)
