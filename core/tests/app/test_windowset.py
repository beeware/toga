import pytest

import toga
from toga.app import WindowSet


@pytest.fixture
def window1(app):
    return toga.Window(title="Window 1", id="a-win")


@pytest.fixture
def window2(app):
    return toga.Window(title="Window 2", id="z-win")


def test_create(app):
    """An empty windowset can be created."""
    windowset = WindowSet(app)

    assert windowset.app == app
    assert len(windowset) == 0


def test_add_discard(app, window1, window2):
    """An item can be added to a windowset."""
    # The windowset has 3 windows - the main window, plus 2 extras
    assert len(app.windows) == 3

    # Check the iterator and sorting works
    assert sorted(iter(app.windows)) == [window1, app.main_window, window2]

    with pytest.raises(
        TypeError,
        match=r"Can only add objects of type toga.Window",
    ):
        app.windows.add(object())

    # Explicitly re-add a window that is already in the windowset
    app.windows.add(window2)
    assert len(app.windows) == 3
    assert window2 in app.windows
    assert window2.app == app

    # Explicitly discard a window that is in the windowset
    app.windows.discard(window2)
    assert window2 not in app.windows

    # Duplicate discard - it's no longer a member
    with pytest.raises(
        ValueError,
        match=r"<toga.window.Window object at .*> is not part of this app",
    ):
        app.windows.discard(window2)

    with pytest.raises(
        TypeError,
        match=r"Can only discard objects of type toga.Window",
    ):
        app.windows.discard(object())
