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


def assert_window_event_triggered(window, expected_event=None):
    window_events = {
        window.on_gain_focus,
        window.on_lose_focus,
        window.on_show,
        window.on_hide,
    }
    unexpected_events = window_events - {expected_event}

    if expected_event:
        expected_event._raw.assert_called_once_with(window)

    for unexpected_event in unexpected_events:
        if unexpected_event._raw is not None:
            unexpected_event._raw.assert_not_called()

    for event in window_events:
        if event._raw is not None:
            event._raw.reset_mock()
