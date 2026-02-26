from dataclasses import dataclass
from unittest.mock import Mock, call

import pytest

from travertino.properties.choices import Choices

from ..utils import mock_apply
from .style_classes import (
    VALUE1,
    VALUE2,
    VALUE3,
    VALUES,
    BaseStyle,
    Style,
)

# Note: Other tests are parametrized with DeprecatedStyle; these are only the tests
# that *only* test deprecated behavior.


@mock_apply
@dataclass(kw_only=True, repr=False)
class MockedApplyStyle(BaseStyle):
    def _apply(self, names):
        pass

    def layout(self, viewport):
        pass


def test_deprecated_copy():
    style = MockedApplyStyle()

    with pytest.warns(DeprecationWarning):
        style_copy = style.copy(applicator=object())

    style_copy.apply.assert_called_once_with()


def test_deprecated_class_methods():
    """Toga < 0.5.0 can still define style properties with the old API."""

    class OldStyle(BaseStyle):
        pass

    with pytest.warns(DeprecationWarning):
        OldStyle.validated_property(
            "implicit", Choices(*VALUES, integer=True), initial=VALUE1
        )

    with pytest.warns(DeprecationWarning):
        OldStyle.directional_property("thing%s")


def test_deprecated_reapply():
    """Reapply() is deprecated, and calls the old apply(name, value) signature."""
    style = Style()
    with pytest.warns(DeprecationWarning):
        style.reapply()

    # Applies all properties
    assert sorted(style.apply.call_args_list) == [
        call("different_values_prop", "value2"),
        call("explicit_const", VALUE1),
        call("explicit_none", None),
        call("explicit_value", 0),
        call("implicit", None),
        call("list_prop", ["value2"]),
        call("thing_bottom", 0),
        call("thing_left", 0),
        call("thing_right", 0),
        call("thing_top", 0),
    ]


def test_deprecated_import():
    """Toga < 0.5.0 can still import what it needs from Travertino."""
    with pytest.deprecated_call():
        from travertino.declaration import BaseStyle, Choices  # noqa


def test_apply_deprecated():
    """Calling with more than one argument is deprecated."""
    style = Style(explicit_const=VALUE2, implicit=VALUE3)
    style._applicator = Mock()
    style._apply.reset_mock()

    with pytest.warns(
        DeprecationWarning,
        match=(
            r"Calling Style\.apply\(\) with multiple arguments is deprecated\. Use the "
            r'"with Style\.batch_apply\(\):" context manager instead\.'
        ),
    ):
        style.apply("explicit_const", "implicit")

    # Should still call down to _apply, though.
    style._apply.assert_called_once_with({"explicit_const", "implicit"})
