import toga
from toga_dummy.utils import TestCase


class BoxTests(TestCase):
    def setUp(self):
        super().setUp()
        self.children = [toga.Widget()]
        self.box = toga.Box(children=self.children)

    def test_widget_created(self):
        self.assertEqual(self.box._impl.interface, self.box)
        self.assertActionPerformed(self.box, "create Box")

    def test_children_added(self):
        self.assertEqual(self.box._children, self.children)
