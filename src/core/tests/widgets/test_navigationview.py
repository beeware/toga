import unittest

import toga
from toga_dummy.utils import TestCase


class NavigationViewTests(TestCase):
    @unittest.skip("Not implemented!")
    def setUp(self):
        super().setUp()

        self.title = "Main View"
        self.content = toga.Box()
        self.navi_view = toga.NavigationView(
            self.title,
            self.content,
        )

    def test_widget_created(self):
        self.assertEqual(self.switch._impl.interface, self.switch)
        self.assertActionPerformed(self.switch, "create Switch")
