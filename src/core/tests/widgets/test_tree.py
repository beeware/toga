import toga
import toga_dummy
from toga_dummy.utils import TestCase


class TreeTests(TestCase):
    def setUp(self):
        super().setUp()

        self.heading = ['Heading {}'.format(x) for x in range(3)]
        self.tree = toga.Tree(headings=self.heading,
                              factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.tree._impl.interface, self.tree)
        self.assertActionPerformed(self.tree, 'create Tree')
