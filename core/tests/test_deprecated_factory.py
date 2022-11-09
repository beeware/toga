import toga
import toga_dummy
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

    def test_image(self):
        resource_path = toga_dummy.factory.paths.toga
        image = toga.Image(resource_path / "resources/toga.png")
        with self.assertWarns(DeprecationWarning):
            image.bind(factory=self.factory)
        self.assertEqual(image._impl.interface, image)

    def test_window(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Window(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_activity_indicator(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.ActivityIndicator(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_box_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Box(children=[toga.Widget()], factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_button_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Button("Test", factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_canvas_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Canvas(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_date_picker_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.DatePicker(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_detailed_list_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.DetailedList(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_divider_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Divider(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_image_view_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.ImageView(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_label_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Label("Test", factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_multiline_text_input_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.MultilineTextInput(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_number_input_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.NumberInput(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_option_container_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.OptionContainer(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_progress_bar_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.ProgressBar(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_scroll_container_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.ScrollContainer(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_selection_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Selection(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_slider_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Slider(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_split_container_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.SplitContainer(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_switch_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Switch("Test", factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_table_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Table(
                headings=["Test"], missing_value="", factory=self.factory
            )
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_text_input_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.TextInput(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_time_picker_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.TimePicker(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_tree_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.Tree(headings=["Test"], factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    def test_web_view_created(self):
        with self.assertWarns(DeprecationWarning):
            widget = toga.WebView(factory=self.factory)
        self.assertEqual(widget._impl.interface, widget)
        self.assertNotEqual(widget.factory, self.factory)

    ######################################################################
    # End backwards compatibility.
    ######################################################################
