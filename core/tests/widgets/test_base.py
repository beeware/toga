import pytest

import toga
from toga.style import Pack
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
    assert_attribute_not_set,
    attribute_value,
)


# Create the simplest possible widget with a concrete implementation that will
# allow children
class ExampleWidget(toga.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._impl = self.factory.Widget(self)
        self._children = []


# Create the simplest possible widget with a concrete implementation that cannot
# have children.
class ExampleLeafWidget(toga.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._impl = self.factory.Widget(self)


@pytest.fixture
def widget(app):
    # App fixture is needed to ensure a fresh widget registry is created
    return ExampleWidget(id="widget_id", style=Pack(padding=666))


def test_simple_widget():
    """A simple widget can be created."""
    widget = ExampleWidget()

    # Round trip the impl/interface
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create Widget")

    # Base properties of the widget have been set
    assert widget.id == str(id(widget))
    assert isinstance(widget.style, Pack)
    assert widget.style.padding == (0, 0, 0, 0)


def test_widget_created(widget):
    """A widget can be created with arguments."""
    # Round trip the impl/interface
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create Widget")

    # Base properties of the widget have been set
    assert widget.enabled
    assert widget.id == "widget_id"
    assert isinstance(widget.style, Pack)
    assert widget.style.padding == (666, 666, 666, 666)


def test_add_child_to_leaf():
    """A child cannot be added to a leaf node."""
    leaf = ExampleLeafWidget()

    # Widget doesn't have an app or window
    assert leaf.app is None
    assert leaf.window is None

    # Leaf nodes report an empty child list
    assert leaf.children == []

    # Create a child widget
    child = ExampleLeafWidget()

    # Add the child.
    with pytest.raises(ValueError, match=r"ExampleLeafWidget cannot have children"):
        leaf.add(child)


def test_add_child_without_app(widget):
    """A child can be added to a node when there's no underlying app."""
    # Widget doesn't have an app or window
    assert widget.app is None
    assert widget.window is None

    # Child list is empty
    assert widget.children == []

    # Create a child widget
    child = ExampleLeafWidget()

    # Add the child.
    widget.add(child)

    # Widget knows about the child and vice versa
    assert widget.children == [child]
    assert child.parent == widget

    # Child has inherited parent's app/window details
    assert child.app is None
    assert child.window is None

    # The impl's add_child has been invoked
    assert_action_performed_with(widget, "add child", child=child._impl)

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")


def test_add_child(app, widget):
    """A child can be added to a node when there's an app & window."""
    # Set the app and window for the widget.
    window = toga.Window()
    window.content = widget
    # Clear the event log
    EventLog.reset()

    # Widget has an app and window
    assert widget.app == app
    assert widget.window == window

    # Widget is registered with app and window
    assert widget.id in app.widgets
    assert widget.id in window.widgets

    # Child list is empty
    assert widget.children == []

    # Create a child widget
    child = ExampleLeafWidget(id="child_id")

    # App's widget index only contains the parent
    assert app.widgets["widget_id"] == widget
    assert "child_id" not in app.widgets

    # Add the child.
    widget.add(child)

    # Widget knows about the child and vice versa
    assert widget.children == [child]
    assert child.parent == widget

    # Child has inherited parent's app/window details
    assert child.app == app
    assert child.window == window

    # The impl's add_child has been invoked
    assert_action_performed_with(widget, "add child", child=child._impl)

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")

    # The window's content gets a refresh notification
    assert_action_performed_with(window.content, "refresh")

    # App's widget index has been updated
    assert len(app.widgets) == 2
    assert app.widgets["widget_id"] == widget
    assert app.widgets["child_id"] == child


def test_child_square_bracket_access(widget):
    """Assign and get individual children via square bracket notation."""
    child1 = ExampleLeafWidget(id="child1_id")
    child2 = ExampleLeafWidget(id="child2_id")

    # Add child to widget
    widget.add(child1)

    # Verify child has been added
    assert widget.children == [child1]

    # Assign child via __setitem__
    widget.children[0] = child2

    # Verify new child is in children via __getitem__
    assert widget.children[0] == child2


def test_get_index_of_children(widget):
    """Populate a widget with children and check the index method."""
    child1 = ExampleLeafWidget(id="child1_id")
    child2 = ExampleLeafWidget(id="child2_id")
    child3 = ExampleLeafWidget(id="child3_id")

    # Add only two children to widget
    widget.add(child1)
    widget.add(child2)

    # Verify children have been added
    assert widget.children == [child1, child2]

    # Get indices of valid children
    assert widget.index(child1) == 0
    assert widget.index(child2) == 1

    # Raise error when child not found in children
    with pytest.raises(ValueError, match=r"ExampleLeafWidget not found"):
        widget.index(child3)


def test_replace_child_with_non_child(widget):
    """Remove a child and add new widget in its place."""
    child1 = ExampleLeafWidget(id="child1_id")
    child2 = ExampleLeafWidget(id="child2_id")
    child3 = ExampleLeafWidget(id="child3_id")

    # Add only two children to widget
    widget.add(child1)
    widget.add(child2)

    # Verify children have been added
    assert widget.children == [child1, child2]

    widget.replace(child1, child3)

    # Verify child1 has been removed and child3 has been added
    assert widget.children == [child3, child2]


def test_add_multiple_children(app, widget):
    """Multiple children can be added in one call."""
    # Set the app and window for the widget.
    window = toga.Window()
    window.content = widget
    # Clear the event log
    EventLog.reset()

    # Widget has an app and window
    assert widget.app == app
    assert widget.window == window

    # Child list is empty
    assert widget.children == []

    # Create 3 child widgets
    child1 = ExampleLeafWidget(id="child1_id")
    child2 = ExampleLeafWidget(id="child2_id")
    child3 = ExampleLeafWidget(id="child3_id")

    # App's widget index only contains the parent
    assert dict(app.widgets) == {"widget_id": widget}

    # Add the children.
    widget.add(child1, child2, child3)

    # Widget knows about the child and vice versa
    assert widget.children == [child1, child2, child3]
    assert child1.parent == widget
    assert child2.parent == widget
    assert child3.parent == widget

    # Children has inherited parent's app/window details
    assert child1.app == app
    assert child1.window == window

    assert child2.app == app
    assert child2.window == window

    assert child3.app == app
    assert child3.window == window

    # The impl's add_child has been invoked 3 time
    assert_action_performed_with(widget, "add child", child=child1._impl)
    assert_action_performed_with(widget, "add child", child=child2._impl)
    assert_action_performed_with(widget, "add child", child=child3._impl)

    # The widget's layout has been refreshed
    # There will be multiple refresh calls
    assert_action_performed_with(widget, "refresh")

    # The window's content gets a refresh notification
    assert_action_performed_with(window.content, "refresh")

    # App's widget index has been updated
    assert dict(app.widgets) == {
        "widget_id": widget,
        "child1_id": child1,
        "child2_id": child2,
        "child3_id": child3,
    }

    # Window's widget index has been updated
    assert dict(window.widgets) == {
        "widget_id": widget,
        "child1_id": child1,
        "child2_id": child2,
        "child3_id": child3,
    }


def test_reparent_child(widget):
    """A widget can be reparented."""
    # Create a second parent widget, and add a child to it
    other = ExampleWidget(id="other")
    child = ExampleLeafWidget(id="child_id")
    other.add(child)

    assert other.children == [child]
    assert child.parent == other

    # Add the child to the widget
    widget.add(child)

    # Widget knows about the child and vice versa
    assert widget.children == [child]
    assert child.parent == widget

    # Original parent as lost the child
    assert other.children == []

    # The impl's add_child has been invoked
    assert_action_performed_with(widget, "add child", child=child._impl)

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")

    # The layout of the old parent has been refreshed
    assert_action_performed_with(other, "refresh")


def test_reparent_child_to_self(widget):
    """Reparenting a widget to the same parent is a no-op."""
    # Add a child to the widget
    child = ExampleLeafWidget(id="child_id")
    widget.add(child)

    assert widget.children == [child]
    assert child.parent == widget

    # Reset the event log so all previous add events are lost
    EventLog.reset()

    # Add the child to the widget again
    widget.add(child)

    # Widget knows about the child and vice versa
    assert widget.children == [child]
    assert child.parent == widget

    # The impl's add_child has *not* been invoked,
    # as the widget was already a child
    assert_action_not_performed(widget, "add child")

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")


def test_insert_child_into_leaf():
    """A child cannot be inserted into a leaf node."""
    leaf = ExampleLeafWidget()

    # Widget doesn't have an app or window
    assert leaf.app is None
    assert leaf.window is None

    # Leaf nodes report an empty child list
    assert leaf.children == []

    # Create a child widget
    child = ExampleLeafWidget()

    # insert the child.
    with pytest.raises(ValueError, match=r"ExampleLeafWidget cannot have children"):
        leaf.insert(0, child)


def test_insert_child_without_app(widget):
    """A child can be inserted into a node when there's no underlying app."""
    # Widget doesn't have an app or window
    assert widget.app is None
    assert widget.window is None

    # Child list is empty
    assert widget.children == []

    # Create a child widget
    child = ExampleLeafWidget()

    # insert the child.
    widget.insert(0, child)

    # Widget knows about the child and vice versa
    assert widget.children == [child]
    assert child.parent == widget

    # Child has inherited parent's app/window details
    assert child.app is None
    assert child.window is None

    # The impl's insert_child has been invoked
    assert_action_performed_with(widget, "insert child", child=child._impl)

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")


def test_insert_child(app, widget):
    """A child can be inserted into a node when there's an app & window."""
    # Set the app and window for the widget.
    window = toga.Window()
    window.content = widget
    # Clear the event log
    EventLog.reset()

    # Widget has an app and window
    assert widget.app == app
    assert widget.window == window

    # Child list is empty
    assert widget.children == []

    # Create a child widget
    child = ExampleLeafWidget(id="child_id")

    # App's widget index only contains the parent
    assert app.widgets["widget_id"] == widget
    assert "child_id" not in app.widgets

    # insert the child.
    widget.insert(0, child)

    # Widget knows about the child and vice versa
    assert widget.children == [child]
    assert child.parent == widget

    # Child has inherited parent's app/window details
    assert child.app == app
    assert child.window == window

    # The impl's insert_child has been invoked
    assert_action_performed_with(widget, "insert child", child=child._impl)

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")

    # The window's content gets a refresh notification
    assert_action_performed_with(window.content, "refresh")

    # App's widget index has been updated
    assert dict(app.widgets) == {
        "widget_id": widget,
        "child_id": child,
    }

    # Window's widget index has been updated
    assert dict(window.widgets) == {
        "widget_id": widget,
        "child_id": child,
    }


def test_insert_position(app, widget):
    """Insert can put a child into a specific position."""
    # Set the app and window for the widget.
    window = toga.Window()
    window.content = widget
    # Clear the event log
    EventLog.reset()

    # Widget has an app and window
    assert widget.app == app
    assert widget.window == window

    # Child list is empty
    assert widget.children == []

    # Create 3 child widgets
    child1 = ExampleLeafWidget(id="child1_id")
    child2 = ExampleLeafWidget(id="child2_id")
    child3 = ExampleLeafWidget(id="child3_id")

    # App's widget index only contains the parent
    assert dict(app.widgets) == {"widget_id": widget}

    # Windows's widget index only contains the parent
    assert dict(window.widgets) == {"widget_id": widget}

    # insert the children.
    widget.insert(0, child1)
    widget.insert(0, child2)
    widget.insert(1, child3)

    # Widget knows about the child and vice versa
    assert widget.children == [child2, child3, child1]
    assert child1.parent == widget
    assert child2.parent == widget
    assert child3.parent == widget

    # Children has inherited parent's app/window details
    assert child1.app == app
    assert child1.window == window

    assert child2.app == app
    assert child2.window == window

    assert child3.app == app
    assert child3.window == window

    # The impl's insert_child has been invoked 3 time
    assert_action_performed_with(widget, "insert child", child=child1._impl)
    assert_action_performed_with(widget, "insert child", child=child2._impl)
    assert_action_performed_with(widget, "insert child", child=child3._impl)

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")

    # The window's content gets a refresh notification
    assert_action_performed_with(window.content, "refresh")

    # App's widget index has been updated
    assert dict(app.widgets) == {
        "widget_id": widget,
        "child1_id": child1,
        "child2_id": child2,
        "child3_id": child3,
    }

    # Window's widget index has been updated
    assert dict(window.widgets) == {
        "widget_id": widget,
        "child1_id": child1,
        "child2_id": child2,
        "child3_id": child3,
    }


def test_insert_bad_position(app, widget):
    """If the position is invalid, an error is raised."""
    # Set the app and window for the widget.
    window = toga.Window()
    window.content = widget
    # Clear the event log
    EventLog.reset()

    # Widget has an app and window
    assert widget.app == app
    assert widget.window == window

    # Child list is empty
    assert widget.children == []

    # Create a child widget
    child = ExampleLeafWidget(id="child_id")

    # App's widget index only contains the parent
    assert dict(app.widgets) == {"widget_id": widget}

    # Window's widget index only contains the parent
    assert dict(window.widgets) == {"widget_id": widget}

    # Insert the child at a position greater than the length of the list.
    # Widget will be added to the end of the list.
    widget.insert(37, child)

    # Widget knows about the child and vice versa
    assert widget.children == [child]
    assert child.parent == widget

    # Child has inherited parent's app/window details
    assert child.app == app
    assert child.window == window

    # The impl's insert_child has been invoked
    assert_action_performed_with(widget, "insert child", child=child._impl)

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")

    # The window's content gets a refresh notification
    assert_action_performed_with(window.content, "refresh")

    # App's widget index has been updated
    assert dict(app.widgets) == {
        "widget_id": widget,
        "child_id": child,
    }

    # Window's widget index has been updated
    assert dict(window.widgets) == {
        "widget_id": widget,
        "child_id": child,
    }


def test_insert_reparent_child(widget):
    """A widget can be reparented by insertion."""
    # Create a second parent widget, and add a child to it
    other = ExampleWidget(id="other")
    child = ExampleLeafWidget(id="child_id")
    other.add(child)

    assert other.children == [child]
    assert child.parent == other

    # insert the child to the widget
    widget.insert(0, child)

    # Widget knows about the child and vice versa
    assert widget.children == [child]
    assert child.parent == widget

    # Original parent as lost the child
    assert other.children == []

    # The impl's insert_child has been invoked
    assert_action_performed_with(widget, "insert child", child=child._impl)

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")

    # The original parent's layout has been refreshed
    assert_action_performed_with(other, "refresh")


def test_insert_reparent_child_to_self(widget):
    """Reparenting a widget to the same parent by insertion is a no-op."""
    # Add a child to the widget
    child = ExampleLeafWidget(id="child_id")
    widget.add(child)

    assert widget.children == [child]
    assert child.parent == widget

    # Reset the event log so all previous insert events are lost
    EventLog.reset()

    # insert the child to the widget again
    widget.insert(0, child)

    # Widget knows about the child and vice versa
    assert widget.children == [child]
    assert child.parent == widget

    # The impl's insert_child has *not* been invoked,
    # as the widget was already a child
    assert_action_not_performed(widget, "insert child")

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")


def test_remove_child_from_leaf():
    """A child cannot be removed from a leaf node."""
    leaf = ExampleLeafWidget()

    # Widget doesn't have an app or window
    assert leaf.app is None
    assert leaf.window is None

    # Leaf nodes report an empty child list
    assert leaf.children == []

    # Create a child widget
    child = ExampleLeafWidget()

    # Remove the child.
    with pytest.raises(ValueError, match=r"ExampleLeafWidget cannot have children"):
        leaf.remove(child)


def test_remove_child_without_app(widget):
    """A child without an app or window can be removed from a widget."""
    # Add a child to the widget
    child = ExampleLeafWidget(id="child_id")
    widget.add(child)

    assert widget.children == [child]
    assert child.parent == widget
    assert child.app is None
    assert child.window is None

    # Remove the child
    widget.remove(child)

    # Parent doesn't know about the child, and vice versa
    assert widget.children == []
    assert child.parent is None

    # App and window are still None
    assert child.app is None
    assert child.window is None

    # The impl's remove_child has been invoked
    assert_action_performed_with(widget, "remove child", child=child._impl)

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")


def test_remove_child(app, widget):
    """A child associated with an app & window can be removed from a widget."""
    # Add a child to the widget
    child = ExampleLeafWidget(id="child_id")
    widget.add(child)

    window = toga.Window()
    window.content = widget
    # Clear the event log
    EventLog.reset()

    assert widget.children == [child]
    assert child.parent == widget
    assert child.app == app
    assert child.window == window
    assert dict(app.widgets) == {"widget_id": widget, "child_id": child}
    assert dict(window.widgets) == {"widget_id": widget, "child_id": child}

    # Remove the child
    widget.remove(child)

    # Parent doesn't know about the child, and vice versa
    assert widget.children == []
    assert child.parent is None

    # app and window have been reset.
    assert child.app is None
    assert child.window is None

    # child widget no longer exists in the app or widgets registries.
    assert dict(app.widgets) == {"widget_id": widget}
    assert dict(window.widgets) == {"widget_id": widget}

    # The impl's remove_child has been invoked
    assert_action_performed_with(widget, "remove child", child=child._impl)

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")

    # The window's content gets a refresh notification
    assert_action_performed_with(window.content, "refresh")

    # App's widget index does not contain the widget
    assert "child_id" not in app.widgets


def test_remove_multiple_children(app, widget):
    """Multiple children can be removed from a widget."""
    # Add children to the widget
    child1 = ExampleLeafWidget(id="child1_id")
    child2 = ExampleLeafWidget(id="child2_id")
    child3 = ExampleLeafWidget(id="child3_id")
    widget.add(child1, child2, child3)

    window = toga.Window()
    window.content = widget
    # Clear the event log
    EventLog.reset()

    assert widget.children == [child1, child2, child3]
    for child in widget.children:
        assert child.parent == widget
        assert child.app == app
        assert child.window == window
        assert app.widgets[child.id] == child
        assert window.widgets[child.id] == child

    # Remove 2 children
    widget.remove(child1, child3)

    # Parent doesn't know about the removed children, and vice versa
    assert widget.children == [child2]
    assert child1.parent is None
    assert child2.parent == widget
    assert child3.parent is None

    # App and window have been reset on the removed widgets
    assert child1.app is None
    assert child1.window is None

    assert child2.app == app
    assert child2.window == window

    assert child3.app is None
    assert child3.window is None

    # The impl's remove_child has been invoked twice
    assert_action_performed_with(widget, "remove child", child=child1._impl)
    assert_action_performed_with(widget, "remove child", child=child3._impl)

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")

    # The window's content gets a refresh notification
    assert_action_performed_with(window.content, "refresh")

    # App's widget index does not contain the widget
    assert "child1_id" not in app.widgets
    assert "child3_id" not in app.widgets

    # Windows's widget index does not contain the widget
    assert "child1_id" not in window.widgets
    assert "child3_id" not in window.widgets


def test_clear_all_children(app, widget):
    """All children can be simultaneously removed from a widget."""
    # Add children to the widget
    child1 = ExampleLeafWidget(id="child1_id")
    child2 = ExampleLeafWidget(id="child2_id")
    child3 = ExampleLeafWidget(id="child3_id")
    widget.add(child1, child2, child3)

    window = toga.Window()
    window.content = widget
    # Clear the event log
    EventLog.reset()

    assert widget.children == [child1, child2, child3]
    for child in widget.children:
        assert child.parent == widget
        assert child.app == app
        assert child.window == window
        assert app.widgets[child.id] == child
        assert window.widgets[child.id] == child

    # Clear children
    widget.clear()

    # Parent doesn't know about the removed children, and vice versa
    assert widget.children == []
    assert child1.parent is None
    assert child2.parent is None
    assert child3.parent is None

    # App and window have been reset on the removed widgets
    assert child1.app is None
    assert child1.window is None

    assert child2.app is None
    assert child2.window is None

    assert child3.app is None
    assert child3.window is None

    # The impl's remove_child has been invoked thrice
    assert_action_performed_with(widget, "remove child", child=child1._impl)
    assert_action_performed_with(widget, "remove child", child=child2._impl)
    assert_action_performed_with(widget, "remove child", child=child3._impl)

    # The widget's layout has been refreshed
    assert_action_performed_with(widget, "refresh")

    # The window's content gets a refresh notification
    assert_action_performed_with(window.content, "refresh")

    # App's widget index does not contain the widget
    assert "child1_id" not in app.widgets
    assert "child2_id" not in app.widgets
    assert "child3_id" not in app.widgets

    # Window's widget index does not contain the widget
    assert "child1_id" not in window.widgets
    assert "child2_id" not in window.widgets
    assert "child3_id" not in window.widgets


def test_clear_no_children(app, widget):
    """No changes are made (no-op) if widget has no children."""
    window = toga.Window()
    window.content = widget
    # Clear the event log
    EventLog.reset()

    assert widget.children == []

    # Clear children
    widget.clear()

    # Parent doesn't have any children still
    assert widget.children == []

    # The widget's layout has *not* been refreshed
    assert_action_not_performed(widget, "refresh")

    # The window's content doesn't get a refresh notification
    assert_action_not_performed(window.content, "refresh")


def test_clear_leaf(app):
    """`clear` cannot be called on a leaf node."""
    leaf = ExampleLeafWidget()
    window = toga.Window()
    window.content = leaf
    # Clear the event log
    EventLog.reset()

    assert leaf.children == []

    # Clear children
    with pytest.raises(ValueError, match=r"ExampleLeafWidget cannot have children"):
        leaf.clear()

    # Parent doesn't have any children still
    assert leaf.children == []

    # The widget's layout has *not* been refreshed
    assert_action_not_performed(leaf, "refresh")

    # The window's content doesn't get a refresh notification
    assert_action_not_performed(window.content, "refresh")


def test_remove_from_non_parent(widget):
    """Trying to remove a child from a widget other than it's parent is a no-op."""
    # Create a second parent widget, and add a child to it
    other = ExampleWidget(id="other")
    child = ExampleLeafWidget(id="child_id")
    other.add(child)

    assert widget.children == []
    assert other.children == [child]
    assert child.parent == other

    # Remove the child from *widget*, which is not the parent
    widget.remove(child)

    # Nothing has changed.
    assert widget.children == []
    assert other.children == [child]
    assert child.parent == other

    # The impl's remove_child has been invoked
    assert_action_not_performed(widget, "remove child")

    # The widget's layout has *not* been refreshed
    assert_action_not_performed(widget, "refresh")


def test_set_app(app, widget):
    """A widget can be assigned to an app."""
    assert len(app.widgets) == 0

    # Assign the widget to an app
    widget.app = app

    # The app has been assigned
    assert widget.app == app

    # The widget doesn't appear in the index, as it's not on a window
    assert len(app.widgets) == 0
    assert "widget_id" not in app.widgets

    # The impl has had its app property set.
    assert attribute_value(widget, "app") == app

    # Assign the widget to a window
    window = toga.Window()
    window.content = widget

    # The widget is now in the app index.
    assert len(app.widgets) == 1
    assert app.widgets["widget_id"] == widget


def test_set_app_with_children(app, widget):
    """If a widget has children, the children get the app assignment."""
    # Add children to the widget
    child1 = ExampleLeafWidget(id="child1_id")
    child2 = ExampleLeafWidget(id="child2_id")
    child3 = ExampleLeafWidget(id="child3_id")
    widget.add(child1, child2, child3)

    assert len(app.widgets) == 0

    # Assign the widget as window content
    window = toga.Window()
    window.content = widget

    # The app has been assigned
    assert widget.app == app

    # The children also have the app assigned
    assert child1.app == app
    assert child2.app == app
    assert child3.app == app

    # The widget index has been updated
    assert len(app.widgets) == 4
    assert app.widgets["widget_id"] == widget
    assert app.widgets["child1_id"] == child1
    assert app.widgets["child2_id"] == child2
    assert app.widgets["child3_id"] == child3

    # The impl of widget and children have had their app property set.
    assert attribute_value(widget, "app") == app
    assert attribute_value(child1, "app") == app
    assert attribute_value(child2, "app") == app
    assert attribute_value(child3, "app") == app


def test_set_same_app(app, widget):
    """A widget can be re-assigned to the same app."""
    assert len(app.widgets) == 0

    # Assign the widget to an app
    widget.app = app

    # Reset the event log so we know the new events
    EventLog.reset()

    # Assign the widget to the same app
    widget.app = app

    # The impl has not had its app property set as a result of the update
    assert_attribute_not_set(widget, "app")


def test_reset_app(app, widget):
    """A widget can be re-assigned to no app."""
    assert len(app.widgets) == 0

    # Assign the widget to an app
    widget.app = app

    # Reset the event log so we know the new events
    EventLog.reset()

    # Clear the app assignment
    widget.app = None

    # The app has been assigned
    assert widget.app is None

    # The widget index has been updated
    assert len(app.widgets) == 0

    # The impl has had its app property set.
    assert attribute_value(widget, "app") is None


def test_set_new_app(app, widget):
    """A widget can be assigned to a different app."""
    # Assign the widget to an app. It won't appear in the registry, as
    # it hasn't been assigned to a window
    widget.app = app
    assert len(app.widgets) == 0

    # Reset the event log so we know the new events
    EventLog.reset()

    # Create a new app
    new_app = toga.App("Test App", "org.beeware.toga.test-app")
    assert len(new_app.widgets) == 0

    # Assign the widget to the same app
    widget.app = new_app

    # The widget has been assigned to the new app
    assert widget.app == new_app

    # The widget still doesn't appear in a widget index.
    assert len(app.widgets) == 0
    assert "widget_id" not in app.widgets
    assert len(new_app.widgets) == 0
    assert "widget_id" not in new_app.widgets

    # The impl has had its app property set.
    assert attribute_value(widget, "app") == new_app


def test_set_window(widget):
    """A widget can be assigned to a window."""
    window = toga.Window()
    assert len(window.widgets) == 0
    assert widget.window is None

    # Assign the widget to a window
    widget.window = window

    # Window has been assigned
    assert widget.window == window

    # Window Widget registry has been updated
    assert len(window.widgets) == 1
    assert window.widgets["widget_id"] == widget


def test_set_window_with_children(app, widget):
    """A widget can be assigned to a window."""
    # Add children to the widget
    child1 = ExampleLeafWidget(id="child1_id")
    child2 = ExampleLeafWidget(id="child2_id")
    child3 = ExampleLeafWidget(id="child3_id")
    widget.add(child1, child2, child3)

    window = toga.Window()
    assert len(app.widgets) == 0
    assert len(window.widgets) == 0
    assert widget.window is None
    assert child1.window is None
    assert child2.window is None
    assert child3.window is None

    # Assign the widget to a window
    widget.window = window

    # Window has been assigned
    assert widget.window == window
    assert child1.window == window
    assert child2.window == window
    assert child3.window == window

    # Widget registry has been updated
    assert len(app.widgets) == 4
    assert len(window.widgets) == 4
    assert window.widgets["widget_id"] == widget
    assert window.widgets["child1_id"] == child1
    assert window.widgets["child2_id"] == child2
    assert window.widgets["child3_id"] == child3


def test_reset_window(widget):
    """A widget can be assigned to a different window."""
    window = toga.Window()
    assert len(window.widgets) == 0
    assert widget.window is None

    # Assign the widget to a window
    widget.window = window
    assert len(window.widgets) == 1

    # Create a new window
    new_window = toga.Window()

    # Assign the widget to the new window
    widget.window = new_window

    # Window has been assigned
    assert widget.window == new_window

    # Window Widget registry has been updated
    assert len(window.widgets) == 0
    assert len(new_window.widgets) == 1
    assert new_window.widgets["widget_id"] == widget


def test_unset_window(widget):
    """A widget can be assigned to no window."""
    window = toga.Window()
    assert len(window.widgets) == 0
    assert widget.window is None

    # Assign the widget to a window
    widget.window = window
    assert len(window.widgets) == 1

    # Assign the widget to no window
    widget.window = None

    # The widget doesn't have a window
    assert widget.window is None

    # Window Widget registry has been updated
    assert len(window.widgets) == 0


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, False),
        ("", False),
        ("true", True),
        ("false", True),  # Evaluated as a string, this value is true.
        (0, False),
        (1234, True),
    ],
)
def test_enabled(widget, value, expected):
    """The enabled status of the widget can be changed."""
    # Widget is initially enabled by default.
    assert widget.enabled

    # Set the enabled status
    widget.enabled = value
    assert widget.enabled == expected

    # Disable the widget
    widget.enabled = False
    assert not widget.enabled

    # Set the enabled status again
    widget.enabled = value
    assert widget.enabled == expected


