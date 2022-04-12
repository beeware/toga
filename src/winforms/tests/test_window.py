from toga_dummy.utils import TestCase
from toga_winforms import window


class TestWindow(TestCase):
    def setUp(self):
        super().setUp()
        self.window = window.Window

    def test_build_single_filter(self):
        test_filter = self.window.build_filter(None, ["txt"])
        self.assertEqual(
            test_filter,
            "txt files (*.txt)|*.txt"
            "|All files (*.*)|*.*",
        )

    def test_build_multiple_filter(self):
        test_filter = self.window.build_filter(None, ["txt", "doc"])
        self.assertEqual(
            test_filter,
            "All matching files (*.txt;*.doc)|*.txt;*.doc"
            "|txt files (*.txt)|*.txt"
            "|doc files (*.doc)|*.doc"
            "|All files (*.*)|*.*",
        )
