from unittest.mock import Mock

import pytest

from toga.sources import ListSource, Row


@pytest.fixture
def source():
    return ListSource(
        data=[
            {"val1": "first", "val2": 111},
            {"val1": "second", "val2": 222},
            {"val1": "third", "val2": 333},
        ],
        accessors=["val1", "val2"],
    )


@pytest.mark.parametrize(
    "value",
    [
        None,
        42,
        "not a list",
    ],
)
def test_invalid_accessors(value):
    """Accessors for a list source must be a list of attribute names."""
    with pytest.raises(
        ValueError,
        match=r"accessors should be a list of attribute names",
    ):
        ListSource(accessors=value)


def test_accessors_required():
    """A list source must specify *some* accessors."""
    with pytest.raises(
        ValueError,
        match=r"ListSource must be provided a list of accessors",
    ):
        ListSource(accessors=[], data=[1, 2, 3])


def test_accessors_copied():
    """A list source must specify *some* accessors."""
    accessors = ["foo", "bar"]
    source = ListSource(accessors)

    assert source._accessors == ["foo", "bar"]

    # The accessors have been copied.
    accessors.append("whiz")
    assert source._accessors == ["foo", "bar"]


def test_empty_source():
    """A list source can be constructed with no data."""
    source = ListSource(accessors=["foo", "bar"])

    assert len(source) == 0


def test_tuples():
    """A ListSource can be instantiated with tuples."""
    source = ListSource(
        data=[
            ("first", 111),
            ("second", 222),
            ("third", 333),
        ],
        accessors=["val1", "val2"],
    )

    assert len(source) == 3

    assert source[0].val1 == "first"
    assert source[0].val2 == 111

    assert source[1].val1 == "second"
    assert source[1].val2 == 222

    listener = Mock()
    source.add_listener(listener)

    # Set element 1
    source[1] = ("new element", 999)

    # source is the same size, but has different data
    assert len(source) == 3
    assert source[1].val1 == "new element"
    assert source[1].val2 == 999

    listener.insert.assert_called_once_with(index=1, item=source[1])


def test_list():
    """A ListSource can be instantiated with lists."""
    source = ListSource(
        data=[
            ["first", 111],
            ["second", 222],
            ["third", 333],
        ],
        accessors=["val1", "val2"],
    )

    assert len(source) == 3

    assert source[0].val1 == "first"
    assert source[0].val2 == 111

    assert source[1].val1 == "second"
    assert source[1].val2 == 222

    listener = Mock()
    source.add_listener(listener)

    # Set element 1
    source[1] = ["new element", 999]

    # source is the same size, but has different data
    assert len(source) == 3
    assert source[1].val1 == "new element"
    assert source[1].val2 == 999

    listener.insert.assert_called_once_with(index=1, item=source[1])


def test_dict():
    """A ListSource can be instantiated with dictionaries."""
    source = ListSource(
        data=[
            {"val1": "first", "val2": 111},
            {"val1": "second", "val2": 222},
            {"val1": "third", "val2": 333},
        ],
        accessors=["val1", "val2"],
    )

    assert len(source) == 3

    assert source[0].val1 == "first"
    assert source[0].val2 == 111

    assert source[1].val1 == "second"
    assert source[1].val2 == 222

    listener = Mock()
    source.add_listener(listener)

    # Set element 1
    source[1] = ["new element", 999]

    # source is the same size, but has different data
    assert len(source) == 3
    assert source[1].val1 == "new element"
    assert source[1].val2 == 999

    listener.insert.assert_called_once_with(index=1, item=source[1])


def test_flat_list():
    """A list source can be created from a flat list of objects."""

    class MyObject:
        def __init__(self, info):
            self.info = info

        def __str__(self):
            return "string value %s" % self.info

    data = [
        MyObject(True),
        MyObject(2),
        MyObject("string"),
    ]

    source = ListSource(
        data=data,
        accessors=["col1"],
    )

    for i, row in enumerate(source):
        assert row.col1 == data[i]


def test_flat_list_numbers():
    """A list source can be created from a flat list of numbers."""

    data = [
        100,
        200.0,
        -3.14,
    ]

    source = ListSource(
        data=data,
        accessors=["col1"],
    )

    for i, row in enumerate(source):
        assert row.col1 == data[i]


def test_flat_list_strings():
    """A list source can be created from a flat list of numbers."""

    data = [
        "xxx",
        "yyy",
        "zzz",
    ]

    source = ListSource(
        data=data,
        accessors=["col1"],
    )

    for i, row in enumerate(source):
        assert row.col1 == data[i]


def test_iter(source):
    """A list source can be iterated over."""
    result = 0
    for row in source:
        result += row.val2

    assert result == 666


