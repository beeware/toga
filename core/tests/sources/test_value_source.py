from unittest.mock import Mock

from toga.sources.value_source import ValueSource


def test_empty():
    """An empty ValueSource can be created."""
    source = ValueSource()

    assert source.accessor == "value"
    assert source.value is None
    assert str(source) == "None"


def test_value():
    """A ValueSource can be created with a value."""
    source = ValueSource(42)

    assert source.accessor == "value"
    assert source.value == 42
    assert str(source) == "42"


def test_value_with_accessor():
    """A ValueSource can be created with a custom accessor."""
    source = ValueSource(42, accessor="something")

    assert source.accessor == "something"
    assert source.something == 42
    assert str(source) == "42"


def test_listener():
    """A listener will be notified of ValueSource changes."""
    source = ValueSource(42)
    listener = Mock()

    source.add_listener(listener)

    source.value = 37

    listener.change.assert_called_once_with(item=37)

    # Reset the mock; clear the value
    listener.reset_mock()
    source.value = None

    listener.change.assert_called_once_with(item=None)

    # Reset the mock; set a *different* attribute on the source
    listener.reset_mock()
    source.something = 1234

    listener.change.assert_not_called()
