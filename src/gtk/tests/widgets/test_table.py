import unittest
from gi.repository import Gtk

import toga

def handle_events():
    while Gtk.events_pending():
        Gtk.main_iteration_do(blocking=False)

class TestGtkTable(unittest.TestCase):

    def setUp(self):
        self.table = toga.Table(
            headings=("one", "two")
        )

        # make a shortcut for easy use
        self.gtk_table = self.table._impl

        self.window = Gtk.Window()
        self.window.add(self.table._impl.native)

    def test_insert(self):
        # Insert a row
        row_data = ("1", "2")
        INSERTED_AT = 0
        row = self.table.data.insert(INSERTED_AT, *row_data)

        # Make sure it's in there
        self.assertTrue(row in self.gtk_table.rows)

        # Get the Gtk.TreeIter
        tree_iter = self.gtk_table.rows[row]

        # Make sure it's a Gtk.TreeIter
        self.assertTrue(isinstance(tree_iter, Gtk.TreeIter))

        # Make sure it's the correct Gtk.TreeIter
        self.assertEqual(row, self.gtk_table.get_row(tree_iter))

        # Get the Gtk.TreePath of the Gtk.TreeIter
        path = self.gtk_table.store.get_path(tree_iter)

        # Make sure it's the correct Gtk.TreePath
        self.assertTrue(isinstance(path, Gtk.TreePath))
        self.assertEqual(str(path), str(INSERTED_AT))
        self.assertEqual(tuple(path), (INSERTED_AT,))
        self.assertEqual(path, Gtk.TreePath(INSERTED_AT))

        # Make sure the row got stored correctly
        result_row = self.gtk_table.store[path]
        self.assertEqual(tuple(result_row), row_data)

    def test_remove(self):
        # Insert a row
        row = self.table.data.insert(0, "1", "2")

        # Make sure it's in there
        self.assertTrue(row in self.gtk_table.rows)

        # Then remove it
        self.gtk_table.remove(row)

        # Make sure its gone
        self.assertFalse(row in self.gtk_table.rows)

    def test_change(self):
        # Insert a row
        row = self.table.data.insert(0, "1", "2")

        # Make sure it's in there
        self.assertTrue(row in self.gtk_table.rows)

        # Change a column
        row.one = "something_changed"
        # (not testing that self.gtk_table.change is called. The Core API
        # unit tests should ensure this already.)

        # Get the Gtk.TreeIter
        tree_iter = self.gtk_table.rows[row]

        # Make sure it's a Gtk.TreeIter
        self.assertTrue(isinstance(tree_iter, Gtk.TreeIter))

        # Make sure it's the correct Gtk.TreeIter
        self.assertEqual(row, self.gtk_table.get_row(tree_iter))

        # Make sure the value changed
        path = self.gtk_table.store.get_path(tree_iter)
        result_row = self.gtk_table.store[path]
        self.assertEqual(tuple(result_row), (row.one, row.two))

    def test_method_get_row(self):
        # Put data in the Table
        self.table.table = []
        A = self.table.data.append(None, one="A1", two="A2")
        tree_iter = self.gtk_table.rows[A]
        self.assertEqual(A, self.gtk_table.get_row(tree_iter))

        with self.assertRaises(TypeError):
            self.gtk_table.get_row(None)

    def test_row_persisence(self):
        A = self.table.data.insert(0, one="A1", two="A2")
        B = self.table.data.insert(0, one="B1", two="B2")

        # B should now precede A
        # tests passes if A "knows" it has moved to index 1

        self.assertEqual(tuple(self.gtk_table.store[0]), ("B1", "B2"))
        self.assertEqual(tuple(self.gtk_table.store[1]), ("A1", "A2"))

    def test_on_select_root_row(self):
        # Insert two dummy rows
        self.table.data = []
        A = self.table.data.append(None, one="A1", two="A2")
        B = self.table.data.append(None, one="B1", two="B2")

        # Create a flag
        succeed = False

        def on_select(table, row, *kw):
            # Make sure the right row was selected
            self.assertEqual(row, B)

            nonlocal succeed
            succeed = True

        self.table.on_select = on_select

        # Select row B
        self.gtk_table.selection.select_path(1)

        # Allow on_select to call
        handle_events()

        self.assertTrue(succeed)

    def test_on_select_child_row(self):
        # Insert two nodes
        self.table.data = []
        A = self.table.data.append(None, one="A1", two="A2")
        B = self.table.data.append(A, one="B1", two="B2")

        # Create a flag
        succeed = False

        def on_select(able, row, *kw):
            # Make sure the right node was selected
            self.assertEqual(row, B)

            nonlocal succeed
            succeed = True

        self.table.on_select = on_select

        # Select node B
        self.gtk_table.selection.select_iter(self.gtk_table.rows[B])

        # Allow on_select to call
        handle_events()

        self.assertTrue(succeed)

    def test_on_select_deleted_node(self):
        # Insert two nodes
        self.table.data = []
        A = self.table.data.append(None, one="A1", two="A2")
        B = self.table.data.append(None, one="B1", two="B2")

        # Create a flag
        succeed = False

        def on_select(table, row):
            nonlocal succeed
            if row is not None:
                # Make sure the right row was selected
                self.assertEqual(row, B)

                # Remove row B. This should trigger on_select again
                table.data.remove(row)
            else:
                self.assertEqual(row, None)
                succeed = True

        self.table.on_select = on_select

        # Select row B
        self.gtk_table.selection.select_iter(self.gtk_table.rows[B])

        # Allow on_select to call
        handle_events()

        self.assertTrue(succeed)
