from unittest.mock import Mock

from toga.widgets_registry import WidgetsRegistry
from toga_dummy.utils import TestCase


def widget_mock(id):
    widget = Mock()
    widget.id = id
    widget.__repr__ = Mock(return_value=f"Widget(id={id})")
    return widget


class TestWidgetsRegistry(TestCase):

    def setUp(self):
        super().setUp()
        self.widgets_registry = WidgetsRegistry()

    def test_empty_registry(self):
        self.assertEqual(len(self.widgets_registry), 0)
        self.assertEqual(list(self.widgets_registry), [])
        self.assertEqual(str(self.widgets_registry), "{}")

    def test_add_widget(self):
        id1 = 1234
        widget = widget_mock(id1)
        self.widgets_registry.add(widget)

        self.assertEqual(len(self.widgets_registry), 1)
        self.assertEqual(list(self.widgets_registry), [widget])
        self.assertEqual(str(self.widgets_registry), "{1234: Widget(id=1234)}")
        self.assertEqual(self.widgets_registry[id1], widget)

    def test_add_two_widgets(self):
        id1, id2 = 1234, 6789
        widget1, widget2 = widget_mock(id1), widget_mock(id2)
        self.widgets_registry.add(widget1)
        self.widgets_registry.add(widget2)

        self.assertEqual(len(self.widgets_registry), 2)
        self.assertEqual(set(self.widgets_registry), {widget1, widget2})
        self.assertEqual(self.widgets_registry[id1], widget1)
        self.assertEqual(self.widgets_registry[id2], widget2)

    def test_extend_widgets(self):
        id1, id2, id3 = 1234, 6789, 9821
        widget1, widget2, widget3 = widget_mock(id1), widget_mock(id2), widget_mock(id3)
        self.widgets_registry.extend(widget1, widget2, widget3)

        self.assertEqual(len(self.widgets_registry), 3)
        self.assertEqual(set(self.widgets_registry), {widget1, widget2, widget3})
        self.assertEqual(self.widgets_registry[id1], widget1)
        self.assertEqual(self.widgets_registry[id2], widget2)
        self.assertEqual(self.widgets_registry[id3], widget3)

    def test_remove_widget(self):
        id1, id2, id3 = 1234, 6789, 9821
        widget1, widget2, widget3 = widget_mock(id1), widget_mock(id2), widget_mock(id3)
        self.widgets_registry.extend(widget1, widget2, widget3)
        self.widgets_registry.remove(id2)

        self.assertEqual(len(self.widgets_registry), 2)
        self.assertEqual(set(self.widgets_registry), {widget1, widget3})
        self.assertEqual(self.widgets_registry[id1], widget1)
        self.assertEqual(self.widgets_registry[id3], widget3)

    def test_add_same_widget_twice(self):
        id1 = 1234
        widget = widget_mock(id1)
        self.widgets_registry.add(widget)
        self.assertRaises(KeyError, self.widgets_registry.add, widget)

        self.assertEqual(len(self.widgets_registry), 1)
        self.assertEqual(list(self.widgets_registry), [widget])
        self.assertEqual(str(self.widgets_registry), "{1234: Widget(id=1234)}")
        self.assertEqual(self.widgets_registry[id1], widget)

    def test_two_widgets_with_same_name(self):
        id1 = 1234
        widget1, widget2 = widget_mock(id1), widget_mock(id1)
        self.widgets_registry.add(widget1)
        self.assertRaises(KeyError, self.widgets_registry.add, widget2)

        self.assertEqual(len(self.widgets_registry), 1)
        self.assertEqual(list(self.widgets_registry), [widget1])
        self.assertEqual(str(self.widgets_registry), "{1234: Widget(id=1234)}")
        self.assertEqual(self.widgets_registry[id1], widget1)
