import toga
import toga_dummy
from toga_dummy.utils import TestCase


# ### ProgressBar truth table
#
# | max     | running   | Behavior                |
# |---------|-----------|-------------------------|
# | None    | False     | disabled                |
# | None    | True      | indeterminate anim.     |
# | number  | False     | show percentage         |
# | number  | True      | show %, working anim.   |
#
# Note: if ``value`` is None, the widget will render as if the value were zero.


class ProgressBarTests(TestCase):
    def setUp(self):
        super().setUp()

        self.progress_bar = toga.ProgressBar(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.progress_bar._impl.interface, self.progress_bar)
        self.assertActionPerformed(self.progress_bar, 'create ProgressBar')

    def test_set_max_to_number(self):
        new_max = 100
        self.progress_bar.max = new_max
        self.assertEqual(self.progress_bar.max, new_max)
        self.assertValueSet(self.progress_bar, 'max', value=new_max)
        self.assertTrue(self.progress_bar.is_determinate)

    def test_set_max_to_none(self):
        self.progress_bar.max = None
        self.assertEqual(self.progress_bar._max, None)
        self.assertValueSet(self.progress_bar, 'max', value=None)
        self.assertFalse(self.progress_bar.is_determinate)

    def test_start(self):
        # Start the progress bar
        self.progress_bar.start()
        self.assertEqual(self.progress_bar.is_running, True)
        self.assertActionPerformed(self.progress_bar, 'start')

        # Forget that `start` was performed so it can be checked again
        del self.progress_bar._impl._actions['start']

        # Already started, no action performed
        with self.assertRaises(AssertionError):
            self.progress_bar.start()
            self.assertActionPerformed(self.progress_bar, 'start')

    def test_stop(self):
        # Start the progress bar
        self.progress_bar.start()
        self.assertEqual(self.progress_bar.is_running, True)
        self.assertActionPerformed(self.progress_bar, 'start')

        self.progress_bar.stop()
        self.assertEqual(self.progress_bar.is_running, False)
        self.assertActionPerformed(self.progress_bar, 'stop')

        # Forget that `stop` was performed so it can be checked again
        del self.progress_bar._impl._actions['stop']

        # Already started, no action performed
        with self.assertRaises(AssertionError):
            self.progress_bar.stop()
            self.assertActionPerformed(self.progress_bar, 'stop')

    def test_set_value_to_number_less_than_max(self):
        new_value = self.progress_bar.max / 2
        self.progress_bar.value = new_value
        self.assertEqual(self.progress_bar.value, new_value)
        self.assertValueSet(self.progress_bar, 'value', value=new_value)

    def test_set_value_to_number_greater_than_max(self):
        new_value = self.progress_bar.max + 1
        self.progress_bar.value = new_value
        self.assertEqual(self.progress_bar.value, self.progress_bar.max)
        self.assertValueSet(self.progress_bar, 'value', value=new_value)

    def test_set_value_to_none(self):
        self.progress_bar.value = None
        self.assertEqual(self.progress_bar.value, 0)  # 0 is clean value for None
        self.assertValueSet(self.progress_bar, 'value', value=None)

    def test_disabled_cases(self):
        # Start with a default progress bar
        self.progress_bar = toga.ProgressBar(factory=toga_dummy.factory)
        self.assertTrue(self.progress_bar.enabled)

        # It should be disabled if it is stopped and max is None

        self.progress_bar.max = None
        self.progress_bar.stop()
        self.progress_bar.value = 0
        self.assertFalse(self.progress_bar.enabled)

        # Starting the progress bar should enable it again

        # self.progress_bar.max = None
        self.progress_bar.start()
        # self.progress_bar.value = 0
        self.assertTrue(self.progress_bar.enabled)

        # Stopping AND providing a max will cause it to display the percentage.

        self.progress_bar.max = 1
        self.progress_bar.stop()
        # self.progress_bar.value = 0
        self.assertTrue(self.progress_bar.enabled)

    def test_already_running(self):
        # Creating a new progress bar with running=True so it is already running
        self.progress_bar = toga.ProgressBar(factory=toga_dummy.factory, running=True)

        # Asserting that start() function is invoked on the underlying widget
        self.assertActionPerformed(self.progress_bar, 'start')

        # The constructor which is __init__ function will call the function start if running=True
        # which will make enabled=True

        # Asserting is_running to be True
        self.assertTrue(self.progress_bar.is_running)

        # Asserting enabled to be True
        self.assertTrue(self.progress_bar.enabled)
