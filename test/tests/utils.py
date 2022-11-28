from pytest import approx

from toga.colors import rgba

# TODO: add non-ASCII strings.
TEXTS = ["", " ", "a", "ab", "abc", "hello world", "hello\nworld"]


# TODO: include None
components = [0, 1, 2, 128, 253, 254, 255]
COLORS = [
    rgba(r, g, b, a)
    for r in components
    for g in components
    for b in components
    for a in [0.0, 0.01, 0.1, 0.5, 0.9, 0.99, 1.0]
]


# This could be generalized in future to accept syntax like:
#   * assert_set_get(obj, name, pytest.approx(value)) - for floating point values
#   * assert_set_get(obj, name, set_value, get_value) - where the two values are different
def assert_set_get(obj, name, value):
    """Calls a setter, then asserts that the same value is returned by the getter."""
    setattr(obj, name, value)
    assert getattr(obj, name) == value


def assert_color(actual, expected):
    for component in ["r", "g", "b"]:
        assert getattr(actual, component) == getattr(expected, component)
    assert actual.a == approx(expected.a, abs=(1 / 255))
