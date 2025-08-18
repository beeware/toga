####################################################################################
# The following tests confirm that the backwards compatibility for Toga 0.4.8 doesn't
# inadvertently catch and silence similar errors that aren't caused by the version
# mismatch.
#
# Testing the compatibility itself — that is, with Toga 0.4.8 — is separate, and is in
# compat/test_compat.py.
####################################################################################

from dataclasses import dataclass

import pytest

from travertino.layout import Viewport
from travertino.node import Node
from travertino.properties.validated import validated_property

from .test_node import Style
from .utils import mock_apply


class Applicator:
    def set_bounds(self):
        pass


@mock_apply
@dataclass(kw_only=True, repr=False)
class TypeErrorLayoutStyle(Style):
    # Uses the correct signature, but raises an unrelated TypeError in layout
    def layout(self, viewport):
        raise TypeError("An unrelated TypeError has occurred somewhere in layout()")


@mock_apply
@dataclass(kw_only=True, repr=False)
class OldTypeErrorLayoutStyle(Style):
    # Just to be extra safe, which this older signature too...
    def layout(self, node, viewport):
        raise TypeError("An unrelated TypeError has occurred somewhere in layout()")


@mock_apply
@dataclass(kw_only=True, repr=False)
class TypeErrorApplyStyle(Style):
    # Can't use the inherited int_prop, because style properties are locked to their
    # specific class
    test_prop = validated_property(integer=True)

    def apply(self, name=None):
        raise TypeError("An unrelated TypeError has occurred somewhere in apply()")


@pytest.mark.parametrize("StyleClass", [TypeErrorLayoutStyle, OldTypeErrorLayoutStyle])
def test_type_error_in_layout(StyleClass):
    """A TypeError in a style's layout() method should propagate."""
    node = Node(style=StyleClass(), applicator=Applicator())
    with pytest.raises(TypeError, match=r"unrelated TypeError"):
        node.refresh(Viewport(50, 50))


def test_type_error_in_apply():
    """A TypeError in a style's apply() method should raise a RuntimeError.

    Yes, this should be hit by the three tests below, but it's tested here separately
    just to be thorough.
    """
    style = TypeErrorApplyStyle()
    with pytest.raises(TypeError, match=r"unrelated TypeError"):
        style.apply()


def test_type_error_in_applicator_assignment():
    """A TypeError in apply() raises a RuntimeError during applicator assignment."""
    style = TypeErrorApplyStyle()
    with pytest.raises(RuntimeError, match=r"Failed to apply style"):
        style._applicator = Applicator()


def test_type_error_in_set():
    """A TypeError in a property's __set__() method should propagate."""
    style = TypeErrorApplyStyle()
    with pytest.raises(TypeError, match=r"unrelated TypeError"):
        style.test_prop = 3


def test_type_error_in_delete():
    """A TypeError in a property's __delete__() method should propagate."""
    style = TypeErrorApplyStyle()
    # Assign to underlying attribute, so that __delete__() won't simply abort.
    style._test_prop = 3
    with pytest.raises(TypeError, match=r"unrelated TypeError"):
        del style.test_prop
