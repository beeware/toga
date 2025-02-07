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


def assert_window_gain_focus(window, trigger_expected=True):
    on_gain_focus_handler = window.on_gain_focus._raw
    on_lose_focus_handler = window.on_lose_focus._raw
    if trigger_expected:
        on_gain_focus_handler.assert_called_once_with(window)
    else:
        on_gain_focus_handler.assert_not_called()
    on_lose_focus_handler.assert_not_called()

    on_gain_focus_handler.reset_mock()
    on_lose_focus_handler.reset_mock()


def assert_window_lose_focus(window, trigger_expected=True):
    on_gain_focus_handler = window.on_gain_focus._raw
    on_lose_focus_handler = window.on_lose_focus._raw
    if trigger_expected:
        on_lose_focus_handler.assert_called_once_with(window)
    else:
        on_lose_focus_handler.assert_not_called()
    on_gain_focus_handler.assert_not_called()

    on_gain_focus_handler.reset_mock()
    on_lose_focus_handler.reset_mock()


def assert_window_on_show(window, trigger_expected=True):
    on_show_handler = window.on_show._raw
    on_hide_handler = window.on_hide._raw
    if trigger_expected:
        on_show_handler.assert_called_once_with(window)
    else:
        on_show_handler.assert_not_called()
    on_hide_handler.assert_not_called()

    on_show_handler.reset_mock()
    on_hide_handler.reset_mock()


def assert_window_on_hide(window, trigger_expected=True):
    on_show_handler = window.on_show._raw
    on_hide_handler = window.on_hide._raw
    if trigger_expected:
        on_hide_handler.assert_called_once_with(window)
    else:
        on_hide_handler.assert_not_called()
    on_show_handler.assert_not_called()

    on_show_handler.reset_mock()
    on_hide_handler.reset_mock()
