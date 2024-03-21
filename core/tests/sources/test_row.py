from unittest.mock import Mock

from toga.sources import Row


def test_row():
    """A row can be created and modified."""
    source = Mock()
    row = Row(val1="value 1", val2=42)
    # Set a source.
    row._source = source

    # initial values are as expected
    assert row.val1 == "value 1"
    assert row.val2 == 42

    # An existing attribute can be updated.
    row.val1 = "new value"
    assert row.val1 == "new value"
    source.notify.assert_called_once_with("change", item=row)
    source.notify.reset_mock()

    # Deleting an attribute causes a change notification
    del row.val1
    assert not hasattr(row, "val1")
    source.notify.assert_called_once_with("change", item=row)
    source.notify.reset_mock()

    # Setting an attribute with an underscore isn't a notifiable event
    row._secret = "secret value"
    assert row._secret == "secret value"
    source.notify.assert_not_called()

    # An attribute that wasn't in the original attribute set
    # still causes a change notification
    row.val3 = "other value"
    assert row.val3 == "other value"
    source.notify.assert_called_once_with("change", item=row)
    source.notify.reset_mock()

    # Deleting an attribute that wasn't in the original attribute set
    # still causes a change notification
    del row.val3
    assert not hasattr(row, "val")
    source.notify.assert_called_once_with("change", item=row)
    source.notify.reset_mock()


def test_row_without_source():
    """A row with no source can be created and modified."""
    row = Row(val1="value 1", val2=42)

    # initial values are as expected
    assert row.val1 == "value 1"
    assert row.val2 == 42

    # An existing attribute can be updated.
    row.val1 = "new value"
    assert row.val1 == "new value"

    # Deleting an attribute causes a change notification
    del row.val1
    assert not hasattr(row, "val1")

    # Setting an attribute starting with an underscore isn't a notifiable event
    row._secret = "secret value"
    assert row._secret == "secret value"

    # An attribute that wasn't in the original attribute set
    # still causes a change notification
    row.val3 = "other value"
    assert row.val3 == "other value"

    # Deleting an attribute that wasn't in the original attribute set
    # still causes a change notification
    del row.val3
    assert not hasattr(row, "val")
