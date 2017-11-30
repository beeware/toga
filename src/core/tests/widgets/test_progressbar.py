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

    def test_set_max(self):
        new_max = 100
        self.progress_bar.max = new_max
        self.assertEqual(self.progress_bar._max, new_max)
        self.assertValueSet(self.progress_bar, 'max', value=new_max)

    def test_set_max_illegal_type(self):
        with self.assertRaises(TypeError):
            self.progress_bar.value = "Brutus!"

    def test_set_value_not_none(self):
        new_value = self.progress_bar.max / 2

        self.progress_bar.value = new_value

        self.assertEqual(self.progress_bar.value, new_value)
        self.assertEqual(self.progress_bar._value, new_value)
        self.assertValueSet(self.progress_bar, 'value', value=new_value)

        self.assertEqual(self.progress_bar.running, False)

    def test_set_value_none(self):
        new_value = None

        self.progress_bar.value = new_value

        self.assertEqual(self.progress_bar.value, new_value)
        self.assertEqual(self.progress_bar._value, new_value)
        # in this case, _impl.set_value should NOT be called
        # self.assertValueSet(self.progress_bar, 'value', value=None)

        self.assertEqual(self.progress_bar.running, True)

    def test_set_value_negative(self):
        self.progress_bar.value = -2
        self.assertEqual(self.progress_bar.value, 0)
        self.assertEqual(self.progress_bar._value, 0)
        self.assertValueSet(self.progress_bar, 'value', value=0)

        self.assertEqual(self.progress_bar.running, False)

    def test_set_value_greater_than_max(self):
        self.progress_bar.value = self.progress_bar.max + 1

        self.assertEqual(self.progress_bar.value, self.progress_bar.max)
        self.assertEqual(self.progress_bar._value, self.progress_bar.max)
        self.assertValueSet(self.progress_bar, 'value', value=self.progress_bar.max)

        self.assertEqual(self.progress_bar.running, False)

    def test_set_value_illegal_type(self):
        with self.assertRaises(TypeError):
            self.progress_bar.value = "Tiberius!"
