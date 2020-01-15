import toga
import toga_dummy
from toga_dummy.utils import TestCase


class DividerTests(TestCase):
    def setUp(self):
        super().setUp()
        self.divider = toga.Divider(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.divider._impl.interface, self.divider)
        self.assertActionPerformed(self.divider, 'create Divider')

    def test_update_direction(self):
        new_direction = toga.Divider.HORIZONTAL
        self.divider.direction = new_direction
        self.assertEqual(self.divider.direction, new_direction)
        self.assertValueSet(self.divider, 'direction', new_direction)
        self.assertActionPerformed(self.divider, 'rehint Divider')
