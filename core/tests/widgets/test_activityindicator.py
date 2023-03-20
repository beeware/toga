import toga
from toga_dummy.utils import EventLog, TestCase


class ActivityIndicatorTests(TestCase):
    def setUp(self):
        super().setUp()
        self.activityindicator = toga.ActivityIndicator()

    def test_widget_created(self):
        self.assertEqual(self.activityindicator._impl.interface, self.activityindicator)
        self.assertActionPerformed(self.activityindicator, "create ActivityIndicator")

    def test_start(self):
        # Start spinning
        self.activityindicator.start()
        self.assertEqual(self.activityindicator.is_running, True)
        self.assertActionPerformed(self.activityindicator, "start ActivityIndicator")

        # Forget that `start` was performed so it can be checked again
        EventLog.reset()

        # Already started, no action performed
        self.activityindicator.start()
        self.assertActionNotPerformed(self.activityindicator, "start ActivityIndicator")

    def test_stop(self):
        # Start spinning
        self.activityindicator.start()

        # Stop spinning
        self.activityindicator.stop()
        self.assertEqual(self.activityindicator.is_running, False)
        self.assertActionPerformed(self.activityindicator, "stop ActivityIndicator")

        # Forget that `stop` was performed so it can be checked again
        EventLog.reset()

        # Already stopped, no action performed
        self.activityindicator.stop()
        self.assertActionNotPerformed(self.activityindicator, "stop ActivityIndicator")

    def test_already_running(self):
        # Creating a new progress bar with running=True so it is already running
        self.activityindicator = toga.ActivityIndicator(running=True)

        # Asserting that start() function is invoked on the underlying widget
        self.assertActionPerformed(self.activityindicator, "start ActivityIndicator")

        # Asserting is_running to be True
        self.assertTrue(self.activityindicator.is_running)
