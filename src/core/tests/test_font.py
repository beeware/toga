import toga
import toga_dummy
from toga_dummy.utils import TestCase


class FontTests(TestCase):
    def setUp(self):
        super().setUp()

        self.family = "sans-serif"
        self.size = 14

        self.font = toga.Font(
            self.family,
            self.size,
            factory=toga_dummy.factory
        )

    def test_family(self):
      self.assertEqual(self.font.family, self.family)

    def test_size(self):
      self.assertEqual(self.font.size, self.size)

    def test_measure(self):
        self.font.measure('measured text', True)
        self.assertActionPerformedWith(self.font, 'measure', text='measured text', tight=True)
