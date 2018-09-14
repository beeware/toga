import sys
from collections import OrderedDict
import unittest
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
except ImportError:
    # If we're on Linux, Gtk *should* be available. If it isn't, make
    # Gtk an object... but in such a way that every test will fail,
    # because the object isn't actually the Gtk interface.
    if sys.platform == 'linux':
        Gtk = object()
    else:
        Gtk = None

from toga_gtk.libs.utils import generate_css, gtk_apply_css


class TestGenerateCSSMethod(unittest.TestCase):
    def setUp(self):
        self.single_line_property = {'color': '#f00'}  # Red
        self.multi_line_property = {
            'font-family': 'sans',
            'font-size': '12px',
            'font-style': 'italic',
        }

        # Use OrderedDict for Python < 3.6
        if sys.version_info < (3, 6):
            d = OrderedDict()
            d['font-family'] = self.multi_line_property['font-family']
            d['font-size'] = self.multi_line_property['font-size']
            d['font-style'] = self.multi_line_property['font-style']
            self.multi_line_property = d

    def test_single_selectors_with_single_line_property(self):
        expected = 'button {\n\tcolor: #f00;\n}'
        got = generate_css('button', self.single_line_property)
        self.assertEqual(expected, got)

    def test_single_selector_with_multi_line_property(self):
        expected = 'button {\n\tfont-family: sans;\n\tfont-size: 12px;\n\tfont-style: italic;\n}'
        got = generate_css('button', self.multi_line_property)
        self.assertEqual(expected, got)

    def test_compound_selectors_with_single_line_property(self):
        expected = 'button, entry {\n\tcolor: #f00;\n}'
        got = generate_css('button, entry', self.single_line_property)
        self.assertEqual(expected, got)

    def test_compound_selector_with_multi_line_property(self):
        expected = 'button, entry {\n\tfont-family: sans;\n\tfont-size: 12px;\n\tfont-style: italic;\n}'
        got = generate_css('button, entry', self.multi_line_property)
        self.assertEqual(expected, got)

    def test_descend_selectors_with_single_line_property(self):
        expected = 'window label {\n\tcolor: #f00;\n}'
        got = generate_css('window label', self.single_line_property)
        self.assertEqual(expected, got)

    def test_descend_selector_with_multi_line_property(self):
        expected = 'window label {\n\tfont-family: sans;\n\tfont-size: 12px;\n\tfont-style: italic;\n}'
        got = generate_css('window label', self.multi_line_property)
        self.assertEqual(expected, got)

    def test_any_child_selectors_with_single_line_property(self):
        expected = 'box * {\n\tcolor: #f00;\n}'
        got = generate_css('box *', self.single_line_property)
        self.assertEqual(expected, got)

    def test_any_child_selector_with_multi_line_property(self):
        expected = 'box * {\n\tfont-family: sans;\n\tfont-size: 12px;\n\tfont-style: italic;\n}'
        got = generate_css('box *', self.multi_line_property)
        self.assertEqual(expected, got)

    def test_empty_selector_raises_value_error(self):
        with self.assertRaises(ValueError):
            generate_css('', self.single_line_property)

    def test_empty_property_raises_value_error(self):
        with self.assertRaises(ValueError):
            generate_css('button', {})


@unittest.skipIf(Gtk is None,
                 "Can't run GTK implementation tests on a non-Linux platform")
class TestGTKApplyCSSMethod(unittest.TestCase):
    def setUp(self):
        self.widget = Gtk.Button()  # Any example widget
        self.style_context = self.widget.get_style_context()
        self.state = self.widget.get_state_flags()

    def test_can_apply_valid_css(self):
        # Checks if a color can be applied to the widget
        gtk_apply_css(self.widget, {'color': '#0ff'})
        final = self.style_context.get_color(self.state)
        self.assertEqual(final,
                         Gdk.RGBA(red=0.0, green=1.0, blue=1.0, alpha=1.0))


if __name__ == '__main__':
    unittest.main()
