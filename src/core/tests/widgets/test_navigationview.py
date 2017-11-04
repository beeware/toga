import unittest

import toga
import toga_dummy
from toga_dummy.utils import TestCase


class NavigationViewTests(TestCase):
    @unittest.skip("Not implemented!")
    def setUp(self):
        super().setUp()

        self.title = 'Main View'
        self.content = toga.Box(factory=toga_dummy.factory)
        self.navi_view = toga.NavigationView(self.title,
                                             self.content,
                                             factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.switch._impl.interface, self.switch)
        self.assertActionPerformed(self.switch, 'create Switch')
