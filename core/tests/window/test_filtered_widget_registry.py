import pytest

import toga


# Create the simplest possible widget with a concrete implementation
class ExampleWidget(toga.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._impl = self.factory.Widget(self)

    def __repr__(self):
        return f"Widget(id={self.id!r})"


# Create a box subclass with a reproducible repr
class ExampleBox(toga.Box):
    def __repr__(self):
        return f"Box(id={self.id!r})"


def make_window(win_id):
    win = toga.Window(id=win_id)
    win.content = ExampleBox(
        id=f"{win_id}.0",
        children=[
            ExampleWidget(id=f"{win_id}.1"),
            ExampleWidget(id=f"{win_id}.2"),
        ],
    )
    return win


def test_membership(app):
    """The registry proxy returns the total widget count."""
    # Create 2 windows with widgets
    win_1 = make_window("1")
    win_2 = make_window("2")

    # The widget registry now has 6 items in it
    assert len(app.widgets) == 6
    assert "1.0" in app.widgets
    assert "1.1" in app.widgets
    assert "1.2" in app.widgets
    assert "1.X" not in app.widgets
    assert "2.0" in app.widgets
    assert "2.1" in app.widgets
    assert "2.2" in app.widgets
    assert "2.X" not in app.widgets

    assert app.widgets["1.1"] == win_1.content.children[0]
    assert app.widgets["2.1"] == win_2.content.children[0]

    assert sorted(app.widgets.keys()) == ["1.0", "1.1", "1.2", "2.0", "2.1", "2.2"]
    assert sorted(app.widgets.values()) == [
        win_1.content,
        win_1.content.children[0],
        win_1.content.children[1],
        win_2.content,
        win_2.content.children[0],
        win_2.content.children[1],
    ]
    assert sorted(iter(app.widgets)) == [
        win_1.content,
        win_1.content.children[0],
        win_1.content.children[1],
        win_2.content,
        win_2.content.children[0],
        win_2.content.children[1],
    ]
    assert sorted(app.widgets.items()) == [
        ("1.0", win_1.content),
        ("1.1", win_1.content.children[0]),
        ("1.2", win_1.content.children[1]),
        ("2.0", win_2.content),
        ("2.1", win_2.content.children[0]),
        ("2.2", win_2.content.children[1]),
    ]
    assert repr(app.widgets) == (
        "{'1.0': Box(id='1.0'), '1.1': Widget(id='1.1'), '1.2': Widget(id='1.2'), "
        "'2.0': Box(id='2.0'), '2.1': Widget(id='2.1'), '2.2': Widget(id='2.2')}"
    )

    # Window 1's registry only has the subset of win1 widgets
    assert len(win_1.widgets) == 3
    assert "1.0" in win_1.widgets
    assert "1.1" in win_1.widgets
    assert "1.2" in win_1.widgets
    assert "1.X" not in win_1.widgets
    assert "2.0" not in win_1.widgets
    assert "2.1" not in win_1.widgets
    assert "2.2" not in win_1.widgets
    assert "2.X" not in win_1.widgets

    assert win_1.widgets["1.1"] == win_1.content.children[0]

    with pytest.raises(KeyError, match=r"2\.1"):
        win_1.widgets["2.1"]

    assert sorted(win_1.widgets.keys()) == ["1.0", "1.1", "1.2"]
    assert sorted(win_1.widgets.values()) == [
        win_1.content,
        win_1.content.children[0],
        win_1.content.children[1],
    ]
    assert sorted(iter(win_1.widgets)) == [
        win_1.content,
        win_1.content.children[0],
        win_1.content.children[1],
    ]
    assert sorted(win_1.widgets.items()) == [
        ("1.0", win_1.content),
        ("1.1", win_1.content.children[0]),
        ("1.2", win_1.content.children[1]),
    ]
    assert (
        repr(win_1.widgets)
        == "{'1.0': Box(id='1.0'), '1.1': Widget(id='1.1'), '1.2': Widget(id='1.2')}"
    )

    # Win 2 is the same as win 1; do a quick check
    assert len(win_2.widgets) == 3
    assert (
        repr(win_2.widgets)
        == "{'2.0': Box(id='2.0'), '2.1': Widget(id='2.1'), '2.2': Widget(id='2.2')}"
    )

    # Remove a widget
    widget = win_1.widgets["1.1"]
    win_1.content.remove(widget)

    # It is no longer in the app registry.
    assert len(app.widgets) == 5
    assert len(win_1.widgets) == 2
    assert "1.1" not in app.widgets
    assert "1.1" not in win_1.widgets

    with pytest.raises(KeyError, match=r"1\.1"):
        app.widgets["1.1"]

    with pytest.raises(KeyError, match=r"1\.1"):
        win_1.widgets["1.1"]


def test_reuse_id(app):
    """A widget ID can be reused once a widget has been removed (#2190)"""
    # Create 2 windows with widgets
    win_1 = make_window("1")
    win_2 = make_window("2")

    # the `magic` ID doesn't exist initially
    assert "magic" not in app.widgets
    assert "magic" not in win_1.widgets
    assert "magic" not in win_2.widgets

    # Create a widget with the magic ID. The widget still isn't in the registry, because
    # it's not part of a window
    first = ExampleWidget(id="magic")

    assert "magic" not in app.widgets
    assert "magic" not in win_1.widgets
    assert "magic" not in win_2.widgets

    # Add the widget to the window. This adds it to the registry
    win_1.content.add(first)

    assert "magic" in app.widgets
    assert "magic" in win_1.widgets
    assert "magic" not in win_2.widgets
    assert app.widgets["magic"] == first

    # Create a second widget with the same ID.
    # The widget exists, but the registry is storing `first`.
    second = ExampleWidget(id="magic")

    assert "magic" in app.widgets
    assert "magic" in win_1.widgets
    assert "magic" not in win_2.widgets
    assert app.widgets["magic"] == first

    # The second widget can't be added as content to either window, because of the ID clash.
    with pytest.raises(
        KeyError,
        match=r"There is already a widget with the id 'magic'",
    ):
        win_1.content.add(second)

    assert "magic" in app.widgets
    assert "magic" in win_1.widgets
    assert "magic" not in win_2.widgets
    assert app.widgets["magic"] == first

    # The widget can't be added to a different window, because there's still an app-level conflict.
    with pytest.raises(
        KeyError,
        match=r"There is already a widget with the id 'magic'",
    ):
        win_2.content.add(second)

    assert "magic" in app.widgets
    assert "magic" in win_1.widgets
    assert "magic" not in win_2.widgets
    assert app.widgets["magic"] == first

    # Remove the first widget
    win_1.content.remove(first)

    assert "magic" not in app.widgets
    assert "magic" not in win_1.widgets
    assert "magic" not in win_2.widgets
    with pytest.raises(KeyError, match=r"magic"):
        app.widgets["magic"]

    # The second widget can now be added to as content.
    win_1.content.add(second)

    assert "magic" in app.widgets
    assert "magic" in win_1.widgets
    assert "magic" not in win_2.widgets
    assert app.widgets["magic"] == second
