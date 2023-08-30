from unittest.mock import Mock

from toga.sources import Row


def test_row():
    "A row can be created and modified"
    source = Mock()
    row = Row(val1="value 1", val2=42)
    row._source = source

    assert row.val1 == "value 1"
    assert row.val2 == 42

    row.val1 = "new value"
    source.notify.assert_called_once_with("change", item=row)
    source.notify.reset_mock()

    # An attribute that wasn't in the original attribute set
    # still causes a change notification
    row.val3 = "other value"
    source.notify.assert_called_once_with("change", item=row)
    source.notify.reset_mock()
