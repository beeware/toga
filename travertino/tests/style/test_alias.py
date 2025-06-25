import re
from contextlib import nullcontext
from functools import partial

import pytest

from .style_classes import VALUE1, VALUE2, VALUE3, Style


@pytest.mark.parametrize(
    "source, alias, initial, value, context",
    [
        (
            "explicit_const",
            "plain_alias",
            VALUE1,
            VALUE3,
            nullcontext,
        ),
        (
            "explicit_const",
            "plain_alias_deprecated",
            VALUE1,
            VALUE3,
            partial(
                pytest.deprecated_call,
                match=(
                    r"Style\.plain_alias_deprecated is deprecated\. "
                    r"Use Style\.explicit_const instead\."
                ),
            ),
        ),
        # There *shouldn't* be anything special about an alias to a
        # directional_property vs. to a validated_property, but it doesn't hurt to
        # check.
        (
            "thing",
            "directional_alias",
            (0, 0, 0, 0),
            (10, 5, 10, 5),
            nullcontext,
        ),
        (
            "thing",
            "directional_alias_deprecated",
            (0, 0, 0, 0),
            (10, 5, 10, 5),
            partial(
                pytest.deprecated_call,
                match=(
                    r"Style\.directional_alias_deprecated is deprecated\. "
                    r"Use Style\.thing instead\."
                ),
            ),
        ),
    ],
)
def test_simple_alias(source, alias, initial, value, context):
    """An alias with a constant source refers consistently to the source property."""
    style = Style()

    # Set on original, check on alias
    with context():
        assert alias not in style

    style[source] = value

    with context():
        assert alias in style
    with context():
        assert style[alias] == value

    del style[source]

    with context():
        assert alias not in style
    with context():
        assert style[alias] == initial

    # Set on alias, check on original.
    assert source not in style

    with context():
        style[alias] = value

    assert source in style
    assert style[source] == value

    with context():
        del style[alias]

    assert source not in style
    assert style[source] == initial


@pytest.mark.parametrize(
    "alias, context",
    [
        ("conditional_alias", nullcontext),
        ("conditional_alias_deprecated", pytest.deprecated_call),
    ],
)
@pytest.mark.parametrize(
    "properties, source, value",
    [
        ({}, "explicit_const", VALUE1),
        ({"thing_top": 10, "list_prop": [VALUE1, VALUE2]}, "explicit_value", 0),
        ({"thing_top": 10, "list_prop": [VALUE1]}, "explicit_none", None),
    ],
)
def test_conditional_alias(alias, context, properties, source, value):
    """An alias correctly checks conditions to determine which property to access."""
    style = Style(**properties)
    with context():
        assert style[alias] == style[source] == value


@pytest.mark.parametrize(
    "alias",
    # No deprecation warnings are given; there's no way to even tell which newer name
    # should be instead.
    ["conditional_alias", "conditional_alias_deprecated"],
)
@pytest.mark.parametrize(
    "properties",
    [
        {"thing_top": 1},
        {"thing_top": 10, "list_prop": [VALUE1, VALUE3]},
        {"thing_top": 11},
    ],
)
def test_conditional_alias_invald(alias, properties):
    """If no condition is valid, using the alias raises an AttributeError."""
    error_msg = re.escape(
        f"'{alias}' is only supported when (thing_top == 0) or (thing_top == 10; "
        "list_prop == ['value1', 'value2']) or (thing_top == 10; list_prop == "
        "['value1'])"
    )
    style = Style(**properties)
    with pytest.raises(AttributeError, match=error_msg):
        _ = style[alias]

    with pytest.raises(AttributeError, match=error_msg):
        style[alias] = 15

    with pytest.raises(AttributeError, match=error_msg):
        _ = alias in style

    with pytest.raises(AttributeError, match=error_msg):
        del style[alias]


@pytest.mark.parametrize(
    "alias, context",
    [
        ("conditional_alias", nullcontext),
        ("conditional_alias_deprecated", pytest.deprecated_call),
    ],
)
@pytest.mark.parametrize(
    "properties",
    [
        {"alias": 1, "thing_top": 10, "list_prop": [VALUE1]},
        {"thing_top": 10, "alias": 1, "list_prop": [VALUE1]},
        {"thing_top": 10, "list_prop": [VALUE1], "alias": 1},
    ],
)
def test_conditional_alias_simultaneous_setting(alias, context, properties):
    """Setting an alias along with its conditions works, in any order."""
    properties = {
        (alias if name == "alias" else name): value
        for name, value in properties.items()
    }
    with context():
        style = Style(**properties)
    with context():
        assert style[alias] == 1

    style = Style()
    with context():
        style.update(**properties)
    with context():
        assert style[alias] == 1
