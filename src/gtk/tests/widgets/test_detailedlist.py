import os
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


def handle_events():
    while Gtk.events_pending():
        Gtk.main_iteration_do(blocking=False)


@unittest.skipIf(Gtk is None, "Can't run GTK implementation tests on a non-Linux platform")
class TestGtkDetailedList(unittest.TestCase):
    def setUp(self):
        icon = toga.Icon(os.path.join(os.path.dirname(__file__), '../../../../demo/toga_demo/resources/brutus-32.png'))
        self.dl = toga.DetailedList([
            dict(icon=icon, title='Item %i' % i, subtitle='this is the subtitle for item %i' % i)
            for i in range(10)
        ])

        # make a shortcut for easy use
        self.gtk_dl = self.dl._impl

        self.window = Gtk.Window()
        self.window.add(self.dl._impl.native)

    def assertRowEqual(self, row, data):
        for attr in ('icon', 'title', 'subtitle'):
            self.assertEqual(getattr(row, attr), data[attr])

    def test_change_source(self):
        # Clear the table directly
        self.gtk_dl.clear()

        # Assign pre-constructed data
        a = dict(icon=None, title='A', subtitle='a subtitle')
        b = dict(icon=None, title='B', subtitle='b subtitle')

        self.dl.data = [a, b]

        # Make sure the data was stored correctly
        store = self.gtk_dl.store
        self.assertRowEqual(store[0], a)
        self.assertRowEqual(store[1], b)

        # Clear the table with empty assignment
        self.dl.data = []

        # Make sure the table is empty
        self.assertEqual(len(store), 0)

        # Repeat with a few different cases
        self.dl.data = None
        self.assertEqual(len(store), 0)

        self.dl.data = ()
        self.assertEqual(len(store), 0)

    def test_insert(self):
        # Insert a row
        row_data = dict(icon=None, title='A', subtitle='a subtitle')

        INSERTED_AT = 0
        self.dl.data.insert(INSERTED_AT, **row_data)

        # Make sure it's in there
        self.assertEqual(len(self.gtk_dl.store), 1)

        # Make sure the row got stored correctly
        result_row = self.gtk_dl.store[INSERTED_AT]
        self.assertRowEqual(result_row, row_data)

    def test_remove(self):
        # Insert a row
        row_data = dict(icon=None, title='1', subtitle='2')

        INSERTED_AT = 0
        row = self.dl.data.insert(INSERTED_AT, **row_data)

        # Make sure it's in there
        self.assertEqual(len(self.gtk_dl.store), 1)

        # Then remove it
        self.gtk_dl.remove(row, index=INSERTED_AT)

        # Make sure its gone
        self.assertIsNone(self.gtk_dl.store.get_item(INSERTED_AT))

    def test_change(self):
        # Insert a row
        row_data = dict(icon=None, title='1', subtitle='2')

        INSERTED_AT = 0
        row = self.dl.data.insert(INSERTED_AT, **row_data)

        # Make sure it's in there
        self.assertEqual(len(self.gtk_dl.store), 1)

        # Change a column
        row.title = "something changed"
        # (not testing that self.gtk_dl.change is called. The Core API
        # unit tests should ensure this already.)

        # Make sure the value changed
        result_row = self.gtk_dl.store[INSERTED_AT]
        self.assertRowEqual(result_row, dict(icon=None, title="something changed", subtitle="2"))

        # Make sure the row was replaced and not appended
        self.assertEqual(len(self.gtk_dl.store), 1)

    def test_row_persistence(self):
        self.dl.data.insert(0, icon=None, title="A1", subtitle="A2")
        self.dl.data.insert(0, icon=None, title="B1", subtitle="B2")

        # B should now precede A
        # tests passes if A "knows" it has moved to index 1

        self.assertRowEqual(self.gtk_dl.store[0], dict(icon=None, title="B1", subtitle="B2"))
        self.assertRowEqual(self.gtk_dl.store[1], dict(icon=None, title="A1", subtitle="A2"))

    def test_on_select_row(self):
        # Insert two dummy rows
        self.dl.data = []
        self.dl.data.append(None, icon=None, title="A1", subtitle="A2")
        b = self.dl.data.append(None, icon=None, title="B1", subtitle="B2")

        # Create a flag
        succeed = False

        def on_select(table, row, *kw):
            # Make sure the right row was selected
            self.assertEqual(row, b)

            nonlocal succeed
            succeed = True

        self.dl.on_select = on_select

        # Select row B
        self.gtk_dl.list_box.select_row(
            self.gtk_dl.list_box.get_row_at_index(1))

        # Allow on_select to call
        handle_events()

        self.assertTrue(succeed)

    def test_on_select_deleted_node(self):
        # Insert two nodes
        self.dl.data = []

        self.dl.data.append(None, icon=None, title="A1", subtitle="A2")
        b = self.dl.data.append(None,  icon=None, title="B1", subtitle="B2")

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

        self.dl.on_select = on_select

        # Select row B
        self.gtk_dl.list_box.select_row(b._impl)

        # Allow on_select to call
        handle_events()

        self.assertTrue(succeed)
