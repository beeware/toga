import toga
import toga_dummy
from toga.sources import ListSource, Source
from toga_dummy.utils import TestCase


class CustomSource(Source):
    pass


class TableTests(TestCase):
    def setUp(self):
        super().setUp()

        self.headings = ["Heading 1", "Heading 2", "Heading 3"]
        self.accessors = ["heading_1", "heading_2", "heading_3"]

        def select_handler(widget, row):
            pass

        def double_click_handler(widget, row):
            pass

        self.on_select = select_handler
        self.on_double_click = double_click_handler

        self.table = toga.Table(
            columns=self.headings,
            on_select=self.on_select,
            on_double_click=self.on_double_click,
            factory=toga_dummy.factory,
        )

    def test_widget_created(self):
        self.assertEqual(self.table._impl.interface, self.table)
        self.assertActionPerformed(self.table, "create Table")

        col_titles = [col.title for col in self.table.columns]
        self.assertEqual(col_titles, self.headings)
        self.assertIsInstance(self.table.data, ListSource)

    def test_list_of_lists_data_source(self):
        data = [
            ["a1", "b1", "c1"],
            ["a2", "b2", "c2"],
        ]

        self.table.data = ListSource(data, self.accessors)
        self.assertIsInstance(self.table.data, ListSource)

    def test_custom_data_source(self):
        data_source = CustomSource()
        self.table.data = data_source
        self.assertIs(self.table.data, data_source)

    def test_nothing_selected(self):
        self.assertEqual(self.table.selection, None)

    def test_scroll_to_row(self):
        data = [
            ["a1", "b1", "c1"],
            ["a2", "b2", "c2"],
            ["a3", "b3", "c3"],
            ["a4", "b3", "c4"],
        ]
        self.table.data = ListSource(data, self.accessors)
        self.table.scroll_to_row(2)
        self.assertValueSet(self.table, "scroll to", 2)

    def test_scroll_to_top(self):
        data = [
            ["a1", "b1", "c1"],
            ["a2", "b2", "c2"],
            ["a3", "b3", "c3"],
            ["a4", "b3", "c4"],
        ]
        self.table.data = ListSource(data, self.accessors)
        self.table.scroll_to_top()
        self.assertValueSet(self.table, "scroll to", 0)

    def test_scroll_to_bottom(self):
        data = [
            ["a1", "b1", "c1"],
            ["a2", "b2", "c2"],
            ["a3", "b3", "c3"],
            ["a4", "b3", "c4"],
        ]
        self.table.data = ListSource(data, self.accessors)
        self.table.scroll_to_bottom()
        self.assertValueSet(self.table, "scroll to", len(self.table.data) - 1)

    def test_multiple_select(self):
        self.assertEqual(self.table.multiple_select, False)
        secondtable = toga.Table(
            self.headings, multiple_select=True, factory=toga_dummy.factory
        )
        self.assertEqual(secondtable.multiple_select, True)

    def test_on_select(self):
        def dummy_handler(widget, row):
            pass

        self.assertValueSet(self.table, "on_select", self.table.on_select)

        on_select = self.table.on_select
        self.assertEqual(on_select._raw, self.on_select)

        self.table.on_select = dummy_handler
        on_select = self.table.on_select
        self.assertEqual(on_select._raw, dummy_handler)

    def test_on_double_click(self):
        def dummy_handler(widget, row):
            pass

        self.assertValueSet(self.table, "on_double_click", self.table.on_double_click)

        on_double_click = self.table.on_double_click
        self.assertEqual(on_double_click._raw, self.on_double_click)

        self.table.on_double_click = dummy_handler
        on_double_click = self.table.on_double_click
        self.assertEqual(on_double_click._raw, dummy_handler)

    def test_add_column(self):
        new_column = toga.Table.Column("Heading 4", text="heading_4", factory=toga_dummy.factory)
        data = [
            ["a1", "b1", "c1"],
            ["a2", "b2", "c2"],
            ["a3", "b3", "c3"],
            ["a4", "b3", "c4"],
        ]
        self.table.data = ListSource(data, self.accessors)

        expecting_columns = self.table.columns + [new_column]
        self.table.add_column(new_column)

        self.assertEqual(self.table.columns, expecting_columns)

    def test_remove_column(self):
        remove = self.table.columns[-1]
        self.table.remove_column(remove)
        self.assertNotIn(remove, self.table.columns)

    def test_remove_column_invalid(self):
        new_column = toga.Table.Column("New", text="heading_24", factory=toga_dummy.factory)

        # Remove a column that doesn't exist
        with self.assertRaises(ValueError):
            self.table.remove_column(new_column)

    def test_remove_column_invalid_type(self):

        # Remove a column using a data type that isn't valid
        with self.assertRaises(ValueError):
            self.table.remove_column(3.14159)
