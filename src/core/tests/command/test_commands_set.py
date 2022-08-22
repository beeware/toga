import random
import unittest
from unittest.mock import Mock

import toga
import toga_dummy
from tests.command.constants import COMMANDS_IN_ORDER, COMMANDS_IN_SET


class TestCommandSet(unittest.TestCase):
    changed = False

    def _changed(self):
        self.changed = True

    def test_cmdset_init(self):
        test_widget = toga.Widget(factory=toga_dummy.factory)
        cs = toga.CommandSet(test_widget)
        self.assertEqual(cs._commands, set())
        self.assertEqual(cs.on_change, None)

    def test_cmdset_add(self):
        self.changed = False
        test_widget = toga.Widget(factory=toga_dummy.factory)
        cs = toga.CommandSet(
            factory=toga_dummy.factory,
            widget=test_widget,
            on_change=self._changed
        )
        grp = toga.Group('Test group', order=10)
        cmd = toga.Command(
            lambda x: print('Hello World'),
            text='test',
            tooltip='test command',
            shortcut='t',
            icon='icons/none.png',
            group=grp,
            section=1,
            order=1,
            factory=toga_dummy.factory
        )
        cs.add(cmd)

        self.assertTrue(self.changed)
        self.assertIsNotNone(cmd._impl)

    def test_cmdset_iter_in_order(self):
        test_widget = toga.Widget(factory=toga_dummy.factory)
        test_widget._impl = Mock()
        test_widget.app = Mock()
        cs = toga.CommandSet(
            factory=toga_dummy.factory,
            widget=test_widget
        )
        commands = list(COMMANDS_IN_ORDER)
        random.shuffle(commands)
        cs.add(*commands)
        test_widget.app.commands.add.assert_called_once_with(*commands)
        self.assertEqual(list(cs), COMMANDS_IN_SET)
