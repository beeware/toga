from toga_dummy.utils import TestCase
import toga_dummy
import toga

class TestWindow(TestCase):
    def setUp(self):
        super().setUp()
        self.window = toga.Window(factory=toga_dummy.factory)

    def test_build_filter(self):
        test_filter = self.window.build_filter(["txt"])
        self.assertEqual(test_filter, "txt files (*.txt)|*.txt|All files (*.*)|*.*")
