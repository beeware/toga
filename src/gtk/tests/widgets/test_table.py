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
class TestGtkTable(unittest.TestCase):
    def setUp(self):
        self.table = toga.Table(
            headings=("one", "two")
        )

        # make a shortcut for easy use
        self.gtk_table = self.table._impl

        self.window = Gtk.Window()
        self.window.add(self.table._impl.native)

    def assertRowEqual(self, row, data):
        self.assertEqual(tuple(row)[1:], data)

    def test_change_source(self):
        # Clear the table directly
        self.gtk_table.clear()

        # Assign pre-constructed data
        self.table.data = [
            ("A1", "A2"),
            ("B1", "B2")
        ]

        # Make sure the data was stored correctly
        store = self.gtk_table.store
        self.assertRowEqual(store[0], ("A1", "A2"))
        self.assertRowEqual(store[1], ("B1", "B2"))

        # Clear the table with empty assignment
        self.table.data = []

        # Make sure the table is empty
        self.assertEqual(len(store), 0)

        # Repeat with a few different cases
        self.table.data = None
        self.assertEqual(len(store), 0)

        self.table.data = ()
        self.assertEqual(len(store), 0)

    def test_insert(self):
        listener = TreeModelListener(self.gtk_table.store)

        # Insert a row
        row_data = ("1", "2")
        INSERTED_AT = 0
        row = self.table.data.insert(INSERTED_AT, *row_data)

        # Make sure it's in there
        self.assertIsNotNone(listener.inserted_it)

        # Get the Gtk.TreeIter
        tree_iter = listener.inserted_it

        # Make sure it's a Gtk.TreeIter
        self.assertTrue(isinstance(tree_iter, Gtk.TreeIter))

        # Make sure it's the correct Gtk.TreeIter
        self.assertEqual(row, self.gtk_table.store.get(tree_iter, 0)[0])

        # Get the Gtk.TreePath of the Gtk.TreeIter
        path = self.gtk_table.store.get_path(tree_iter)

        # Make sure it's the correct Gtk.TreePath
        self.assertTrue(isinstance(path, Gtk.TreePath))
        self.assertEqual(str(path), str(INSERTED_AT))
        self.assertEqual(tuple(path), (INSERTED_AT,))
        self.assertEqual(path, Gtk.TreePath(INSERTED_AT))
        self.assertEqual(path, listener.inserted_path)

        # Make sure the row got stored correctly
        result_row = self.gtk_table.store[path]
        self.assertRowEqual(result_row, row_data)

    def test_remove(self):
        listener = TreeModelListener(self.gtk_table.store)
        # Insert a row
        row = self.table.data.insert(0, "1", "2")

        # Make sure it's in there
        self.assertIsNotNone(listener.inserted_it)

        # Then remove it
        self.gtk_table.remove(index=0, item=row)

        # Make sure its gone
        self.assertIsNotNone(listener.deleted_path)

    def test_change(self):
        listener = TreeModelListener(self.gtk_table.store)

        # Insert a row
        row = self.table.data.insert(0, "1", "2")

        # Make sure it's in there
        self.assertIsNotNone(listener.inserted_it)

        # Change a column
        row.one = "something_changed"
        # (not testing that self.gtk_table.change is called. The Core API
        # unit tests should ensure this already.)

        # Get the Gtk.TreeIter
        tree_iter = listener.changed_it

        # Make sure it's a Gtk.TreeIter
        self.assertTrue(isinstance(tree_iter, Gtk.TreeIter))

        # Make sure it's the correct Gtk.TreeIter
        self.assertEqual(row, self.gtk_table.store.get(tree_iter, 0)[0])

        # Make sure the value changed
        path = self.gtk_table.store.get_path(tree_iter)
        result_row = self.gtk_table.store[path]
        self.assertRowEqual(result_row, (row.one, row.two))

    def test_row_persistence(self):
        self.table.data.insert(0, one="A1", two="A2")
        self.table.data.insert(0, one="B1", two="B2")

        # B should now precede A
        # tests passes if A "knows" it has moved to index 1

        self.assertRowEqual(self.gtk_table.store[0], ("B1", "B2"))
        self.assertRowEqual(self.gtk_table.store[1], ("A1", "A2"))

    def test_on_select_root_row(self):
        # Insert two dummy rows
        self.table.data = []
        self.table.data.append(None, one="A1", two="A2")
        b = self.table.data.append(None, one="B1", two="B2")

        # Create a flag
        succeed = False

        def on_select(table, row, *kw):
            # Make sure the right row was selected
            self.assertEqual(row, b)

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

        listener = TreeModelListener(self.gtk_table.store)

        a = self.table.data.append(None, one="A1", two="A2")
        b = self.table.data.append(a, one="B1", two="B2")

        # Create a flag
        succeed = False

        def on_select(able, row, *kw):
            # Make sure the right node was selected
            self.assertEqual(row, b)

            nonlocal succeed
            succeed = True

        self.table.on_select = on_select

        # Select node B
        self.gtk_table.selection.select_iter(listener.inserted_it)

        # Allow on_select to call
        handle_events()

        self.assertTrue(succeed)

    def test_on_select_deleted_node(self):
        # Insert two nodes
        self.table.data = []

        listener = TreeModelListener(self.gtk_table.store)

        self.table.data.append(None, one="A1", two="A2")
        listener.clear()
        b = self.table.data.append(None, one="B1", two="B2")

        # Create a flag
        succeed = False

        def on_select(table, row):
            nonlocal succeed
            if row is not None:
                # Make sure the right row was selected
                self.assertEqual(row, b)

                # Remove row B. This should trigger on_select again
                table.data.remove(row)
            else:
                self.assertEqual(row, None)
                succeed = True

        self.table.on_select = on_select

        # Select row B
        self.gtk_table.selection.select_iter(listener.inserted_it)

        # Allow on_select to call
        handle_events()

        self.assertTrue(succeed)
