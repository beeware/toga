from toga_dummy.utils import TestCase
from toga_winforms.widgets import button


def generator(interface, obj):
    for i in range(5):
        obj.val = i
        yield 1


class TestButton(TestCase):
    def setUp(self):
        super().setUp()
        self.button = button.Button

    def test_winforms_click(self):
        self.val = None
        button = self.button(None)
        button.set_on_press(generator)
        button.on_press()
        self.assertEqual(self.val, 4)
