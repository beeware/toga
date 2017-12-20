import toga
from toga.font import SANS_SERIF, measure_text

import toga_dummy
from toga_dummy.utils import TestCase


class FontTests(TestCase):
    def setUp(self):
        super().setUp()

        self.family = SANS_SERIF
        self.size = 14

        self.font = toga.Font(
            self.family,
            self.size,
        )

    def test_family(self):
      self.assertEqual(self.font.family, self.family)

    def test_size(self):
      self.assertEqual(self.font.size, self.size)

    def test_measure(self):
        measure_text(self.font, 'measured text', tight=True, factory=toga_dummy.factory)
        self.assertFunctionPerformedWith('font', 'measure_text', text='measured text', tight=True)
