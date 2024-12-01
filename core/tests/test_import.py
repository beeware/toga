import sys

import pytest


def test_lazy_succeed(monkeypatch):
    """Submodules are imported on demand."""
    for mod_name in ["toga", "toga.documents", "toga.widgets.button"]:
        monkeypatch.delitem(sys.modules, mod_name, raising=False)

    # A clean import of the top-level toga module should not import any submodules.
    import toga

    assert "toga.documents" not in sys.modules
    assert "toga.widgets.button" not in sys.modules

    # Accessing a name should import only the necessary submodules.
    Button = toga.Button
    assert "toga.widgets.button" in sys.modules
    assert "toga.documents" not in sys.modules

    # Accessing a name multiple times should return the same object.
    assert Button is toga.Button
    assert Button is sys.modules["toga.widgets.button"].Button

    # Same again with a different module.
    Document = toga.Document
    assert Document is sys.modules["toga.documents"].Document


def test_lazy_fail():
    """Nonexistent names should raise a normal AttributeError."""
    import toga

    with pytest.raises(
        AttributeError, match="module 'toga' has no attribute 'nonexistent'"
    ):
        toga.nonexistent
