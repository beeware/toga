import toga
import toga_dummy
from toga.sources import ListSource, Source
from toga_dummy.utils import TestCase


class CustomSource(Source):
    pass


class TableTests(TestCase):
    def setUp(self):
        super().setUp()

        self.headings = ['Heading 1', 'Heading 2', 'Heading 3']

        def select_handler(widget, row):
            pass

        self.on_select = select_handler

        self.table = toga.Table(
            self.headings,
            on_select=self.on_select,
            factory=toga_dummy.factory
        )

    def test_widget_created(self):
        self.assertEqual(self.table._impl.interface, self.table)
        self.assertActionPerformed(self.table, 'create Table')

        self.assertEqual(self.table.headings, self.headings)
        self.assertIsInstance(self.table.data, ListSource)

    def test_list_of_lists_data_source(self):
        self.table.data = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
        ]

        self.assertIsInstance(self.table.data, ListSource)

    def test_custom_data_source(self):
        data_source = CustomSource()
        self.table.data = data_source
        self.assertIs(self.table.data, data_source)

    def test_nothing_selected(self):
        self.assertEqual(self.table.selection, None)

    def test_scroll_to_row(self):
        self.table.data = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3'],
            ['a4', 'b3', 'c4']
        ]
        self.table.scroll_to_row(2)
        self.assertValueSet(self.table, 'scroll to', 2)

    def test_scroll_to_top(self):
        self.table.data = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3'],
            ['a4', 'b3', 'c4']
        ]
        self.table.scroll_to_top()
        self.assertValueSet(self.table, 'scroll to', 0)

    def test_scroll_to_bottom(self):
        self.table.data = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3'],
            ['a4', 'b3', 'c4']
        ]
        self.table.scroll_to_bottom()
        self.assertValueSet(self.table, 'scroll to', len(self.table.data) - 1)

    def test_multiple_select(self):
        self.assertEqual(self.table.multiple_select, False)
        secondtable = toga.Table(
            self.headings,
            multiple_select=True,
            factory=toga_dummy.factory
        )
        self.assertEqual(secondtable.multiple_select, True)

    def test_on_select(self):

        def dummy_handler(widget, row):
            pass

        self.assertValueSet(self.table, "on_select", self.table.on_select)

        on_sele = self.table.on_select
        self.assertEqual(on_sele._raw, self.on_select)

        self.table.on_select = dummy_handler
        on_sele = self.table.on_select
        self.assertEqual(on_sele._raw, dummy_handler)
