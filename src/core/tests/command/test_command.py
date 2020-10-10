import toga
import toga_dummy
from tests.utils import order_test

from tests.command.constants import PARENT_GROUP1, COMMANDS_IN_ORDER
from toga_dummy.utils import TestCase


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

    def test_command_repr(self):
        self.assertEqual(
            repr(toga.Command(None, "A", group=PARENT_GROUP1, order=1, section=4)),
            "<Command label=A group=<Group label=P order=1 parent=None> section=4 order=1>"
        )

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
