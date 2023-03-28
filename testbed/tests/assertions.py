from pytest import approx

from toga.colors import TRANSPARENT

NOT_PROVIDED = object()


def assert_set_get(obj, name, value, expected=NOT_PROVIDED):
    if expected is NOT_PROVIDED:
        expected = value

    setattr(obj, name, value)
    actual = getattr(obj, name)
    assert actual == expected
    return actual


def assert_color(actual, expected):
    if expected in {None, TRANSPARENT}:
        assert expected == actual
    else:
        if actual in {None, TRANSPARENT}:
            assert expected == actual
        else:
            assert (actual.r, actual.g, actual.b, actual.a) == (
                expected.r,
                expected.g,
                expected.b,
                approx(expected.a, abs=(1 / 255)),
            )
