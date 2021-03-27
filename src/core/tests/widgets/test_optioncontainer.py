from unittest import mock

import toga
import toga_dummy
from toga_dummy.utils import TestCase, TestStyle


class OptionContainerTests(TestCase):
    def setUp(self):
        super().setUp()

        self.on_select = mock.Mock()
        self.op_container = toga.OptionContainer(
            style=TestStyle(),
            factory=toga_dummy.factory,
            on_select=self.on_select
        )
        self.widget = toga.Box(style=TestStyle(), factory=toga_dummy.factory)
        self.label2, self.widget2 = "Widget 2", toga.Box(
            style=TestStyle(), factory=toga_dummy.factory
        )
        self.label3, self.widget3 = "Widget 3", toga.Box(
            style=TestStyle(), factory=toga_dummy.factory
        )
        self.label = 'New Container'
        self.op_container.add(self.label, self.widget)

    def assert_tab(self, tab, index, label, widget, enabled):
        self.assertEqual(tab.index, index)
        self.assertEqual(tab.label, label)
        self.assertEqual(tab._interface, self.op_container)
        self.assertEqual(tab.enabled, enabled)
        self.assertEqual(tab.content, widget)

    def add_widgets(self):
        self.op_container.add(self.label2, self.widget2)
        self.op_container.add(self.label3, self.widget3)

    def test_on_select(self):
        self.assertEqual(self.op_container.on_select._raw, self.on_select)

    def test_widget_created(self):
        self.assertEqual(self.op_container._impl.interface, self.op_container)
        self.assertActionPerformed(self.op_container, 'create OptionContainer')

    def test_adding_container_invokes_add_content(self):
        self.assertActionPerformedWith(
            self.op_container, 'add content', label=self.label, widget=self.widget._impl
        )

        self.assertActionPerformedWith(
            self.widget, 'set bounds', x=0, y=0, width=0, height=0
        )

    def test_widget_refresh_sublayouts(self):
        # Clear event log to verify new set bounds for refresh
        self.reset_event_log()

        self.op_container.refresh_sublayouts()
        self.assertActionPerformedWith(
            self.widget, 'set bounds', x=0, y=0, width=0, height=0
        )

    def test_set_current_tab_as_index(self):
        self.add_widgets()
        self.op_container.current_tab = 1
        self.assert_tab(
            self.op_container.current_tab,
            index=1,
            label=self.label2,
            widget=self.widget2,
            enabled=True,
        )

    def test_set_current_tab_as_label(self):
        self.add_widgets()
        self.op_container.current_tab = self.label3
        self.assert_tab(
            self.op_container.current_tab,
            index=2,
            label=self.label3,
            widget=self.widget3,
            enabled=True,
        )

    def test_set_current_tab_as_tab(self):
        self.add_widgets()
        self.op_container.current_tab = self.op_container.content[1]
        self.assert_tab(
            self.op_container.current_tab,
            index=1,
            label=self.label2,
            widget=self.widget2,
            enabled=True,
        )

    def test_current_tab_increment(self):
        self.add_widgets()
        self.op_container.current_tab = 1
        self.op_container.current_tab += 1
        self.assert_tab(
            self.op_container.current_tab,
            index=2,
            label=self.label3,
            widget=self.widget3,
            enabled=True,
        )

    def test_set_current_tab_as_label_raises_an_error(self):
        self.add_widgets()

        def set_label():
            self.op_container.current_tab = "I do not exist!"

        self.assertRaises(ValueError, set_label)

    def test_current_tab_string_increment_raises_an_error(self):
        self.add_widgets()

        def set_label():
            self.op_container.current_tab += "I do not exist!"

        self.assertRaises(ValueError, set_label)

    def test_current_tab_string_decrement_raises_an_error(self):
        self.add_widgets()

        def set_label():
            self.op_container.current_tab -= "I do not exist!"

        self.assertRaises(ValueError, set_label)

    def test_current_tab_decrement(self):
        self.add_widgets()
        self.op_container.current_tab = 1
        self.op_container.current_tab -= 1
        self.assert_tab(
            self.op_container.current_tab,
            index=0,
            label=self.label,
            widget=self.widget,
            enabled=True,
        )

    def test_disable_tab(self):
        self.op_container.current_tab.enabled = False
        self.assertEqual(self.op_container.current_tab.enabled, False)

    def test_content_repr(self):
        self.add_widgets()
        self.assertEqual(
            (
                "OptionList([OptionItem(title=New Container), "
                "OptionItem(title=Widget 2), "
                "OptionItem(title=Widget 3)])"
            ),
            repr(self.op_container.content)
        )

    def test_add_tabs(self):
        self.add_widgets()
        self.assertEqual(len(self.op_container.content), 3)
        self.assertEqual(self.op_container.content[0]._content, self.widget)
        self.assertEqual(self.op_container.content[1]._content, self.widget2)
        self.assertEqual(self.op_container.content[2]._content, self.widget3)

    def test_remove_tab(self):
        self.add_widgets()
        self.op_container.remove(1)
        self.assertEqual(len(self.op_container.content), 2)
        self.assertEqual(self.op_container.content[0]._content, self.widget)
        self.assertEqual(self.op_container.content[1]._content, self.widget3)

    def test_set_content_in_constructor(self):
        new_container = toga.OptionContainer(
            style=TestStyle(),
            factory=toga_dummy.factory,
            content=[
                (self.label, self.widget),
                (self.label2, self.widget2),
                (self.label3, self.widget3),
            ]
        )
        self.assertEqual(len(new_container.content), 3)
        self.assertEqual(new_container.content[0]._content, self.widget)
        self.assertEqual(new_container.content[1]._content, self.widget2)
        self.assertEqual(new_container.content[2]._content, self.widget3)

    def test_set_window(self):
        window = mock.Mock()
        self.op_container.window = window
        for item in self.op_container.content:
            self.assertEqual(item._content.window, window)
