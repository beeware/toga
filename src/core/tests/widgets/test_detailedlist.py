import toga
import toga_dummy
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
