import toga
import toga_dummy
from toga_dummy.utils import TestCase


class ActivityIndicatorTests(TestCase):
    def setUp(self):
        super().setUp()
        self.acivityindicator = toga.ActivityIndicator(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.acivityindicator._impl.interface, self.acivityindicator)
        self.assertActionPerformed(self.acivityindicator, 'create AcivityIndicator')

    def test_start(self):
        # Start spinning
        self.acivityindicator.start()
        self.assertEqual(self.acivityindicator.is_running, True)
        self.assertActionPerformed(self.acivityindicator, 'start')

        # Forget that `start` was performed so it can be checked again
        del self.acivityindicator._impl._actions['start']

        # Already started, no action performed
        with self.assertRaises(AssertionError):
            self.acivityindicator.start()
            self.assertActionPerformed(self.acivityindicator, 'start')

    def test_stop(self):
        # Stop spinning
        self.acivityindicator.start()
        self.assertEqual(self.acivityindicator.is_running, True)
        self.assertActionPerformed(self.acivityindicator, 'start')

        self.acivityindicator.stop()
        self.assertEqual(self.acivityindicator.is_running, False)
        self.assertActionPerformed(self.acivityindicator, 'stop')

        # Forget that `stop` was performed so it can be checked again
        del self.acivityindicator._impl._actions['stop']

        # Already started, no action performed
        with self.assertRaises(AssertionError):
            self.acivityindicator.stop()
            self.assertActionPerformed(self.acivityindicator, 'stop')
