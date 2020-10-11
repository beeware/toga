import unittest
from unittest import mock

import toga
import toga_dummy
from toga.sources.list_source import ListSource


class TestDataSourceCommandSet(unittest.TestCase):

    def setUp(self):
        self.label = "Label"
        self.group = toga.Group("Some Label")
        self.section = 7
        self.order = 2
        self.data = ListSource(data=["one", "two", "three"], accessors=["value"])
        self.item_action = mock.Mock()
        self.app = mock.Mock()
        self.commands_set = toga.DataSourceCommandSet(
            self.label,
            self.data,
            factory=toga_dummy.factory,
            group=self.group,
            section=self.section,
            order=self.order,
            item_to_label=lambda item: item.value,
            item_action=self.item_action,
            app=self.app
        )

    def test_properties(self):
        self.assertEqual(self.commands_set.label, self.label)
        self.assertEqual(self.commands_set.group, self.group)
        self.assertEqual(self.commands_set.section, self.section)
        self.assertEqual(self.commands_set.order, self.order)

    def test_all_commands(self):
        self.assert_all_commands(
            (
                *self.group.to_tuple(),
                (self.section, self.order, self.label),
                (0, 0, "one")
            ),
            (
                *self.group.to_tuple(),
                (self.section, self.order, self.label),
                (0, 1, "two")
            ),
            (
                *self.group.to_tuple(),
                (self.section, self.order, self.label),
                (0, 2, "three")
            ),
        )

    def test_command_action(self):
        widget = mock.Mock()
        all_commands = list(self.commands_set)
        for command in all_commands:
            command.action(widget)
        self.assertEqual(
            self.item_action.call_args_list,
            [
                mock.call(all_commands[0], self.data[0]),
                mock.call(all_commands[1], self.data[1]),
                mock.call(all_commands[2], self.data[2]),
            ]
        )

    def test_none_command_action(self):
        commands_set = toga.DataSourceCommandSet(
            self.label,
            self.data,
            item_to_label=lambda item: item.value,
            factory=toga_dummy.factory,
            item_action=None,
        )
        for command in commands_set:
            self.assertIsNone(command.action)

    def test_insert(self):
        self.data.insert(1, "four")
        self.assert_all_commands(
            (
                *self.group.to_tuple(),
                (self.section, self.order, self.label),
                (0, 0, "one")
            ),
            (
                *self.group.to_tuple(),
                (self.section, self.order, self.label),
                (0, 1, "four")
            ),
            (
                *self.group.to_tuple(),
                (self.section, self.order, self.label),
                (0, 2, "two")
            ),
            (
                *self.group.to_tuple(),
                (self.section, self.order, self.label),
                (0, 3, "three")
            ),
        )

    def test_remove(self):
        self.data.remove(self.data[1])
        self.assert_all_commands(
            (
                *self.group.to_tuple(),
                (self.section, self.order, self.label),
                (0, 0, "one"),
            ),
            (
                *self.group.to_tuple(),
                (self.section, self.order, self.label),
                (0, 1, "three"),
            ),
        )

    def assert_all_commands(self, *all_commands_tuples):
        self.assertEqual(
            [command.to_tuple() for command in self.commands_set],
            list(all_commands_tuples)
        )
