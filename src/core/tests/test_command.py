import unittest

import toga
import toga_dummy


class TestCommand(unittest.TestCase):
    def test_group_init_no_order(self):
        grp = toga.Group('label')
        self.assertEqual(grp.label, 'label')
        self.assertEqual(grp.order, 0)
    
    def test_group_init_with_order(self):
        grp = toga.Group('label', 2)
        self.assertEqual(grp.label, 'label')
        self.assertEqual(grp.order, 2)
    
    def test_group_lt(self):
        grp1, grp2 = toga.Group('A'), toga.Group('B')
        self.assertTrue(toga.Group('A', 1) < toga.Group('A', 2))
        self.assertTrue(toga.Group('A') < toga.Group('B'))
    
    def test_group_eq(self):
        self.assertEqual(toga.Group('A'), toga.Group('A'))
        self.assertEqual(toga.Group('A', 1), toga.Group('A', 1))
        self.assertNotEqual(toga.Group('A'), toga.Group('B'))
        self.assertNotEqual(toga.Group('A', 1), toga.Group('A', 2))
        self.assertNotEqual(toga.Group('A', 1), toga.Group('B', 1))
    
    def test_command_init_defaults(self):
        cmd = toga.Command(lambda x: print('Hello World'), 'test', factory=toga_dummy.factory)
        self.assertEqual(cmd.label, 'test')
        self.assertEqual(cmd.shortcut, None)
        self.assertEqual(cmd.tooltip, None)
        self.assertEqual(cmd.icon_id, None)
        self.assertEqual(cmd.group, toga.Group.COMMANDS)
        self.assertEqual(cmd.section, 0)
        self.assertEqual(cmd.order, 0)
        self.assertTrue(cmd._enabled)
        self.assertEqual(cmd._widgets, [])
    
    def test_command_init_kargs(self):
        grp = toga.Group('Test group', order=10)
        cmd = toga.Command(lambda x: print('Hello World'),
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
        self.assertEqual(cmd.icon_id, 'icons/none.png')
        self.assertEqual(cmd.group, grp)
        self.assertEqual(cmd.section, 1)
        self.assertEqual(cmd.order, 1)
        self.assertTrue(cmd._enabled)
        self.assertEqual(cmd._widgets, [])
        self.assertTrue(cmd.enabled)
        cmd.enabled = False
        self.assertFalse(cmd._enabled)
        self.assertFalse(cmd.enabled)
    
    def test_cmd_sort_key(self):
        grp = toga.Group('Test group', order=10)
        cmd = toga.Command(lambda x: print('Hello World'),
                           label='test',
                           tooltip='test command',
                           shortcut='t',
                           icon='icons/none.png',
                           group=grp,
                           section=1,
                           order=1,
                           factory=toga_dummy.factory
                           )
        self.assertEqual(toga.cmd_sort_key(cmd), (grp, 1, 1, 'test'))

class TestCommandSet(unittest.TestCase):
    changed = False

    def _changed(self):
        self.changed = True
        
    def test_cmdset_init(self):
        test_widget = toga.Widget(factory=toga_dummy.factory)
        cs = toga.CommandSet(test_widget)
        self.assertEqual(cs.widget, test_widget)
        self.assertEqual(cs._values, set())
        self.assertEqual(cs.on_change, None)
    
    def test_cmdset_add(self):
        self.changed = False
        test_widget = toga.Widget(factory=toga_dummy.factory)
        cs = toga.CommandSet(test_widget, on_change=self._changed)
        grp = toga.Group('Test group', order=10)
        cmd = toga.Command(lambda x: print('Hello World'),
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
    
    def test_cmdset_iter(self):
        test_widget = toga.Widget(factory=toga_dummy.factory)
        cs = toga.CommandSet(test_widget)
        grp = toga.Group('Test group', order=10)
        cmd = toga.Command(lambda x: print('Hello World'),
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
        self.assertEqual(list(cs), [cmd])
