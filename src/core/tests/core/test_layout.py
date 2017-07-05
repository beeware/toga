import unittest
import toga

class TestCoreLayout(unittest.TestCase):
    def setUp(self):
        self.widget = toga.Widget()
        self.layout = toga.Layout(self.widget)

    def test_instantiation(self):
        self.assertEqual(self.layout.node, self.widget)

    def test_layout__repr__with_node(self):
        self.layout.width = 10
        self.layout.height = 20
        self.layout.left = 30
        self.layout.top = 40
        self.assertEqual(self.layout.__repr__(), '<Layout (dirty) (10x20 @ 30,40)>')

    def test_layout__repr__with_node_None(self):
        layout = toga.Layout(None)
        self.assertEqual(layout.__repr__(), '<Layout (dirty) (NonexNone @ 0,0)>')

    def test_layout__eql__(self):
        self.assertTrue(self.layout == self.layout)

    def test_layout_rest(self):
        self.layout.width = 100
        self.layout.height = 100
        self.layout.top = 100
        self.layout.left = 100
        self.assertEqual(self.layout.width, 100)
        self.assertEqual(self.layout.height, 100)
        self.assertEqual(self.layout.top, 100)
        self.assertEqual(self.layout.left, 100)
        self.layout.reset()
        self.assertEqual(self.layout.width, None)
        self.assertEqual(self.layout.height, None)
        self.assertEqual(self.layout.top, 0)
        self.assertEqual(self.layout.left, 0)

    def test_layout_dirty(self):
        self.layout.dirty = True
        self.assertTrue(self.layout.dirty)
        self.layout.dirty = False
        self.assertFalse(self.layout.dirty)
        self.layout.dirty = None
        self.assertIsNone(self.layout.dirty)

    def test_layout_right(self):
        self.layout.left = 50
        self.layout.width = 50
        self.assertEqual(self.layout.right, 100)

    def test_layout_bottom(self):
        self.layout.top = 50
        self.layout.height = 50
        self.assertEqual(self.layout.bottom, 100)

    def test_layout_absolute(self):
        pass

    def test_layout_origin(self):
        origin = self.layout.origin
        self.assertEqual(origin.top, 0)
        self.assertEqual(origin.left, 0)
