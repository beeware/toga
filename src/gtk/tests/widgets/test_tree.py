import unittest
from gi.repository import Gtk

import toga


def handle_events():
    while Gtk.events_pending():
        Gtk.main_iteration_do(blocking=False)


class TestGtkTree(unittest.TestCase):

    def setUp(self):
        self.tree = toga.Tree(
            headings=("one", "two")
        )

        # make a shortcut for easy use
        self.gtk_tree = self.tree._impl

        self.window = Gtk.Window()
        self.window.add(self.tree._impl.native)

    def test_change_source(self):
        # Clear the table directly
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
        self.assertEqual(tuple(store[0]), ("A1", "A2"))
        self.assertEqual(tuple(store[1]), ("B1", "B2"))
        self.assertEqual(tuple(store[(1, 0)]), ("B1.1", "B2.1"))

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
        # Insert a node
        node_data = ("1", "2")
        node = self.tree.data.insert(None, 0, *node_data)

        # Make sure it's in there
        self.assertTrue(node in self.gtk_tree.nodes)

        # Get the Gtk.TreeIter
        tree_iter = self.gtk_tree.nodes[node]

        # Make sure it's a Gtk.TreeIter
        self.assertTrue(isinstance(tree_iter, Gtk.TreeIter))

        # Make sure it's the correct Gtk.TreeIter
        self.assertEqual(node, self.gtk_tree.get_node(tree_iter))

        # Get the Gtk.TreePath of the Gtk.TreeIter
        path = self.gtk_tree.store.get_path(tree_iter)

        # Make sure it's the correct Gtk.TreePath
        self.assertTrue(isinstance(path, Gtk.TreePath))
        self.assertEqual(path, Gtk.TreePath(0))
        # self.assertEqual(str(path), "0")
        # self.assertEqual(tuple(path), (0,))

        # Make sure the node got stored correctly
        result_node = self.gtk_tree.store[path]
        self.assertEqual(tuple(result_node), node_data)

    def test_insert_child_node(self):
        self.tree.data = []

        # Insert blank node as parent
        parent = self.tree.data.insert(None, 0, *(None, None))

        # Insert a child node
        node_data = ("1", "2")
        node = self.tree.data.insert(parent, 0, *node_data)

        # Make sure it's in there
        self.assertTrue(node in self.gtk_tree.nodes)

        # Get the Gtk.TreeIter
        tree_iter = self.gtk_tree.nodes[node]

        # Make sure it's a Gtk.TreeIter
        self.assertTrue(isinstance(tree_iter, Gtk.TreeIter))

        # Make sure it's the correct Gtk.TreeIter
        self.assertEqual(node, self.gtk_tree.get_node(tree_iter))

        # Get the Gtk.TreePath of the Gtk.TreeIter
        path = self.gtk_tree.store.get_path(tree_iter)

        # Make sure it's the correct Gtk.TreePath
        self.assertTrue(isinstance(path, Gtk.TreePath))
        self.assertEqual(str(path), "0:0")
        self.assertEqual(tuple(path), (0, 0))
        self.assertEqual(path, Gtk.TreePath((0, 0)))

        # Make sure the node got stored correctly
        result_node = self.gtk_tree.store[path]
        self.assertEqual(tuple(result_node), node_data)

    def test_remove(self):
        # Insert a node
        node = self.tree.data.insert(None, 0, "1", "2")

        # Make sure it's in there
        self.assertTrue(node in self.gtk_tree.nodes)

        # Then remove it
        self.gtk_tree.remove(node)

        # Make sure its gone
        self.assertFalse(node in self.gtk_tree.nodes)

    def test_change(self):
        # Insert a node
        node = self.tree.data.insert(None, 0, "1", "2")

        # Make sure it's in there
        self.assertTrue(node in self.gtk_tree.nodes)

        # Change a column
        node.one = "something_changed"
        # (not testing that self.gtk_tree.change is called. The Core API
        # unit tests should ensure this already.)

        # Get the Gtk.TreeIter
        tree_iter = self.gtk_tree.nodes[node]

        # Make sure it's a Gtk.TreeIter
        self.assertTrue(isinstance(tree_iter, Gtk.TreeIter))

        # Make sure it's the correct Gtk.TreeIter
        self.assertEqual(node, self.gtk_tree.get_node(tree_iter))

        # Make sure the value changed
        path = self.gtk_tree.store.get_path(tree_iter)
        result_node = self.gtk_tree.store[path]
        self.assertEqual(tuple(result_node), (node.one, node.two))

    def test_method_compare_tree_iters(self):
        store = self.gtk_tree.store
        store.clear()
        store.append(None, ("1", "2"))

        # Gtk.TreeIters can't be compared directly
        self.assertNotEqual(store[0].iter, store[0].iter)

        self.assertTrue(self.gtk_tree.compare_tree_iters(
            store[0].iter,
            store[0].iter
        ))

    def test_method_get_node(self):
        # Put data in the Tree
        self.tree.data = []
        A = self.tree.data.append(None, one="A1", two="A2")
        tree_iter = self.gtk_tree.nodes[A]
        self.assertEqual(A, self.gtk_tree.get_node(tree_iter))

        with self.assertRaises(TypeError):
            self.gtk_tree.get_node(None)

    def test_node_persistence_for_replacement(self):
        self.tree.data = []
        A = self.tree.data.insert(None, 0, one="A1", two="A2")
        B = self.tree.data.insert(None, 0, one="B1", two="B2")

        # B should now precede A
        # test passes if A "knows" it has moved to index 1

        self.assertEqual(tuple(self.gtk_tree.store[0]), ("B1", "B2"))
        self.assertEqual(tuple(self.gtk_tree.store[1]), ("A1", "A2"))

    def test_node_persistence_for_deletion(self):
        self.tree.data = []
        A = self.tree.data.append(None, one="A1", two="A2")
        B = self.tree.data.append(None, one="B1", two="B2")

        self.tree.data.remove(A)

        # test passes if B "knows" it has moved to index 0
        self.assertEqual(tuple(self.gtk_tree.store[0]), ("B1", "B2"))

    def test_on_select_root_node(self):
        # Insert dummy nodes
        self.tree.data = []
        A = self.tree.data.append(None, one="A1", two="A2")
        B = self.tree.data.append(None, one="B1", two="B2")

        # Create a flag
        succeed = False

        def on_select(tree, row, *kw):
            # Make sure the right node was selected
            self.assertEqual(row, B)

            nonlocal succeed
            succeed = True

        self.tree.on_select = on_select

        # Select node B
        self.gtk_tree.selection.select_iter(self.gtk_tree.nodes[B])

        # Allow on_select to call
        handle_events()

        self.assertTrue(succeed)

    def test_on_select_child_node(self):
        # Insert two nodes
        self.tree.data = []
        A = self.tree.data.append(None, one="A1", two="A2")
        B = self.tree.data.append(A, one="B1", two="B2")

        # Create a flag
        succeed = False

        def on_select(tree, row):
            # Make sure the right node was selected
            self.assertEqual(row, B)

            nonlocal succeed
            succeed = True

        self.tree.on_select = on_select

        # Expand parent node (A) on Gtk.TreeView to allow selection
        path = self.gtk_tree.store.get_path(self.gtk_tree.nodes[A])
        self.gtk_tree.treeview.expand_row(path, True)

        # Select node B
        self.gtk_tree.selection.select_iter(self.gtk_tree.nodes[B])
        # Allow on_select to call
        handle_events()

        self.assertTrue(succeed)

    def test_on_select_deleted_node(self):
        # Insert two nodes
        self.tree.data = []
        A = self.tree.data.append(None, one="A1", two="A2")
        B = self.tree.data.append(None, one="B1", two="B2")

        # Create a flag
        succeed = False

        def on_select(tree, row):
            nonlocal succeed
            if row is not None:
                # Make sure the right node was selected
                self.assertEqual(row, B)

                # Remove node B. This should trigger on_select again
                tree.data.remove(row)
            else:
                self.assertEqual(row, None)
                succeed = True

        self.tree.on_select = on_select

        # Select node B
        self.gtk_tree.selection.select_iter(self.gtk_tree.nodes[B])

        # Allow on_select to call
        handle_events()

        self.assertTrue(succeed)
