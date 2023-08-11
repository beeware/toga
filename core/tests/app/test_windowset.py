import pytest

import toga
from toga.app import WindowSet


@pytest.fixture
def app():
    return toga.App("Test App", "org.beeware.toga.app.main_window")


@pytest.fixture
def window1():
    return toga.Window(title="Window 1")


@pytest.fixture
def window2():
    return toga.Window(title="Window 2")


@pytest.fixture
def window3():
    return toga.Window(title="Window 3")


def test_create(app):
    """An empty windowset can be created."""
    windowset = WindowSet(app)

    assert windowset.app == app
    assert len(windowset) == 0


def test_add_discard(app, window1, window2, window3):
    """An item can be added to a windowset"""
    windowset = WindowSet(app)
    windowset.add(window1)
    windowset.add(window2)
    assert len(windowset) == 2
    # Check the iterator works
    assert set(iter(windowset)) == {window1, window2}

    with pytest.raises(
        TypeError,
        match=r"Can only add objects of type toga.Window",
    ):
        windowset.add(object())

    windowset.add(window3)
    assert len(windowset) == 3
    assert window3 in windowset
    assert window3.app == app

    # Re-add the same window
    windowset.add(window3)
    assert len(windowset) == 3
    assert window3 in windowset
    assert window3.app == app

    # Discard the window
    windowset.discard(window3)
    assert window3 not in windowset

    # Duplicate discard - it's no longer a member
    with pytest.raises(
        ValueError,
        match=r"<toga.window.Window object at .*> is not part of this app",
    ):
        windowset.discard(window3)

    with pytest.raises(
        TypeError,
        match=r"Can only discard objects of type toga.Window",
    ):
        windowset.discard(object())


def test_add_discard_by_operator(app, window1, window2, window3):
    """An item can be added to a windowset by inline operators"""
    windowset = WindowSet(app)
    windowset.add(window1)
    windowset.add(window2)
    assert len(windowset) == 2

    with pytest.raises(
        TypeError,
        match=r"Can only add objects of type toga.Window",
    ):
        windowset += object()

    windowset += window3
    assert len(windowset) == 3
    assert window3 in windowset
    assert window3.app == app

    # Re-add the same window
    windowset += window3
    assert len(windowset) == 3
    assert window3 in windowset
    assert window3.app == app

    # Discard the window
    windowset -= window3
    assert window3 not in windowset

    # Duplicate discard - it's no longer a member
    with pytest.raises(
        ValueError,
        match=r"<toga.window.Window object at .*> is not part of this app",
    ):
        windowset -= window3

    with pytest.raises(
        TypeError,
        match=r"Can only discard objects of type toga.Window",
    ):
        windowset -= object()
