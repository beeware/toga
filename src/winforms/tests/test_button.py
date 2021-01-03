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
        self.button.on_press = generator
        button.on_press('widget', self)
        self.assertEqual(self.val, 4)
