from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from toga.colors import ColorT

from travertino.constants import (  # noqa: F401
    BOLD,
    BOTTOM,
    CENTER,
    COLUMN,
    CURSIVE,
    END,
    FANTASY,
    HIDDEN,
    ITALIC,
    JUSTIFY,
    LEFT,
    LTR,
    MONOSPACE,
    NONE,
    NORMAL,
    OBLIQUE,
    RIGHT,
    ROW,
    RTL,
    SANS_SERIF,
    SERIF,
    SMALL_CAPS,
    START,
    SYSTEM,
    TOP,
    TRANSPARENT,
    VISIBLE,
)
from travertino.properties.aliased import Condition, aliased_property
from travertino.properties.shorthand import composite_property, directional_property
from travertino.properties.validated import list_property, validated_property

from toga.fonts import (
    FONT_STYLES,
    FONT_VARIANTS,
    FONT_WEIGHTS,
    SYSTEM_DEFAULT_FONT_SIZE,
    SYSTEM_DEFAULT_FONTS,
)

from .compat import _alignment_property
from .layout import PackMechanicsBase

NOT_PROVIDED = object()

PACK = "pack"


@dataclass(kw_only=True, repr=False)
class Pack(PackMechanicsBase):
    _doc_link = "[style properties](/reference/style/pack)"

    display: str = validated_property(PACK, NONE, initial=PACK)
    visibility: str = validated_property(VISIBLE, HIDDEN, initial=VISIBLE)
    direction: str = validated_property(ROW, COLUMN, initial=ROW)
    align_items: str | None = validated_property(START, CENTER, END)
    justify_content: str | None = validated_property(START, CENTER, END, initial=START)
    gap: int = validated_property(integer=True, initial=0)

    width: str | int = validated_property(NONE, integer=True, initial=NONE)
    height: str | int = validated_property(NONE, integer=True, initial=NONE)
    flex: float = validated_property(number=True, initial=0)

    margin: (
        int
        | tuple[int]
        | tuple[int, int]
        | tuple[int, int, int]
        | tuple[int, int, int, int]
    ) = directional_property("margin{}")
    margin_top: int = validated_property(integer=True, initial=0)
    margin_right: int = validated_property(integer=True, initial=0)
    margin_bottom: int = validated_property(integer=True, initial=0)
    margin_left: int = validated_property(integer=True, initial=0)

    color: ColorT | None = validated_property(color=True)
    background_color: ColorT | None = validated_property(TRANSPARENT, color=True)

    text_align: str | None = validated_property(LEFT, RIGHT, CENTER, JUSTIFY)
    text_direction: str | None = validated_property(RTL, LTR, initial=LTR)

    font_family: str | list[str] = list_property(
        *SYSTEM_DEFAULT_FONTS, string=True, initial=[SYSTEM]
    )
    font_style: str = validated_property(*FONT_STYLES, initial=NORMAL)
    font_variant: str = validated_property(*FONT_VARIANTS, initial=NORMAL)
    font_weight: str = validated_property(*FONT_WEIGHTS, initial=NORMAL)
    font_size: int = validated_property(integer=True, initial=SYSTEM_DEFAULT_FONT_SIZE)
    font: (
        tuple[int, list[str] | str]
        | tuple[str, int, list[str] | str]
        | tuple[str, str, int, list[str] | str]
        | tuple[str, str, str, int, list[str] | str]
    ) = composite_property(
        optional=("font_style", "font_variant", "font_weight"),
        required=("font_size", "font_family"),
    )

    ######################################################################
    # Directional aliases
    ######################################################################

    horizontal_align_content: str | None = aliased_property(
        source={Condition(direction=ROW): "justify_content"}
    )
    horizontal_align_items: str | None = aliased_property(
        source={Condition(direction=COLUMN): "align_items"}
    )
    vertical_align_content: str | None = aliased_property(
        source={Condition(direction=COLUMN): "justify_content"}
    )
    vertical_align_items: str | None = aliased_property(
        source={Condition(direction=ROW): "align_items"}
    )

    ######################################################################
    # 2024-12: Backwards compatibility for Toga < 0.5.0
    ######################################################################

    padding: (
        int
        | tuple[int]
        | tuple[int, int]
        | tuple[int, int, int]
        | tuple[int, int, int, int]
    ) = aliased_property(source="margin", deprecated=True)
    padding_top: int = aliased_property(source="margin_top", deprecated=True)
    padding_right: int = aliased_property(source="margin_right", deprecated=True)
    padding_bottom: int = aliased_property(source="margin_bottom", deprecated=True)
    padding_left: int = aliased_property(source="margin_left", deprecated=True)

    alignment: str | None = _alignment_property(TOP, RIGHT, BOTTOM, LEFT, CENTER)

    ######################################################################
    # End backwards compatibility
    ######################################################################
