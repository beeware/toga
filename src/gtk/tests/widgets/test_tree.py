import unittest
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except ImportError:
    import sys
    # If we're on Linux, Gtk *should* be available. If it isn't, make
    # Gtk an object... but in such a way that every test will fail,
    # because the object isn't actually the Gtk interface.
    if sys.platform == 'linux':
        Gtk = object()
    else:
        Gtk = None

import toga

from .utils import TreeModelListener


def handle_events():
    while Gtk.events_pending():
        Gtk.main_iteration_do(blocking=False)


@unittest.skipIf(Gtk is None, "Can't run GTK implementation tests on a non-Linux platform")
class TestGtkTree(unittest.TestCase):
    def setUp(self):
        self.tree = toga.Tree(
            headings=("one", "two")
        )

        # make a shortcut for easy use
        self.gtk_tree = self.tree._impl

        self.window = Gtk.Window()
        self.window.add(self.tree._impl.native)

    def assertNodeEqual(self, node, data):
        self.assertEqual(tuple(node)[1:], data)

    def test_change_source(self):
        # Clear the tree directly
        self.gtk_tree.clear()

        # Assign pre-constructed data
        self.tree.data = {
            ("A1", "A2"): [],
            ("B1", "B2"): [
                ("B1.1", "B2.1")
            ]
        }

        # Make sure the data was stored correctly
        store = self.gtk_tree.store
        self.assertNodeEqual(store[0], ("A1", "A2"))
        self.assertNodeEqual(store[1], ("B1", "B2"))
        self.assertNodeEqual(store[(1, 0)], ("B1.1", "B2.1"))

        # Clear the table with empty assignment
        self.tree.data = []

        # Make sure the table is empty
        self.assertEqual(len(store), 0)

        # Repeat with a few different cases
        self.tree.data = None
        self.assertEqual(len(store), 0)

        self.tree.data = ()
        self.assertEqual(len(store), 0)

    def test_insert_root_node(self):
        listener = TreeModelListener(self.gtk_tree.store)

        # Insert a node
        node_data = ("1", "2")
        node = self.tree.data.insert(None, 0, *node_data)

        # Make sure it's in there
        self.assertIsNotNone(listener.inserted_it)

        # Get the Gtk.TreeIter
        tree_iter = listener.inserted_it

        # Make sure it's a Gtk.TreeIter
        self.assertTrue(isinstance(tree_iter, Gtk.TreeIter))

        # Make sure it's the correct Gtk.TreeIter
        self.assertEqual(node, self.gtk_tree.store.get(tree_iter, 0)[0])

        # Get the Gtk.TreePath of the Gtk.TreeIter
        path = self.gtk_tree.store.get_path(tree_iter)

        # Make sure it's the correct Gtk.TreePath
        self.assertTrue(isinstance(path, Gtk.TreePath))
        self.assertEqual(path, Gtk.TreePath(0))
        self.assertEqual(listener.inserted_path, Gtk.TreePath(0))
        # self.assertEqual(str(path), "0")
        # self.assertNodeEqual(path), (0,))

        # Make sure the node got stored correctly
        self.assertNodeEqual(self.gtk_tree.store[path], node_data)

    def test_insert_child_node(self):
        listener = TreeModelListener(self.gtk_tree.store)

        self.tree.data = []

        # Insert blank node as parent
        parent = self.tree.data.insert(None, 0, *(None, None))

        listener.clear()

        # Insert a child node
        node_data = ("1", "2")
        node = self.tree.data.insert(parent, 0, *node_data)

        # Make sure it's in there
        self.assertIsNotNone(listener.inserted_path)

        # Get the Gtk.TreeIter
        tree_iter = listener.inserted_it

        # Make sure it's a Gtk.TreeIter
        self.assertTrue(isinstance(tree_iter, Gtk.TreeIter))

        # Make sure it's the correct Gtk.TreeIter
        self.assertEqual(node, self.gtk_tree.store.get(tree_iter, 0)[0])

        # Get the Gtk.TreePath of the Gtk.TreeIter
        path = self.gtk_tree.store.get_path(tree_iter)

        # Make sure it's the correct Gtk.TreePath
        self.assertTrue(isinstance(path, Gtk.TreePath))
        self.assertEqual(str(path), "0:0")
        self.assertEqual(tuple(path), (0, 0))
        self.assertEqual(path, Gtk.TreePath((0, 0)))
        self.assertEqual(listener.inserted_path, Gtk.TreePath((0, 0)))

        # Make sure the node got stored correctly
        self.assertNodeEqual(self.gtk_tree.store[path], node_data)

    def test_remove(self):
        listener = TreeModelListener(self.gtk_tree.store)

        # Insert a node
        node = self.tree.data.insert(None, 0, "1", "2")

        # Make sure it's in there
        self.assertIsNotNone(listener.inserted_it)

        # Then remove it
        self.gtk_tree.remove(node, index=0, parent=None)

        # Make sure its gone
        self.assertIsNone(self.gtk_tree.store.do_get_value(listener.inserted_it, 0))

    def test_change(self):
        listener = TreeModelListener(self.gtk_tree.store)

        # Insert a node
        node = self.tree.data.insert(None, 0, "1", "2")

        # Make sure it's in there
        self.assertIsNotNone(listener.inserted_path)
        self.assertEqual([0], listener.inserted_path.get_indices())

        # Change a column
        node.one = "something_changed"

        self.assertIsNotNone(listener.changed_path)
        self.assertIsNotNone(listener.changed_it)

        # Get the Gtk.TreeIter
        tree_iter = listener.changed_it

        # Make sure it's a Gtk.TreeIter
        self.assertTrue(isinstance(tree_iter, Gtk.TreeIter))

        # Make sure it's the correct Gtk.TreeIter
        self.assertEqual(node, self.gtk_tree.store.get(tree_iter, 0)[0])

        # Make sure the value changed
        path = self.gtk_tree.store.get_path(tree_iter)
        self.assertNodeEqual(self.gtk_tree.store[path], (node.one, node.two))

    def test_node_persistence_for_replacement(self):
        self.tree.data = []
        self.tree.data.insert(None, 0, one="A1", two="A2")
        self.tree.data.insert(None, 0, one="B1", two="B2")

        # B should now precede A
        # test passes if A "knows" it has moved to index 1

        self.assertNodeEqual(self.gtk_tree.store[0], ("B1", "B2"))
        self.assertNodeEqual(self.gtk_tree.store[1], ("A1", "A2"))

    def test_node_persistence_for_deletion(self):
        self.tree.data = []
        a = self.tree.data.append(None, one="A1", two="A2")
        self.tree.data.append(None, one="B1", two="B2")

        self.tree.data.remove(a)

        # test passes if B "knows" it has moved to index 0
        self.assertNodeEqual(self.gtk_tree.store[0], ("B1", "B2"))

    def test_on_select_root_node(self):
        listener = TreeModelListener(self.gtk_tree.store)

        # Insert dummy nodes
        self.tree.data = []
        self.tree.data.append(None, one="A1", two="A2")
        listener.clear()
        b = self.tree.data.append(None, one="B1", two="B2")

        # Create a flag
        succeed = False

        def on_select(tree, node):
            # Make sure the right node was selected
            self.assertEqual(node, b)

            nonlocal succeed
            succeed = True

        self.tree.on_select = on_select

        # Select node B
        self.gtk_tree.selection.select_iter(listener.inserted_it)

        # Allow on_select to call
        handle_events()

        self.assertTrue(succeed)

    def test_on_select_child_node(self):
        listener = TreeModelListener(self.gtk_tree.store)

        # Insert two nodes
        self.tree.data = []
        a = self.tree.data.append(None, one="A1", two="A2")
        a_iter = listener.inserted_it
        listener.clear()
        b = self.tree.data.append(a, one="B1", two="B2")

        # Create a flag
        succeed = False

        def on_select(tree, node):
            # Make sure the right node was selected
            self.assertEqual(node, b)

            nonlocal succeed
            succeed = True

        self.tree.on_select = on_select

        # Expand parent node (a) on Gtk.TreeView to allow selection
        path = self.gtk_tree.store.get_path(a_iter)
        self.gtk_tree.treeview.expand_row(path, True)

        # Select node B
        self.gtk_tree.selection.select_iter(listener.inserted_it)
        # Allow on_select to call
        handle_events()

        self.assertTrue(succeed)

    def test_on_select_deleted_node(self):
        listener = TreeModelListener(self.gtk_tree.store)

        # Insert two nodes
        self.tree.data = []
        self.tree.data.append(None, one="A1", two="A2")
        b = self.tree.data.append(None, one="B1", two="B2")

        # Create a flag
        succeed = False

        def on_select(tree, node):
            nonlocal succeed
            if node is not None:
                # Make sure the right node was selected
                self.assertEqual(node, b)

                # Remove node B. This should trigger on_select again
                tree.data.remove(node)
            else:
                self.assertEqual(node, None)
                succeed = True

        self.tree.on_select = on_select

        # Select node B
        self.gtk_tree.selection.select_iter(listener.inserted_it)

        # Allow on_select to call
        handle_events()

        self.assertTrue(succeed)
