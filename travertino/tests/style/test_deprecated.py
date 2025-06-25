from unittest.mock import Mock

import pytest

from travertino.properties.choices import Choices

from ..utils import apply_dataclass, mock_apply
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
@apply_dataclass
class MockedApplyStyle(BaseStyle):
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
    """Reapply() is deprecated (but still calls apply()."""
    style = Style()
    with pytest.warns(DeprecationWarning):
        style.reapply()

    style.apply.assert_called_once_with()


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
