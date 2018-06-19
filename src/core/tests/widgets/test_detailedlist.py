import toga
import toga_dummy
from toga.sources import ListSource
from toga_dummy.utils import TestCase


class TestDetailedList(TestCase):
    def setUp(self):
        super().setUp()

        self.on_select = None
        self.on_delete = None
        self.on_refresh = None

        self.dlist = toga.DetailedList(factory=toga_dummy.factory,
                                       on_select=self.on_select,
                                       on_delete=self.on_delete,
                                       on_refresh=self.on_refresh)

    def test_widget_created(self):
        self.assertEqual(self.dlist._impl.interface, self.dlist)
        self.assertActionPerformed(self.dlist, 'create DetailedList')

    def test_detailedlist_property(self):
        test_list = ["test1", "test2", " "]
        self.dlist.data = test_list
        listsource_list = ListSource(data=test_list, accessors=['icon', 'label1', 'label2'])
        for i in range(len(self.dlist.data)):
            self.assertEqual(self.dlist.data[i]._attrs, listsource_list[i]._attrs)

        test_tuple = ("ttest1", "ttest2", " ")
        self.dlist.data = test_tuple
        listsource_tuple = ListSource(data=test_tuple, accessors=['icon', 'label1', 'label2'])
        for i in range(len(self.dlist.data)):
            self.assertEqual(self.dlist.data[i]._attrs, listsource_tuple[i]._attrs)

        self.dlist.data = listsource_list
        for i in range(len(self.dlist.data)):
            self.assertEqual(self.dlist.data[i]._attrs, listsource_list[i]._attrs)

    def test_scroll_to_row(self):
        test_list = ["test1", "test2", "test3", " "]
        self.dlist.data = test_list
        self.dlist.scroll_to_row(2)
        self.assertValueSet(self.dlist, 'scroll to', 2)

    def test_scroll_to_top(self):
        test_list = ["test1", "test2", "test3", " "]
        self.dlist.data = test_list
        self.dlist.scroll_to_top()
        self.assertValueSet(self.dlist, 'scroll to', 0)

    def test_scroll_to_bottom(self):
        test_list = ["test1", "test2", "test3", " "]
        self.dlist.data = test_list
        self.dlist.scroll_to_bottom()
        self.assertValueSet(self.dlist, 'scroll to', len(self.dlist.data) - 1)
