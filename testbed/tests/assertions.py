from pytest import approx


# This could be generalized in future to accept syntax like:
#   * assert_set_get(obj, name, pytest.approx(value)) - for floating point values
#   * assert_set_get(obj, name, set_value, get_value) - where the two values are different
def assert_set_get(obj, name, value):
    """Calls a setter, then asserts that the same value is returned by the getter."""
    setattr(obj, name, value)
    assert getattr(obj, name) == value


def assert_color(actual, expected):
    for component in ["r", "g", "b"]:
        assert getattr(actual, component) == getattr(
            expected, component
        ), f"actual={actual} != expected={expected}"
    assert actual.a == approx(
        expected.a, abs=(1 / 255)
    ), f"actual={actual} != expected={expected}"
