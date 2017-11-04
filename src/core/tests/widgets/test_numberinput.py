import toga
import toga_dummy
from toga_dummy.utils import TestCase


class NumberInputTests(TestCase):
    def setUp(self):
        super().setUp()

        self.nr_input = toga.NumberInput(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.nr_input._impl.interface, self.nr_input)
        self.assertActionPerformed(self.nr_input, 'create NumberInput')
