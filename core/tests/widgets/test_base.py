from unittest.mock import Mock

import toga
from toga.style import Pack
from toga_dummy.utils import TestCase


# Create the simplest possible widget with a concrete implementation
class Widget(toga.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._impl = self.factory.Widget(self)


class WidgetTests(TestCase):
    def setUp(self):
        super().setUp()

        self.id = "widget_id"
        self.style = Pack(padding=666)

        self.widget = Widget(
            id=self.id,
            style=self.style,
        )

    def test_arguments_were_set_correctly(self):
        self.assertEqual(self.widget.id, self.id)
        self.assertEqual(self.widget.style.padding, self.style.padding)

    def test_create_widget_with_no_style(self):
        widget = toga.Widget()
        self.assertTrue(isinstance(widget.style, Pack))

    def test_enabled_with_None(self):
        # Using a Box for test because we need a concrete implementation to use this property.
        box = toga.Box()
        box.enabled = None
        self.assertFalse(box.enabled)
        self.assertActionPerformedWith(box, "set enabled", value=None)

    def test_adding_child(self):
        self.assertIsNone(self.widget.app)
        self.assertIsNone(self.widget.window)
        self.assertEqual(
            self.widget.children, [], "No child was added, should return an empty list."
        )
        # Create a child widget to add to widget.
        child = toga.Widget()

        with self.assertRaises(ValueError, msg="Widget cannot have children."):
            self.widget.add(child)

        # Deliberately set widget._children = [] to allow it to have children.
        # Only for test purposes!
        self.widget._children = []
        self.widget.add(child)
        self.assertEqual(self.widget.children, [child])

    def test_adding_child_with_app(self):
        app = toga.App("Test App", "org.beeware.test")
        self.widget.app = app
        self.assertEqual(
            self.widget.children, [], "No child was added, should return an empty list."
        )

        # Create a child widget to add to widget.
        child_id = "child-id"
        child = Widget(id=child_id)

        # Deliberately set widget._children = [] to allow it to have children.
        # Only for test purposes!
        self.widget._children = []
        self.widget.add(child)
        self.assertEqual(self.widget.children, [child])
        self.assertEqual(self.widget.app, app)
        self.assertEqual(child.app, app)
        self.assertEqual(len(app.widgets), 2)
        self.assertEqual(app.widgets[self.id], self.widget)
        self.assertEqual(app.widgets[child_id], child)

    def test_adding_child_with_window(self):
        window = toga.Window()
        window.content = Mock()
        self.widget.window = window
        self.assertEqual(
            self.widget.children, [], "No child was added, should return an empty list."
        )

        # Create a child widget to add to widget.
        child_id = "child-id"
        child = Widget(id=child_id)

        # Deliberately set widget._children = [] to allow it to have children.
        # Only for test purposes!
        self.widget._children = []
        self.widget.add(child)
        self.assertEqual(self.widget.children, [child])
        self.assertEqual(self.widget.window, window)
        self.assertEqual(child.window, window)
        self.assertEqual(len(window.widgets), 2)
        self.assertEqual(window.widgets[self.id], self.widget)
        self.assertEqual(window.widgets[child_id], child)

    def test_adding_children(self):
        self.assertEqual(
            self.widget.children, [], "No children added, should return an empty list."
        )
        # Create 2 children to add to widget.
        child1 = toga.Widget()
        child2 = toga.Widget()

        self.widget._children = []
        self.widget.add(child1, child2)
        self.assertEqual(self.widget.children, [child1, child2])

    def test_adding_child_with_existing_parent(self):
        # Create a second parent widget.
        widget2 = toga.Widget()
        # Create a child widget to add to widget2 before adding to widget.
        child = toga.Widget()

        widget2._children = []
        widget2.add(child)
        self.assertEqual(widget2.children, [child])

        self.widget._children = []
        self.widget.add(child)
        self.assertEqual(self.widget.children, [child])
        self.assertEqual(widget2.children, [])

    def test_inserting_child_into_empty_list(self):
        self.assertEqual(
            self.widget.children,
            [],
            "No child was inserted, should return an empty list.",
        )
        # Create a child widget to insert into widget.
        child = toga.Widget()

        with self.assertRaises(ValueError, msg="Widget cannot have children."):
            self.widget.insert(0, child)

        self.widget._children = []
        self.widget.insert(0, child)
        self.assertEqual(self.widget.children, [child])

    def test_inserting_child_into_list_containing_one_child(self):
        self.assertEqual(
            self.widget.children,
            [],
            "No child was inserted, should return an empty list.",
        )
        # Create 2 children to insert into widget.
        child1 = toga.Widget()
        child2 = toga.Widget()

        self.widget._children = []
        self.widget.insert(0, child1)
        self.widget.insert(1, child2)
        self.assertEqual(self.widget.children, [child1, child2])

    def test_inserting_child_into_list_containing_three_children(self):
        self.assertEqual(
            self.widget.children,
            [],
            "No child was inserted, should return an empty list.",
        )
        # Create 3 children to add to widget.
        child1 = toga.Widget()
        child2 = toga.Widget()
        child3 = toga.Widget()
        # Create a child to insert into widget.
        child4 = toga.Widget()

        self.widget._children = []
        self.widget.add(child1, child2, child3)
        self.widget.insert(2, child4)

        self.assertEqual(self.widget.children, [child1, child2, child4, child3])

    def test_inserting_child_with_existing_parent(self):
        # Create a second parent widget.
        widget2 = toga.Widget()
        # Create a child widget to insert into widget2 before inserting into widget.
        child = toga.Widget()

        widget2._children = []
        widget2.insert(0, child)
        self.assertEqual(widget2.children, [child])

        self.widget._children = []
        self.widget.insert(0, child)
        self.assertEqual(self.widget.children, [child])
        self.assertEqual(widget2.children, [])

    def test_removing_child(self):
        self.assertEqual(
            self.widget.children, [], "No child was added, should return an empty list."
        )
        # Create a child widget to add then remove from widget.
        child = toga.Widget()

        self.widget._children = []
        self.widget.add(child)
        self.assertEqual(self.widget.children, [child])

        self.widget.remove(child)
        self.assertEqual(self.widget.children, [])

    def test_removing_child_with_app(self):
        app = toga.App("Test App", "org.beeware.test")
        self.widget.app = app
        self.assertEqual(
            self.widget.children, [], "No child was added, should return an empty list."
        )
        # Create a child widget to add then remove from widget.
        child = Widget()

        self.widget._children = []
        self.widget.add(child)
        self.assertEqual(self.widget.children, [child])
        self.assertEqual(len(app.widgets), 2)

        self.widget.remove(child)
        self.assertEqual(self.widget.children, [])
        self.assertEqual(len(app.widgets), 1)
        self.assertEqual(app.widgets[self.id], self.widget)

    def test_removing_child_with_window(self):
        window = toga.Window()
        window.content = Mock()
        self.widget.window = window
        self.assertEqual(
            self.widget.children, [], "No child was added, should return an empty list."
        )
        # Create a child widget to add then remove from widget.
        child = Widget()

        self.widget._children = []
        self.widget.add(child)
        self.assertEqual(self.widget.children, [child])
        self.assertEqual(len(window.widgets), 2)

        self.widget.remove(child)
        self.assertEqual(self.widget.children, [])
        self.assertEqual(len(window.widgets), 1)
        self.assertEqual(window.widgets[self.id], self.widget)

    def test_removing_children(self):
        self.assertEqual(
            self.widget.children, [], "No children added, should return an empty list."
        )
        # Create 2 children to add then remove from widget.
        child1 = toga.Widget()
        child2 = toga.Widget()

        self.widget._children = []
        self.widget.add(child1, child2)
        self.assertEqual(self.widget.children, [child1, child2])

        self.widget.remove(child1, child2)
        self.assertEqual(self.widget.children, [])

    def test_removing_two_out_of_three_children(self):
        self.assertEqual(
            self.widget.children, [], "No children added, should return am empty list."
        )
        # Create 3 children to add to widget, 2 of which will be removed.
        child1 = toga.Widget()
        child2 = toga.Widget()
        child3 = toga.Widget()

        self.widget._children = []
        self.widget.add(child1, child2, child3)
        self.assertEqual(self.widget.children, [child1, child2, child3])

        self.widget.remove(child1, child3)
        self.assertEqual(self.widget.children, [child2])

    def test_set_app(self):
        "A widget can be assigned to an app"
        app = toga.App("Test App", "org.beeware.test")
        self.assertEqual(len(app.widgets), 0)
        self.widget.app = app

        # The app has been assigned
        self.assertEqual(self.widget.app, app)
        self.assertEqual(len(app.widgets), 1)
        self.assertEqual(app.widgets[self.id], self.widget)

        # The app has been assigned to the underlying impl
        self.assertValueSet(self.widget, "app", app)

    def test_set_app_with_children(self):
        "A widget with children can be assigned to an app"
        # Create 2 children to add to widget, 2 of which will be removed.
        child_id1, child_id2 = "child-id1", "child-id2"
        child1 = Widget(id=child_id1)
        child2 = Widget(id=child_id2)

        self.widget._children = []
        self.widget.add(child1, child2)

        app = toga.App("Test App", "org.beeware.test")
        self.assertEqual(len(app.widgets), 0)

        self.widget.app = app

        # The app has been assigned to all children
        self.assertEqual(self.widget.app, app)
        self.assertEqual(child1.app, app)
        self.assertEqual(child2.app, app)
        self.assertEqual(len(app.widgets), 3)
        self.assertEqual(app.widgets[self.id], self.widget)
        self.assertEqual(app.widgets[child_id1], child1)
        self.assertEqual(app.widgets[child_id2], child2)

        # The app has been assigned to the underlying impls
        self.assertValueSet(self.widget, "app", app)
        self.assertValueSet(child1, "app", app)
        self.assertValueSet(child2, "app", app)

    def test_repeat_set_app(self):
        "If a widget is already assigned to an app, doing so again raises an error"
        app = toga.App("Test App", "org.beeware.test")
        self.widget.app = app

        # The app has been assigned
        self.assertEqual(self.widget.app, app)

        # Assign the widget to the same app
        app2 = toga.App("Test App", "org.beeware.test")

        with self.assertRaises(ValueError, msg="is already associated with an App"):
            self.widget.app = app2

        # The app is still assigned to the original app
        self.assertEqual(self.widget.app, app)
        self.assertEqual(list(app.widgets), [self.widget])

    def test_repeat_same_set_app(self):
        "If a widget is already assigned to an app, re-assigning to the same app is OK"
        app = toga.App("Test App", "org.beeware.test")
        self.widget.app = app

        # The app has been assigned
        self.assertEqual(self.widget.app, app)

        # Assign the widget to the same app
        self.widget.app = app

        # The app is still assigned
        self.assertEqual(self.widget.app, app)
        self.assertEqual(list(app.widgets), [self.widget])

    def test_remove_app(self):
        "A widget can be assigned to an app"
        app = toga.App("Test App", "org.beeware.test")
        self.assertEqual(len(app.widgets), 0)

        self.widget.app = app
        self.widget.app = None

        # The app has been unassigned
        self.assertIsNone(self.widget.app)
        self.assertEqual(len(app.widgets), 0)

        # The app has been assigned to the underlying impl
        self.assertValueSet(self.widget, "app", None)

    def test_set_window(self):
        window = toga.Window()
        self.assertEqual(len(window.widgets), 0)
        self.widget.window = window

        self.assertEqual(len(window.widgets), 1)
        self.assertEqual(window.widgets[self.id], self.widget)

    def test_replace_window(self):
        window1, window2 = (toga.Window(), toga.Window())
        self.widget.window = window1
        self.assertEqual(len(window1.widgets), 1)
        self.assertEqual(len(window2.widgets), 0)

        self.widget.window = window2
        self.assertEqual(len(window1.widgets), 0)
        self.assertEqual(len(window2.widgets), 1)
        self.assertEqual(window2.widgets[self.id], self.widget)

    def test_remove_window(self):
        window = toga.Window()
        self.assertEqual(len(window.widgets), 0)

        self.widget.window = window
        self.widget.window = None

        self.assertEqual(len(window.widgets), 0)

    def test_focus(self):
        self.widget.focus()
        self.assertActionPerformed(self.widget, "focus")

    def test_set_tab_index(self):
        tab_index = 8
        self.widget.tab_index = tab_index
        self.assertValueSet(self.widget, "tab_index", tab_index)

    def test_get_tab_index(self):
        tab_index = 8
        self.widget.tab_index = tab_index
        self.assertEqual(self.widget.tab_index, tab_index)
        self.assertValueGet(self.widget, "tab_index")
