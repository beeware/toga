import unittest
import toga


class TestCorePoint(unittest.TestCase):
    def setUp(self):
        self.top = 50
        self.left = 100
        self.point = toga.Point(self.top, self.left)

    def test_point__repr__(self):
        self.assertEqual(self.point.__repr__(), '<Point (100,50)>')

    def test_point_left(self):
        self.assertEqual(self.point.left, 100)

    def test_point_top(self):
        self.assertEqual(self.point.top, 50)
