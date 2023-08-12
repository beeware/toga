import toga
from toga.fonts import SANS_SERIF
from toga_dummy.utils import TestCase


class DeprecatedFactoryTests(TestCase):
    def setUp(self):
        super().setUp()
        self.factory = object()
        self.callback = lambda x: None

    ######################################################################
    # 2022-09: Backwards compatibility
    ######################################################################
    # factory no longer used

    def test_font(self):
        widget = toga.Font(SANS_SERIF, 14)
        with self.assertWarns(DeprecationWarning):
            widget.bind(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_canvas_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Canvas(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_detailed_list_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.DetailedList(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_table_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Table(
                headings=["Test"], missing_value="", factory=self.factory
            )
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_tree_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Tree(headings=["Test"], factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    ######################################################################
    # End backwards compatibility.
    ######################################################################