def test_refresh_root(widget):
    """Refresh can be invoked on the root node."""
    # Add children to the widget
    child1 = ExampleLeafWidget(id="child1_id")
    child2 = ExampleLeafWidget(id="child2_id")
    child3 = ExampleLeafWidget(id="child3_id")
    widget.add(child1, child2, child3)

    # Refresh the root node
    widget.refresh()

    # Root widget was refreshed
    assert_action_performed(widget, "refresh")


def test_refresh_child(widget):
    """Refresh can be invoked on child."""
    # Add children to the widget
    child1 = ExampleLeafWidget(id="child1_id")
    child2 = ExampleLeafWidget(id="child2_id")
    child3 = ExampleLeafWidget(id="child3_id")
    widget.add(child1, child2, child3)

    # Refresh a child
    child2.refresh()

    # Child widget was refreshed
    assert_action_performed(child2, "refresh")

    # Root widget was refreshed
    assert_action_performed(widget, "refresh")


def test_focus(widget):
    """A widget can be given focus."""
    widget.focus()
    assert_action_performed(widget, "focus")


def test_tab_index(widget):
    """The tab index of a widget can be set and retrieved."""
    # The initial tab index is None
    assert widget.tab_index is None

    tab_index = 8
    widget.tab_index = tab_index

    assert widget.tab_index == 8
    assert attribute_value(widget, "tab_index") == tab_index
