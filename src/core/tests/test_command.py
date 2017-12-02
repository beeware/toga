import unittest

import toga
import toga_dummy
from toga_dummy.utils import EventLog


class TestCommand(unittest.TestCase):
    def test_group_init_no_order(self):
        grp = toga.Group('label')
        self.assertEqual(grp.label, 'label')
        self.assertEqual(grp.order, 0)
    
    def test_group_init_with_order(self):
        grp = toga.Group('label', 2)
        self.assertEqual(grp.label, 'label')
        self.assertEqual(grp.order, 2)
    
    def test_group_lt(self):
        grp1, grp2 = toga.Group('A'), toga.Group('B')
        self.assertTrue(toga.Group('A', 1) < toga.Group('A', 2))
        self.assertTrue(toga.Group('A') < toga.Group('B'))
    
    def test_group_eq(self):
        self.assertEqual(toga.Group('A'), toga.Group('A'))
        self.assertEqual(toga.Group('A', 1), toga.Group('A', 1))
        self.assertNotEqual(toga.Group('A'), toga.Group('B'))
        self.assertNotEqual(toga.Group('A', 1), toga.Group('A', 2))
        self.assertNotEqual(toga.Group('A', 1), toga.Group('B', 1))
