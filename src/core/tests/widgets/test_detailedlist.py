import unittest

import toga
import toga_dummy
from toga_dummy.utils import TestCase


class TestDetailedList(TestCase):
    @unittest.skip('Not implemented!')
    def setUp(self):
        super().setUp()

        self.text = 'test text'

        self.detailed_list = toga.DetailedList(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.detailed_list._impl.interface, self.detailed_list)
        self.assertActionPerformed(self.detailed_list, 'create Canvas')
