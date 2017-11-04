import toga
import toga_dummy
from toga_dummy.utils import TestCase


class OptionContainerTests(TestCase):
    def setUp(self):
        super().setUp()

        self.op_container = toga.OptionContainer(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.op_container._impl.interface, self.op_container)
        self.assertActionPerformed(self.op_container, 'create OptionContainer')

    def test_adding_container_invokes_add_content(self):
        widget = toga.Box(factory=toga_dummy.factory)
        label = 'New Container'

        self.op_container.add(label, widget)
        self.assertActionPerformedWith(self.op_container, 'add content', label=label, widget=widget._impl)
