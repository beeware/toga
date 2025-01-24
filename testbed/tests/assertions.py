from pytest import approx

from toga.colors import TRANSPARENT, rgba

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


def reverse_alpha_blending_over(blended_color, back_color, original_alpha):
    # This is the reverse of the "over" operation and has
    # been derived from the "over" operation formula, see:
    # https://en.wikipedia.org/wiki/Alpha_compositing#Description

    if original_alpha == 0:
        return back_color
    else:
        front_color = rgba(
            round(
                (
                    (blended_color.r * blended_color.a)
                    - (back_color.r * back_color.a * (1 - original_alpha))
                )
                / original_alpha
            ),
            round(
                (
                    (blended_color.g * blended_color.a)
                    - (back_color.g * back_color.a * (1 - original_alpha))
                )
                / original_alpha
            ),
            round(
                (
                    (blended_color.b * blended_color.a)
                    - (back_color.b * back_color.a * (1 - original_alpha))
                )
                / original_alpha
            ),
            original_alpha,
        )
        return front_color


def assert_background_color(actual, expected):
    # For platforms where alpha blending is manually implemented, the
    # probe.background_color property returns a tuple consisting of:
    #   - The widget's background color
    #   - The widget's parent's background color
    #   - The widget's original alpha value - Required for deblending
    if isinstance(actual, tuple):
        actual_widget_bg, actual_parent_bg, actual_widget_bg_alpha = actual
        deblended_actual_widget_bg = reverse_alpha_blending_over(
            actual_widget_bg, actual_parent_bg, actual_widget_bg_alpha
        )
        if isinstance(expected, tuple):
            expected_widget_bg, expected_parent_bg, expected_widget_bg_alpha = expected
            deblended_expected_widget_bg = reverse_alpha_blending_over(
                expected_widget_bg, expected_parent_bg, expected_widget_bg_alpha
            )
            assert_color(deblended_actual_widget_bg, deblended_expected_widget_bg)
        # For comparison when expected is a single value object
        else:
            if (expected == TRANSPARENT) or (
                expected.a
                == 0
                # Since a color having an alpha value of 0 cannot be deblended to
                # get the exact original color, as deblending in such cases would
                # lead to a division by zero error. So, just check that widget and
                # parent have the same color.
            ):
                assert_color(actual_widget_bg, actual_parent_bg)
            elif expected.a != 1:
                assert_color(deblended_actual_widget_bg, expected)
            else:
                assert_color(actual_widget_bg, expected)
    # For other platforms
    else:
        assert_color(actual, expected)

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
