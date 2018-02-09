import toga
import toga_dummy
from toga.command import CommandSet
from toga_dummy.utils import TestCase


class TestWindow(TestCase):
    def setUp(self):
        super().setUp()
        self.window = toga.Window(factory=toga_dummy.factory)

    def test_widget_created(self):
        id = self.window.id
        self.assertIsNotNone(self.window.id)
        app = toga.App('test_name', 'id.app', factory=toga_dummy.factory)
        new_app = toga.App('error_name', 'id.error', factory=toga_dummy.factory)
        self.window.app = app
        with self.assertRaises(Exception):
            self.window.app = new_app

    def test_window_title(self):
        title = self.window.title
        self.assertEqual(title, 'Toga')

    def test_toolbar(self):
        toolbar = self.window.toolbar
        self.assertIsInstance(toolbar, CommandSet)

    def test_size_and_position_properties(self):
        size = (640, 480)
        self.assertEqual(size, self.window.size)
        position = (100, 100)
        self.assertEqual(position, self.window.position)

    def test_full_screen_set(self):
        self.assertEqual(self.window.full_screen, False)
