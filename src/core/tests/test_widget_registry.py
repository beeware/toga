from unittest.mock import Mock

from toga.widgets.base import WidgetRegistry
from toga_dummy.utils import TestCase


def widget_mock(id):
    widget = Mock()
    widget.id = id
    widget.__repr__ = Mock(return_value=f"Widget(id={id})")
    return widget


class TestWidgetsRegistry(TestCase):
    def setUp(self):
        super().setUp()
        self.widget_registry = WidgetRegistry()

    def test_empty_registry(self):
        self.assertEqual(len(self.widget_registry), 0)
        self.assertEqual(list(self.widget_registry), [])
        self.assertEqual(str(self.widget_registry), "{}")

    def test_add_widget(self):
        id1 = 1234
        widget = widget_mock(id1)
        self.widget_registry.add(widget)

        self.assertEqual(len(self.widget_registry), 1)
        self.assertEqual(list(self.widget_registry), [widget])
        self.assertEqual(str(self.widget_registry), "{1234: Widget(id=1234)}")
        self.assertEqual(self.widget_registry[id1], widget)

    def test_add_two_widgets(self):
        id1, id2 = 1234, 6789
        widget1, widget2 = widget_mock(id1), widget_mock(id2)
        self.widget_registry.add(widget1)
        self.widget_registry.add(widget2)

        self.assertEqual(len(self.widget_registry), 2)
        self.assertEqual(set(self.widget_registry), {widget1, widget2})
        self.assertEqual(self.widget_registry[id1], widget1)
        self.assertEqual(self.widget_registry[id2], widget2)

    def test_update_widgets(self):
        id1, id2, id3 = 1234, 6789, 9821
        widget1, widget2, widget3 = widget_mock(id1), widget_mock(id2), widget_mock(id3)
        self.widget_registry.update({widget1, widget2, widget3})

        self.assertEqual(len(self.widget_registry), 3)
        self.assertEqual(set(self.widget_registry), {widget1, widget2, widget3})
        self.assertEqual(self.widget_registry[id1], widget1)
        self.assertEqual(self.widget_registry[id2], widget2)
        self.assertEqual(self.widget_registry[id3], widget3)

    def test_remove_widget(self):
        id1, id2, id3 = 1234, 6789, 9821
        widget1, widget2, widget3 = widget_mock(id1), widget_mock(id2), widget_mock(id3)
        self.widget_registry.update({widget1, widget2, widget3})
        self.widget_registry.remove(id2)

        self.assertEqual(len(self.widget_registry), 2)
        self.assertEqual(set(self.widget_registry), {widget1, widget3})
        self.assertEqual(self.widget_registry[id1], widget1)
        self.assertEqual(self.widget_registry[id3], widget3)

    def test_add_same_widget_twice(self):
        id1 = 1234
        widget = widget_mock(id1)
        self.widget_registry.add(widget)
        self.assertRaises(KeyError, self.widget_registry.add, widget)

        self.assertEqual(len(self.widget_registry), 1)
        self.assertEqual(list(self.widget_registry), [widget])
        self.assertEqual(str(self.widget_registry), "{1234: Widget(id=1234)}")
        self.assertEqual(self.widget_registry[id1], widget)

    def test_two_widgets_with_same_name(self):
        id1 = 1234
        widget1, widget2 = widget_mock(id1), widget_mock(id1)
        self.widget_registry.add(widget1)
        self.assertRaises(KeyError, self.widget_registry.add, widget2)

        self.assertEqual(len(self.widget_registry), 1)
        self.assertEqual(list(self.widget_registry), [widget1])
        self.assertEqual(str(self.widget_registry), "{1234: Widget(id=1234)}")
        self.assertEqual(self.widget_registry[id1], widget1)

    def test_using_setitem_directly(self):
        id1 = 1234
        widget = widget_mock(id1)
        self.assertRaises(RuntimeError, self.widget_registry.__setitem__, id1, widget)
