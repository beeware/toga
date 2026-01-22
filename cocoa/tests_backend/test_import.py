import sys

import pytest


def test_lazy_succeed(monkeypatch):
    """Submodules are imported on demand."""
    for mod_name in ["toga_cocoa", "toga_cocoa.factory", "toga_cocoa.widgets.button"]:
        monkeypatch.delitem(sys.modules, mod_name, raising=False)

    # clean import of the top-level toga_cocoa module should not import any submodules.
    import toga_cocoa

    assert "toga_cocoa.factory" not in sys.modules
    assert "toga_cocoa.widgets.button" not in sys.modules

    # Accessing a name should import only the necessary submodules.
    Button = toga_cocoa.Button
    assert "toga_cocoa.factory" in sys.modules
    assert "toga_cocoa.widgets.button" in sys.modules

    # Accessing a name multiple times should return the same object.
    assert Button is toga_cocoa.Button
    assert Button is sys.modules["toga_cocoa.factory"].Button

    # Same again with a different attribute.
    App = toga_cocoa.App
    assert App is sys.modules["toga_cocoa.factory"].App

    assert hasattr(toga_cocoa, "Button")
    assert hasattr(toga_cocoa, "App")
    cached_button = toga_cocoa.Button
    assert cached_button is Button


def test_lazy_fail():
    """Nonexistent names should raise a normal AttributeError."""
    import toga_cocoa

    with pytest.raises(
        AttributeError, match="module 'toga_cocoa' has no attribute 'nonexistent'"
    ):
        _ = toga_cocoa.nonexistent


def test_lazy_load_cache(monkeypatch):
    import toga_cocoa

    if "Button" in toga_cocoa.__dict__:
        del toga_cocoa.__dict__["Button"]
    btn = toga_cocoa.Button
    assert btn is toga_cocoa.Button


def test_lazy_attribute_error(monkeypatch):
    import toga_cocoa

    with pytest.raises(
        AttributeError, match="module 'toga_cocoa' has no attribute 'nonexistent'"
    ):
        _ = toga_cocoa.nonexistent
