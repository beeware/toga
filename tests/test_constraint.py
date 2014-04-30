from unittest import TestCase

from toga.widget import WidgetBase


class TestWidget(WidgetBase):
    def __init__(self, width=None, height=None):
        super(TestWidget, self).__init__()
        self.height_hints = height
        self.width_hints = width

    def __repr__(self):
        return u'<Widget:%s>' % id(self)


class TestContainer(TestWidget):
    def __init__(self):
        super(TestContainer, self).__init__()
        self.layout_manager = LayoutManager(self)
        self._children = []
        self._constraints = []

    def __repr__(self):
        return u'<Container:%s>' % id(self)

    def add(self, widget):
        self.layout_manager.reset()
        self._children.append(widget)

    def constrain(self, constraint):
        "Add the given constraint to the widget."
        self.layout_manager.reset()
        self._constraints.append(constraint)


class SimpleConstraintTestCase(TestCase):
    def assertValueEqual(self, value, vmin, vpref, vmax, fixed):
        self.assertEqual((value.vmin, value.vpref, value.vmax, value.fixed), (vmin, vpref, vmax, fixed))

    def setUp(self):
        self.obj1 = TestWidget()

        self.solvers = {
            self.obj1: Solver(),
        }

    def test_apply_equality_constant(self):
        "A single == constraint involving a constant can be applied to a solver list"

        constraint = self.obj1.LEFT == 10

        # Apply the constraint and check results
        self.assertTrue(constraint.apply(self.solvers))
        self.assertValueEqual(self.solvers[self.obj1].left, 10, 10, 10, True)

    def test_apply_gte_constant(self):
        "A single > constraint involving a constant can be applied to a solver list"

        constraint = self.obj1.LEFT > 10

        # Apply the constraint and check results
        self.assertTrue(constraint.apply(self.solvers))
        self.assertValueEqual(self.solvers[self.obj1].left, 10, 10, None, False)

    def test_apply_lte_constant(self):
        "A single < constraint involving a constant can be applied to a solver list"

        constraint = self.obj1.LEFT < 10

        # Apply the constraint and check results
        self.assertTrue(constraint.apply(self.solvers))
        self.assertValueEqual(self.solvers[self.obj1].left, None, 10, 10, False)

    def test_apply_equality_constant_reverse(self):
        "A single == constraint (specified in reverse) involving a constant can be applied to a solver list"

        constraint = 10 == self.obj1.LEFT

        # Apply the constraint and check results
        self.assertTrue(constraint.apply(self.solvers))
        self.assertValueEqual(self.solvers[self.obj1].left, 10, 10, 10, True)

    def test_apply_gte_constant_reverse(self):
        "A single > constraint (specified in reverse) involving a constant can be applied to a solver list"

        constraint = 10 < self.obj1.LEFT

        # Apply the constraint and check results
        self.assertTrue(constraint.apply(self.solvers))
        self.assertValueEqual(self.solvers[self.obj1].left, 10, 10, None, False)

    def test_apply_lte_constant_reverse(self):
        "A single < constraint (specified in reverse) involving a constant can be applied to a solver list"

        constraint = 10 > self.obj1.LEFT

        # Apply the constraint and check results
        self.assertTrue(constraint.apply(self.solvers))
        self.assertValueEqual(self.solvers[self.obj1].left, None, 10, 10, False)

    def test_apply_equality_constant_multiplier(self):
        "A single == constraint involving a constant and a multiplier can be applied to a solver list"

        constraint = (2 * self.obj1.LEFT == 10)

        # Apply the constraint and check results
        self.assertTrue(constraint.apply(self.solvers))
        self.assertValueEqual(self.solvers[self.obj1].left, 5, 5, 5, True)

    def test_apply_gte_constant_multiplier(self):
        "A single > constraint involving a constant and a multiplier can be applied to a solver list"

        constraint = 2 * self.obj1.LEFT > 10

        # Apply the constraint and check results
        self.assertTrue(constraint.apply(self.solvers))
        self.assertValueEqual(self.solvers[self.obj1].left, 5, 5, None, False)

    def test_apply_lte_constant_multiplier(self):
        "A single < constraint involving a constant and a multiplier can be applied to a solver list"

        constraint = 2 * self.obj1.LEFT < 10

        # Apply the constraint and check results
        self.assertTrue(constraint.apply(self.solvers))
        self.assertValueEqual(self.solvers[self.obj1].left, None, 5, 5, False)
