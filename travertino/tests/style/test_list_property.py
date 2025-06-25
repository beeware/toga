from collections.abc import Sequence

import pytest

from travertino.properties.immutablelist import ImmutableList

from .style_classes import VALUE1, VALUE2, VALUE3, Style


@pytest.mark.parametrize(
    "value, expected",
    [
        ([VALUE1], [VALUE1]),
        (VALUE1, [VALUE1]),
        ([VALUE1, VALUE3], [VALUE1, VALUE3]),
        ([VALUE2, VALUE1], [VALUE2, VALUE1]),
        ([VALUE2, VALUE3, 1, 2, VALUE1], [VALUE2, VALUE3, 1, 2, VALUE1]),
        # Duplicates are kept, but "normalized" via validation.
        (
            [VALUE3, 1, VALUE3, "1", True, " 1", VALUE2],
            [VALUE3, 1, VALUE3, 1, 1, 1, VALUE2],
        ),
        # Other sequences should work too.
        ((VALUE1, VALUE3), [VALUE1, VALUE3]),
    ],
)
def test_list_property(value, expected):
    style = Style()
    style.list_prop = value
    assert style.list_prop == expected


@pytest.mark.parametrize(
    "value, error, match",
    [
        (
            5,
            TypeError,
            r"Value for list property list_prop must be a sequence\.",
        ),
        (
            # Fails because it's only a generator, not a comprehension:
            (i for i in [VALUE1, VALUE3]),
            TypeError,
            r"Value for list property list_prop must be a sequence.",
        ),
        (
            [VALUE3, VALUE1, "bogus"],
            ValueError,
            r"Invalid item value 'bogus' for list property list_prop; "
            r"Valid values are: none, value1, value2, value3, <integer>",
        ),
        (
            (),
            ValueError,
            r"List properties cannot be set to an empty sequence; "
            r"to reset a property, use del `style.list_prop`\.",
        ),
        (
            [],
            ValueError,
            r"List properties cannot be set to an empty sequence; "
            r"to reset a property, use del `style.list_prop`\.",
        ),
    ],
)
def test_list_property_invalid(value, error, match):
    style = Style()
    with pytest.raises(error, match=match):
        style.list_prop = value


def test_list_property_immutable():
    style = Style()
    style.list_prop = [1, 2, 3, VALUE2]
    prop = style.list_prop

    with pytest.raises(TypeError, match=r"does not support item assignment"):
        prop[0] = 5

    with pytest.raises(TypeError, match=r"doesn't support item deletion"):
        del prop[1]

    with pytest.raises(AttributeError):
        prop.insert(2, VALUE1)

    with pytest.raises(AttributeError):
        prop.append(VALUE3)

    with pytest.raises(AttributeError):
        prop.clear()

    with pytest.raises(AttributeError):
        prop.reverse()

    with pytest.raises(AttributeError):
        prop.pop()

    with pytest.raises(AttributeError):
        prop.remove(VALUE2)

    with pytest.raises(AttributeError):
        prop.extend([5, 6, 7])

    with pytest.raises(TypeError, match=r"unsupported operand type\(s\)"):
        prop += [4, 3, VALUE1]

    with pytest.raises(TypeError, match=r"unsupported operand type\(s\)"):
        prop += ImmutableList([4, 3, VALUE1])

    with pytest.raises(AttributeError):
        prop.sort()


def test_list_property_list_like():
    style = Style()
    style.list_prop = [1, 2, 3, VALUE2]
    prop = style.list_prop

    assert isinstance(prop, ImmutableList)
    assert prop == [1, 2, 3, VALUE2]
    assert prop == ImmutableList([1, 2, 3, VALUE2])
    assert prop[2] == 3
    assert str(prop) == repr(prop) == "[1, 2, 3, 'value2']"
    assert len(prop) == 4

    count = 0
    for _ in prop:
        count += 1
    assert count == 4

    assert [*reversed(prop)] == [VALUE2, 3, 2, 1]

    assert prop.index(3) == 2

    assert prop.count(VALUE2) == 1

    assert isinstance(prop, Sequence)
