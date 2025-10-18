from unittest.mock import Mock, call

from .style_classes import VALUE2, VALUE3, Style


def test_batched_apply():
    """With applicator, apply should batch calls to internal _apply."""
    style = Style()
    style._applicator = Mock()
    style.apply.reset_mock()
    style._apply.reset_mock()

    style.update(explicit_const=VALUE2, implicit=VALUE3)
    # Apply is called once for each property during update, but these calls are stored
    # and batched into one combined call to _apply.
    assert style.apply.mock_calls == [call("explicit_const"), call("implicit")]
    style._apply.assert_called_once_with({"explicit_const", "implicit"})

    style.apply.reset_mock()
    style._apply.reset_mock()


def test_batched_apply_no_names():
    """Batching doesn't do anything if no names were batched."""
    style = Style()
    style._applicator = Mock()
    style._apply.reset_mock()

    with style.batch_apply():
        pass

    style._apply.assert_not_called()


def test_batched_apply_nested():
    """Nesting batch_apply() does nothing; _apply is only called when all are exited."""
    style = Style()
    style._applicator = Mock()
    style._apply.reset_mock()

    with style.batch_apply():
        with style.batch_apply():
            style.update(explicit_const=VALUE2, implicit=VALUE3)

        style._apply.assert_not_called()

    style._apply.assert_called_once_with({"explicit_const", "implicit"})


def test_batched_apply_directional():
    """Assigning or deleting a directional property batches to _apply."""
    style = Style()
    style._applicator = Mock()
    style._apply.reset_mock()

    style.thing = 10
    style._apply.assert_called_once_with(
        {"thing_top", "thing_right", "thing_bottom", "thing_left"}
    )
    style._apply.reset_mock()

    del style.thing
    style._apply.assert_called_once_with(
        {"thing_top", "thing_right", "thing_bottom", "thing_left"}
    )
    style._apply.reset_mock()

    style.thing = (15, 15, 15, 15)
    style._apply.assert_called_once_with(
        {"thing_top", "thing_right", "thing_bottom", "thing_left"}
    )
    style._apply.reset_mock()

    style.thing = (0, 15, 15, 15)
    style._apply.assert_called_once_with({"thing_top"})
    style._apply.reset_mock()

    del style.thing
    style._apply.assert_called_once_with({"thing_right", "thing_bottom", "thing_left"})
