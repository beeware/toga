import random
import unittest

import toga
import toga_dummy
from tests.utils import order_test

from toga import GROUP_BREAK, SECTION_BREAK
from toga_dummy.utils import TestCase

PARENT_GROUP1 = toga.Group("P", 1)
CHILD_GROUP1 = toga.Group("C", order=2, parent=PARENT_GROUP1)
CHILD_GROUP2 = toga.Group("B", order=4, parent=PARENT_GROUP1)
PARENT_GROUP2 = toga.Group("O", 2)
CHILD_GROUP3 = toga.Group("A", 2, parent=PARENT_GROUP2)

A = toga.Command(None, "A", group=PARENT_GROUP2, order=1)
S = toga.Command(None, "S", group=PARENT_GROUP1, order=5)
T = toga.Command(None, "T", group=CHILD_GROUP2, order=2)
U = toga.Command(None, "U", group=CHILD_GROUP2, order=1)
V = toga.Command(None, "V", group=PARENT_GROUP1, order=3)
B = toga.Command(None, "B", group=CHILD_GROUP1, section=2, order=1)
W = toga.Command(None, "W", group=CHILD_GROUP1, order=4)
X = toga.Command(None, "X", group=CHILD_GROUP1, order=2)
Y = toga.Command(None, "Y", group=CHILD_GROUP1, order=1)
Z = toga.Command(None, "Z", group=PARENT_GROUP1, order=1)

COMMANDS_IN_ORDER = [Z, Y, X, W, B, V, U, T, S, A]
COMMANDS_IN_SET = [
    Z, GROUP_BREAK,
    Y, X, W, SECTION_BREAK, B, GROUP_BREAK,
    V, GROUP_BREAK,
    U, T, GROUP_BREAK,
    S, GROUP_BREAK,
    A,
]


class TestCommand(TestCase):
    def setUp(self):
        # We need to define a test app to instantiate paths.
        self.app = toga.App(
            formal_name='Test App',
            app_id='org.beeware.test-app',
            factory=toga_dummy.factory,
        )

    def test_command_init_defaults(self):
        cmd = toga.Command(lambda x: print('Hello World'), 'test', factory=toga_dummy.factory)
        self.assertEqual(cmd.label, 'test')
        self.assertEqual(cmd.shortcut, None)
        self.assertEqual(cmd.tooltip, None)
        self.assertEqual(cmd.icon, None)
        self.assertEqual(cmd.group, toga.Group.COMMANDS)
        self.assertEqual(cmd.section, 0)
        self.assertEqual(cmd.order, 0)
        self.assertTrue(cmd._enabled)

    def test_command_init_kargs(self):
        grp = toga.Group('Test group', order=10)
        cmd = toga.Command(
            lambda x: print('Hello World'),
            label='test',
            tooltip='test command',
            shortcut='t',
            icon='icons/none.png',
            group=grp,
            section=1,
            order=1,
            factory=toga_dummy.factory
        )
        self.assertEqual(cmd.label, 'test')
        self.assertEqual(cmd.shortcut, 't')
        self.assertEqual(cmd.tooltip, 'test command')
        self.assertEqual(cmd.icon.path, 'icons/none.png')
        self.assertEqual(cmd.group, grp)
        self.assertEqual(cmd.section, 1)
        self.assertEqual(cmd.order, 1)
        self.assertTrue(cmd._enabled)
        self.assertTrue(cmd.enabled)
        cmd.enabled = False
        self.assertFalse(cmd._enabled)
        self.assertFalse(cmd.enabled)

    def test_command_bind(self):
        grp = toga.Group('Test group', order=10)
        cmd = toga.Command(
            lambda x: print('Hello World'),
            label='test',
            tooltip='test command',
            shortcut='t',
            icon='icons/none.png',
            group=grp,
            section=1,
            order=1,
            factory=toga_dummy.factory
        )
        retur_val = cmd.bind(factory=toga_dummy.factory)
        self.assertEqual(retur_val, cmd._impl)

    def test_command_enabler(self):
        grp = toga.Group('Test group', order=10)
        cmd = toga.Command(
            lambda x: print('Hello World'),
            label='test',
            tooltip='test command',
            shortcut='t',
            icon='icons/none.png',
            group=grp,
            section=1,
            order=1,
            factory=toga_dummy.factory,
        )
        cmd.bind(toga_dummy.factory)
        cmd.enabled = False
        self.assertActionPerformedWith(cmd, 'set enabled', value=False)
        cmd.enabled = True
        self.assertActionPerformedWith(cmd, 'set enabled', value=True)

    test_order_commands_by_label = order_test(
        toga.Command(None, "A"), toga.Command(None, "B")
    )
    test_order_commands_by_number = order_test(
        toga.Command(None, "B", order=1), toga.Command(None, "A", order=2)
    )
    test_order_commands_by_section = order_test(
        toga.Command(None, "B", group=PARENT_GROUP1, section=1, order=2),
        toga.Command(None, "A", group=PARENT_GROUP1, section=2, order=1)
    )
    test_order_commands_by_groups = order_test(*COMMANDS_IN_ORDER)


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
            label='test',
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
        cs = toga.CommandSet(
            factory=toga_dummy.factory,
            widget=test_widget
        )
        commands = list(COMMANDS_IN_ORDER)
        random.shuffle(commands)
        cs.add(*commands)
        self.assertEqual(list(cs), COMMANDS_IN_SET)
