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
