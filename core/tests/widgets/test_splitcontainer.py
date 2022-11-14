from unittest import mock

import toga
from toga_dummy.utils import TestCase, TestStyle


class SplitContainerTests(TestCase):
    def setUp(self):
        super().setUp()
        self.content = [toga.Box(style=TestStyle()), toga.Box(style=TestStyle())]
        self.split = toga.SplitContainer(style=TestStyle())

    def test_widget_created(self):
        self.assertEqual(self.split._impl.interface, self.split)
        self.assertActionPerformed(self.split, "create SplitContainer")

    def test_setting_content_valid_input(self):
        new_content = [toga.Box(style=TestStyle()), toga.Box(style=TestStyle())]
        self.split.content = new_content
        self.assertEqual(self.split.content, new_content)

    def test_setting_content_false_input(self):
        with self.assertRaises(Exception):
            self.split.content = toga.Box()

        with self.assertRaises(ValueError):
            self.split.content = [toga.Box()]

    def test_setting_content_invokes_impl_method(self):
        new_content = [toga.Box(style=TestStyle()), toga.Box(style=TestStyle())]
        self.split.content = new_content
        self.assertActionPerformedWith(
            self.split, "add content", position=0, widget=new_content[0]._impl
        )
        self.assertActionPerformedWith(
            self.split, "add content", position=1, widget=new_content[1]._impl
        )

        self.assertActionPerformedWith(
            new_content[0], "set bounds", x=0, y=0, width=0, height=0
        )
        self.assertActionPerformedWith(
            new_content[1], "set bounds", x=0, y=0, width=0, height=0
        )

    def test_direction_property_default(self):
        self.assertEqual(self.split.direction, True)

    def test_setting_direction_property_invokes_impl_method(self):
        new_value = False
        self.split.direction = new_value
        self.assertValueSet(self.split, "direction", new_value)

    def test_setting_content_valid_input_with_tuple_of2(self):
        new_content = [
            (toga.Box(style=TestStyle()), 1.2),
            (toga.Box(style=TestStyle()), 2.5),
        ]
        self.split.content = new_content
        self.assertEqual(self.split._weight[0], 1.2)
        self.assertEqual(self.split._weight[1], 2.5)

    def test_setting_content_valid_input_with_tuple_of3(self):
        new_content = [
            (toga.Box(style=TestStyle()), 1.2),
            (toga.Box(style=TestStyle()), 2.5, False),
        ]
        self.split.content = new_content
        self.assertEqual(self.split._weight[0], 1.2)
        self.assertEqual(self.split._weight[1], 2.5)
        self.assertActionPerformedWith(
            self.split,
            "add content",
            position=0,
            widget=new_content[0][0]._impl,
            flex=True,
        )
        self.assertActionPerformedWith(
            self.split,
            "add content",
            position=1,
            widget=new_content[1][0]._impl,
            flex=False,
        )

    def test_setting_content_valid_input_with_tuple_of_more3(self):
        new_content = [
            (toga.Box(style=TestStyle()), 1.2, True, True),
            (toga.Box(style=TestStyle()), 2.5, False, True),
        ]
        with self.assertRaises(ValueError):
            self.split.content = new_content

    def test_set_window_without_content(self):
        window = mock.Mock()
        self.split.window = window
        self.assertEqual(self.split.window, window)

    def test_set_window_with_content(self):
        self.split.content = self.content
        for content in self.content:
            self.assertIsNone(content.window)

        window = mock.Mock()
        self.split.window = window

        self.assertEqual(self.split.window, window)
        for content in self.content:
            self.assertEqual(content.window, window)

    def test_set_app_without_content(self):
        app = mock.Mock()
        self.split.app = app
        self.assertEqual(self.split.app, app)

    def test_set_app_with_content(self):
        self.split.content = self.content
        for content in self.content:
            self.assertIsNone(content.app)

        app = mock.Mock()
        self.split.app = app

        self.assertEqual(self.split.app, app)
        for content in self.content:
            self.assertEqual(content.app, app)

    def test_refresh_without_content(self):
        self.split.refresh()
        self.assertActionPerformedWith(
            self.split, "set bounds", x=0, y=0, width=0, height=0
        )

    def test_refresh_with_content(self):
        for content in self.content:
            self.assertActionNotPerformed(content, "set bound")

        self.split.content = self.content

        self.split.refresh()
        self.assertActionPerformedWith(
            self.split, "set bounds", x=0, y=0, width=0, height=0
        )
        for content in self.content:
            self.assertActionPerformedWith(
                content, "set bounds", x=0, y=0, width=0, height=0
            )
