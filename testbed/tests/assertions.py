from pytest import approx

from toga.colors import TRANSPARENT


# This could be generalized in future to accept syntax like:
#   * assert_set_get(obj, name, pytest.approx(value)) - for floating point values
#   * assert_set_get(obj, name, set_value, get_value) - where the two values are different
def assert_set_get(obj, name, value):
    """Calls a setter, then asserts that the same value is returned by the getter.

    :param obj: The object to inspect
    :param name: The name of the attribute to set and get
    :param value: The value to set
    """
    setattr(obj, name, value)
    actual = getattr(obj, name)
    assert actual == value, f"Expected {value!r}, got {actual!r}"


def assert_color(actual, expected):
    if expected in [None, TRANSPARENT]:
        assert expected == actual
    else:
        if actual in [None, TRANSPARENT]:
            assert expected == actual
        else:
            assert all(
                [
                    getattr(actual, component) == getattr(expected, component)
                    for component in ["r", "g", "b"]
                ]
                + [actual.a == approx(expected.a, abs=(1 / 255))]
            ), f"Expected {expected}, got {actual}"
