import toga
import toga_dummy
from toga_dummy.utils import TestCase


class ProgressBarTests(TestCase):
    def setUp(self):
        super().setUp()

        self.progress_bar = toga.ProgressBar(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.progress_bar._impl.interface, self.progress_bar)
        self.assertActionPerformed(self.progress_bar, 'create ProgressBar')

    def test_set_value(self):
        self.progress_bar.value = 10
        self.assertEqual(self.progress_bar.value, 10)
        self.assertEqual(self.progress_bar._value, 10)
        self.assertValueSet(self.progress_bar, 'value', value=10)

    def test_set_max(self):
        new_max = 100
        self.progress_bar.max = new_max
        self.assertEqual(self.progress_bar._max, new_max)
        self.assertValueSet(self.progress_bar, 'max', value=new_max)
