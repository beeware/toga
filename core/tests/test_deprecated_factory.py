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

    def test_app(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.App(
                formal_name="Test", app_id="org.beeware.test-app", factory=self.factory
            )
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_document_app(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.DocumentApp(
                formal_name="Test", app_id="org.beeware.test-app", factory=self.factory
            )
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_main_window(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.MainWindow(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_command(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Command(self.callback, "Test", factory=self.factory)
        with self.assertWarns(DeprecationWarning):
            widget.bind(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_command_set(self):
        with self.assertWarns(DeprecationWarning):
            toga.CommandSet(factory=self.factory)

    def test_font(self):
        widget = toga.Font(SANS_SERIF, 14)
        with self.assertWarns(DeprecationWarning):
            widget.bind(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_icon(self):
        widget = toga.Icon("resources/toga", system=True)
        with self.assertWarns(DeprecationWarning):
            widget.bind(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_window(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Window(factory=self.factory)
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

    def test_option_container_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.OptionContainer(factory=self.factory)
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
