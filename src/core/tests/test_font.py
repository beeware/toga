import toga
from toga.fonts import SANS_SERIF, ITALIC, SMALL_CAPS, BOLD

import toga_dummy
from toga_dummy.utils import TestCase


class FontTests(TestCase):
    def setUp(self):
        super().setUp()

        self.family = SANS_SERIF
        self.size = 14
        self.style = ITALIC
        self.variant = SMALL_CAPS
        self.weight = BOLD

        self.font = toga.Font(
            family=self.family,
            size=self.size,
            style=self.style,
            variant=self.variant,
            weight=self.weight)

        # Bind the font to the dummy factory
        self.font.bind(toga_dummy.factory)

    def test_family(self):
        self.assertEqual(self.font.family, self.family)

    def test_size(self):
        self.assertEqual(self.font.size, self.size)

    def test_style(self):
        self.assertEqual(self.font.style, self.style)

    def test_variant(self):
        self.assertEqual(self.font.variant, self.variant)

    def test_weight(self):
        self.assertEqual(self.font.weight, self.weight)

    def test_measure(self):
        self.font.measure('measured text', tight=True)
        self.assertActionPerformedWith(self.font, 'measure', text='measured text', tight=True)
