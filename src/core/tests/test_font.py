import unittest
from unittest.mock import Mock, MagicMock, patch
import toga
import toga_dummy


class TestFont(unittest.TestCase):
    def setUp(self):
        self.family = "sans-serif"
        self.size = 14

        self.font = toga.Font(
            self.family,
            self.size
        )

    def test_family(self):
      self.assertEqual(self.font.family, self.family)

    def test_size(self):
      self.assertEqual(self.font.size, self.size)
