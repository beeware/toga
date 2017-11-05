import toga
import toga_dummy
from toga_dummy.utils import TestCase


class SplitContainerTests(TestCase):
    def setUp(self):
        self.content = [toga.Box(factory=toga_dummy.factory), toga.Box(factory=toga_dummy.factory)]
        self.split = toga.SplitContainer(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.split._impl.interface, self.split)
        self.assertActionPerformed(self.split, 'create SplitContainer')

    def test_setting_content_valid_input(self):
        new_content = [toga.Box(factory=toga_dummy.factory), toga.Box(factory=toga_dummy.factory)]
        self.split.content = new_content
        self.assertEqual(self.split.content, new_content)

    def test_setting_content_false_input(self):
        with self.assertRaises(Exception):
            self.split.content = toga.Box(factory=toga_dummy.factory)

        with self.assertRaises(ValueError):
            self.split.content = [toga.Box(factory=toga_dummy.factory)]

    def test_setting_content_invokes_impl_method(self):
        new_content = [toga.Box(factory=toga_dummy.factory), toga.Box(factory=toga_dummy.factory)]
        self.split.content = new_content
        self.assertActionPerformedWith(self.split, 'add content', position=0, widget=new_content[0]._impl)
        self.assertActionPerformedWith(self.split, 'add content', position=1, widget=new_content[1]._impl)

    def test_direction_property_default(self):
        self.assertEqual(self.split.direction, True)

    def test_setting_direction_property_invokes_impl_method(self):
        new_value = False
        self.split.direction = new_value
        self.assertValueSet(self.split, 'direction', new_value)