def test_clear(source):
    """A list source can be cleared."""

    assert len(source) == 3

    listener = Mock()
    source.add_listener(listener)

    # Clear the list
    source.clear()

    # List is empty
    assert len(source) == 0

    # A notification was sent
    listener.clear.assert_called_once_with()


def test_insert_kwarg(source):
    """You can insert into a list source using kwargs."""

    listener = Mock()
    source.add_listener(listener)

    # Insert the new element
    row = source.insert(1, dict(val1="new element", val2=999))

    assert len(source) == 4
    assert source[1] == row
    assert row.val1 == "new element"
    assert row.val2 == 999

    listener.insert.assert_called_once_with(index=1, item=row)


def test_insert_positional(source):
    """You can insert into a list source using positional args."""
    listener = Mock()
    source.add_listener(listener)

    # Insert the new element using positional args.
    # The values are mapped to the accessors in order.
    row = source.insert(1, ("new element", 999))

    assert len(source) == 4
    assert source[1] == row
    assert row.val1 == "new element"
    assert row.val2 == 999

    listener.insert.assert_called_once_with(index=1, item=row)


def test_append_dict(source):
    """You can append onto a list source using a dictionary."""

    listener = Mock()
    source.add_listener(listener)

    # Append the new element
    row = source.append(dict(val1="new element", val2=999))

    assert len(source) == 4
    assert source[3] == row
    assert row.val1 == "new element"
    assert row.val2 == 999

    listener.insert.assert_called_once_with(index=3, item=row)


def test_append_positional(source):
    """You can append onto a list source using positional args."""
    listener = Mock()
    source.add_listener(listener)

    # Append the new element using positional args.
    # The values are mapped to the accessors in order.
    row = source.append(("new element", 999))

    assert len(source) == 4
    assert source[3] == row
    assert row.val1 == "new element"
    assert row.val2 == 999

    listener.insert.assert_called_once_with(index=3, item=row)


def test_del(source):
    """You can delete an item from a list source by index."""
    listener = Mock()
    source.add_listener(listener)

    # Delete the second element
    row = source[1]
    del source[1]

    assert len(source) == 2
    assert source[0].val1 == "first"
    assert source[0].val2 == 111

    assert source[1].val1 == "third"
    assert source[1].val2 == 333

    listener.remove.assert_called_once_with(item=row, index=1)


def test_remove(source):
    """You can remove an item from a list source."""
    listener = Mock()
    source.add_listener(listener)

    # Remove the second element
    row = source[1]
    source.remove(row)

    assert len(source) == 2
    assert source[0].val1 == "first"
    assert source[0].val2 == 111

    assert source[1].val1 == "third"
    assert source[1].val2 == 333

    listener.remove.assert_called_once_with(item=row, index=1)


def test_index(source):
    """You can get the index of any row within a list source."""
    for i, row in enumerate(source):
        assert i == source.index(row)

    # look-alike rows are not equal, so index lookup should fail
    lookalike_row = Row(val1="second", val2=222)
    with pytest.raises(
        ValueError,
        match=r"<Row .* val1='second' val2=222> is not in list",
    ):
        source.index(lookalike_row)

    with pytest.raises(
        ValueError,
        match=r"None is not in list",
    ):
        source.index(None)

    with pytest.raises(
        ValueError,
        match=r"<Row .* \(no attributes\)> is not in list",
    ):
        source.index(Row())


def test_find(source):
    """You can find the index of any matching row within a list source."""

    # Duplicate row 1 of the data.
    source.append(dict(val1="second", val2=222))

    # A unique row can be found
    assert source.find(dict(val1="third", val2=333)) == source[2]

    # A unique row can be found, using implied accessor order
    assert source.find(("third", 333)) == source[2]

    # A unique row can be found, using only the first accessor
    assert source.find("third") == source[2]

    # If data isn't unique, the first match is returned
    assert source.find(dict(val1="second", val2=222)) == source[1]

    # The search can start after a given instance
    assert source.find(dict(val1="second", val2=222), start=source[1]) == source[3]

    # A partial match is enough
    assert source.find(dict(val1="third")) == source[2]

    # find will fail if the object doesn't exist
    with pytest.raises(
        ValueError,
        match=r"No row matching {'val1': 'not there', 'val2': 999} in data",
    ):
        source.find(dict(val1="not there", val2=999))

    # An overspecified search will fail
    with pytest.raises(
        ValueError,
        match=r"No row matching {'val1': 'first', 'val2': 111, 'value': 'overspecified'} in data",
    ):
        source.find(dict(val1="first", val2=111, value="overspecified"))
