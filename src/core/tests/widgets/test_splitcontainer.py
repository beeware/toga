import toga
import toga_dummy
from toga_dummy.utils import TestCase, TestStyle


class SplitContainerTests(TestCase):
    def setUp(self):
        self.content = [
            toga.Box(style=TestStyle(), factory=toga_dummy.factory),
            toga.Box(style=TestStyle(), factory=toga_dummy.factory)
        ]
        self.split = toga.SplitContainer(style=TestStyle(), factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.split._impl.interface, self.split)
        self.assertActionPerformed(self.split, 'create SplitContainer')

    def test_setting_content_valid_input(self):
        new_content = [
            toga.Box(style=TestStyle(), factory=toga_dummy.factory),
            toga.Box(style=TestStyle(), factory=toga_dummy.factory)
        ]
        self.split.content = new_content
        self.assertEqual(self.split.content, new_content)

    def test_setting_content_false_input(self):
        with self.assertRaises(Exception):
            self.split.content = toga.Box(factory=toga_dummy.factory)

        with self.assertRaises(ValueError):
            self.split.content = [toga.Box(factory=toga_dummy.factory)]

    def test_setting_content_invokes_impl_method(self):
        new_content = [
            toga.Box(style=TestStyle(), factory=toga_dummy.factory),
            toga.Box(style=TestStyle(), factory=toga_dummy.factory)
        ]
        self.split.content = new_content
        self.assertActionPerformedWith(self.split, 'add content', position=0, widget=new_content[0]._impl)
        self.assertActionPerformedWith(self.split, 'add content', position=1, widget=new_content[1]._impl)

        self.assertActionPerformedWith(new_content[0], 'set bounds', x=0, y=0, width=0, height=0)
        self.assertActionPerformedWith(new_content[1], 'set bounds', x=0, y=0, width=0, height=0)

    def test_setting_content_with_weights(self):
        new_content = [
            (toga.Box(style=TestStyle(), factory=toga_dummy.factory), 0.3),
            (toga.Box(style=TestStyle(), factory=toga_dummy.factory), 0.7)
        ]
        self.split.content = new_content

    def test_direction_property_default(self):
        self.assertEqual(self.split.direction, True)

    def test_setting_direction_property_invokes_impl_method(self):
        new_value = False
        self.split.direction = new_value
        self.assertValueSet(self.split, 'direction', new_value)

    def test_setting_app_for_container_content(self):
        new_content = [
            toga.Box(style=TestStyle(), factory=toga_dummy.factory),
            toga.Box(style=TestStyle(), factory=toga_dummy.factory)
        ]
        self.split.content = new_content

        self.split.set_app()

    def test_setting_window_for_container_content(self):
        new_content = [
            toga.Box(style=TestStyle(), factory=toga_dummy.factory),
            toga.Box(style=TestStyle(), factory=toga_dummy.factory)
        ]
        self.split.content = new_content

        self.split.set_window()

    def test_refresh_sublayouts(self):
        new_content = [
            toga.Box(style=TestStyle(), factory=toga_dummy.factory),
            toga.Box(style=TestStyle(), factory=toga_dummy.factory)
        ]
        self.split.content = new_content
        self.split.refresh_sublayouts()