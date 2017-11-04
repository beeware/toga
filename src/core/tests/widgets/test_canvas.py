import toga
import toga_dummy
from toga_dummy.utils import EventLog, TestCase


class CanvasTests(TestCase):
    def setUp(self):
        super().setUp()

        self.testing_canvas = toga.Canvas(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.testing_canvas._impl.interface, self.testing_canvas)
        self.assertActionPerformed(self.testing_canvas, 'create Canvas')
