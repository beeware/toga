import toga
import toga_dummy
from toga_dummy.utils import TestCase
from toga.sources import TreeSource, Source

class TreeTests(TestCase):
    def setUp(self):
        super().setUp()

        self.headings = ['Heading {}'.format(x) for x in range(3)]

        self.data = None
        self.tree = toga.Tree(headings=self.headings,
                              data=self.data,
                              factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.tree._impl.interface, self.tree)
        self.assertActionPerformed(self.tree, 'create Tree')
        self.assertIsInstance(self.tree.data, TreeSource)

        self.assertEqual(self.tree.headings, self.headings)

    def test_setter_creates_tree_with_dict_data(self):
        self.data = {
            ('first', 111): None,
            ('second', 222): [],
            ('third', 333): [
                ('third.one', 331),
                {'heading_0': 'third.two', 'heading_1': 332}
            ]
        }
        self.tree.data = self.data

        self.assertIsInstance(self.tree.data, TreeSource)
        self.assertFalse(self.tree.data[0].can_have_children())
        self.assertTrue(self.tree.data[1].can_have_children())
        self.assertEqual(self.tree.data[1].heading_1, 222)
        self.assertEqual(self.tree.data[2][0].heading_1, 331)

    def test_data_setter_creates_tree_with_tuple_data(self):
        pass

    def test_data_setter_creates_tree_with_list_data(self):
        pass

    def test_data_setter_creates_tree_with_data_source(self):
        pass

    def test_data_setter_creates_tree_with_data_none(self):
        pass

    def test_data_with_treesource(self):
        self.data = {
            ('first', 111): None,
            ('second', 222): [],
            ('third', 333): [
                ('third.one', 331),
                {'heading_0': 'third.two', 'heading_1': 332}
            ]
        }
        self.tree.data = TreeSource(accessors=self.tree._accessors, data=self.data)

    def test_multiple_select(self):
        self.assertEqual(self.tree.multiple_select, False)
        self.tree.multiple_select = True
        self.assertEqual(self.tree.multiple_select, True)

    def test_nothing_selected(self):
        self.assertIsNone(self.tree.selection)

    def test_on_select(self):
        self.assertIsNone(self.tree._on_select)

        # set a new callback
        def callback(widget, **extra):
            return 'called {} with {}'.format(type(widget), extra)

        self.tree.on_select = callback
        self.assertEqual(self.tree.on_select._raw, callback)
        self.assertEqual(
            self.tree.on_select('widget', a=1),
            "called <class 'toga.widgets.tree.Tree'> with {'a': 1}"
        )
        self.assertValueSet(self.tree, 'on_select', self.tree.on_select)
