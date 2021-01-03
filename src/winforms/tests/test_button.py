import toga
import unittest


class TestButton(unittest.TestCase):
    def setUp(self):
        self.val = None

        def generator(self, widget):
            for i in range(5):
                self.val = i
                yield 1
        self.button = toga.Button(label="Run", on_press=generator)

    def test_winforms_click(self):
        self.button.on_press()
        self.assertEqual(self.val, 4)
