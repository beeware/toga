import toga
import toga_dummy
from toga_dummy.utils import TestCase, TestStyle


class OptionContainerTests(TestCase):
    def setUp(self):
        super().setUp()

        self.op_container = toga.OptionContainer(style=TestStyle(), factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.op_container._impl.interface, self.op_container)
        self.assertActionPerformed(self.op_container, 'create OptionContainer')

    def test_adding_container_invokes_add_content(self):
        widget = toga.Box(style=TestStyle(), factory=toga_dummy.factory)
        label = 'New Container'

        self.op_container.add(label, widget)
        self.assertActionPerformedWith(self.op_container, 'add content', label=label, widget=widget._impl)

        self.assertActionPerformedWith(widget, 'set bounds', x=0, y=0, width=0, height=0)

    def test_widget_refresh_sublayouts(self):
        widget = toga.Box(style=TestStyle(), factory=toga_dummy.factory)
        label = 'New Container'

        self.op_container.add(label, widget)
        self.assertActionPerformedWith(self.op_container, 'add content', label=label, widget=widget._impl)
        self.assertActionPerformedWith(widget, 'set bounds', x=0, y=0, width=0, height=0)

        # Clear event log to verify new set bounds for refresh
        self.reset_event_log()

        self.op_container.refresh_sublayouts()
        self.assertActionPerformedWith(widget, 'set bounds', x=0, y=0, width=0, height=0)
