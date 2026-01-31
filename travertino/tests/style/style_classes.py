from __future__ import annotations

from dataclasses import dataclass
from warnings import catch_warnings, filterwarnings

from travertino.properties.aliased import Condition, aliased_property
from travertino.properties.choices import Choices
from travertino.properties.shorthand import composite_property, directional_property
from travertino.properties.validated import list_property, validated_property
from travertino.style import BaseStyle

from ..utils import mock_apply

VALUE1 = "value1"
VALUE2 = "value2"
VALUE3 = "value3"
VALUE4 = "value4"
VALUES = [VALUE1, VALUE2, VALUE3, None]


@mock_apply
@dataclass(kw_only=True, repr=False)
class Style(BaseStyle):
    def _apply(self, names):
        pass

    def layout(self, viewport):
        pass

    #############################
    # Simple validated properties
    #############################

    # Some properties with explicit initial values
    explicit_const: str | int = validated_property(
        *VALUES, integer=True, initial=VALUE1
    )
    explicit_value: str | int = validated_property(*VALUES, integer=True, initial=0)
    explicit_none: str | int | None = validated_property(
        *VALUES, integer=True, initial=None
    )

    # A property with an implicit default value.
    # This usually means the default is platform specific.
    implicit: str | int | None = validated_property(
        VALUE1, VALUE2, VALUE3, integer=True
    )

    #############
    # Directional
    #############

    thing: tuple[str | int] | str | int = directional_property("thing{}")
    thing_top: str | int = validated_property(*VALUES, integer=True, initial=0)
    thing_right: str | int = validated_property(*VALUES, integer=True, initial=0)
    thing_bottom: str | int = validated_property(*VALUES, integer=True, initial=0)
    thing_left: str | int = validated_property(*VALUES, integer=True, initial=0)

    # Nothing below here needs to be tested in deprecated API:

    ######
    # List
    ######

    list_prop: list[str] = list_property(*VALUES, integer=True, initial=(VALUE2,))

    ###########
    # Composite
    ###########

    different_values_prop: str = validated_property(
        VALUE2, VALUE3, VALUE4, initial=VALUE2
    )

    composite_no_optional: tuple[str] = composite_property(
        optional=(), required=("explicit_const", "explicit_value")
    )
    composite_optional: tuple[str] = composite_property(
        optional=("explicit_none", "different_values_prop"),
        required=("explicit_const", "explicit_value"),
    )
    composite_different_lengths: tuple[str] = composite_property(
        optional=("explicit_none", "different_values_prop", "explicit_const"),
        required=("explicit_value",),
    )

    #########
    # Aliases
    #########

    plain_alias: str | int = aliased_property(source="explicit_const")
    plain_alias_deprecated: str | int = aliased_property(
        source="explicit_const", deprecated=True
    )
    directional_alias: tuple[str | int] | str | int = aliased_property(source="thing")
    directional_alias_deprecated: tuple[str | int] | str | int = aliased_property(
        source="thing", deprecated=True
    )
    conditional_alias: str | int = aliased_property(
        source={
            Condition(thing_top=0): "explicit_const",
            Condition(thing_top=10, list_prop=[VALUE1, VALUE2]): "explicit_value",
            Condition(thing_top=10, list_prop=[VALUE1]): "explicit_none",
        }
    )
    conditional_alias_deprecated: str | int = aliased_property(
        source={
            Condition(thing_top=0): "explicit_const",
            Condition(thing_top=10, list_prop=[VALUE1, VALUE2]): "explicit_value",
            Condition(thing_top=10, list_prop=[VALUE1]): "explicit_none",
        },
        deprecated=True,
    )


########################################
# Backwards compatibility for Toga < 0.5
########################################

VALUE_CHOICES = Choices(*VALUES, integer=True)

with catch_warnings():
    filterwarnings("ignore", category=DeprecationWarning)

    @mock_apply
    class DeprecatedStyle(BaseStyle):
        def _apply(self, names):
            pass

        def layout(self, viewport):
            pass

    # Some properties with explicit initial values
    DeprecatedStyle.validated_property(
        "explicit_const", choices=VALUE_CHOICES, initial=VALUE1
    )
    DeprecatedStyle.validated_property(
        "explicit_value", choices=VALUE_CHOICES, initial=0
    )
    DeprecatedStyle.validated_property(
        "explicit_none", choices=VALUE_CHOICES, initial=None
    )

    # A property with an implicit default value.
    # This usually means the default is platform specific.
    DeprecatedStyle.validated_property(
        "implicit", choices=Choices(VALUE1, VALUE2, VALUE3, integer=True)
    )

    # A set of directional properties
    DeprecatedStyle.validated_property("thing_top", choices=VALUE_CHOICES, initial=0)
    DeprecatedStyle.validated_property("thing_right", choices=VALUE_CHOICES, initial=0)
    DeprecatedStyle.validated_property("thing_bottom", choices=VALUE_CHOICES, initial=0)
    DeprecatedStyle.validated_property("thing_left", choices=VALUE_CHOICES, initial=0)
    DeprecatedStyle.directional_property("thing%s")
