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
from .layout import PackLogic

NOT_PROVIDED = object()

PACK = "pack"


@dataclass(kw_only=True, repr=False)
class Pack(PackLogic):
    _doc_link = "[style properties](/reference/style/pack)"

    display: str = validated_property(PACK, NONE, initial=PACK)
    """Defines how to display the widget.

    **Allowed values:** `"pack"` or `"none"`

    **Default value:** `"pack"`

    A value of `"pack"` will apply the pack layout algorithm to this node and its
    descendants. A value of `"none"` removes the widget from the layout entirely. Space
    will be allocated for the widget as if it were there, but the widget itself will
    not be visible.
    """
    visibility: str = validated_property(VISIBLE, HIDDEN, initial=VISIBLE)
    """Defines whether the widget should be drawn.

    **Allowed values:** `"hidden"` or `"visible"`

    **Default value:** `"visible"`

    A value of `"visible"` means the widget will be displayed. A value of `"hidden"`
    removes the widget from view, but allocates space for the widget as if it were
    still in the layout.

    Any children of a hidden widget are implicitly removed from view.

    If a previously hidden widget is made visible, any children of the widget with a
    visibility of `"hidden"` will remain hidden. Any descendants of the hidden child
    will also remain hidden, regardless of their visibility.
    """
    direction: str = validated_property(ROW, COLUMN, initial=ROW)
    """The packing direction for children of the box.

    **Allowed values:** `"row"` or `"column"`

    **Default value:** `"row"`

    A value of `"column"` indicates children will be stacked vertically, from top to
    bottom. A value of `"row"` indicates children will be packed horizontally;
    left-to-right if `text_direction` is `"ltr"`, or right-to-left if `text_direction`
    is `"rtl"`.
    """
    align_items: str | None = validated_property(START, CENTER, END)
    """The alignment of this box's children along the cross axis.

    **Allowed values:** `"start"`, `"center"`, or `"end"`

    **Default value:** `"start"`

    **Aliases:** `vertical_align_items` in a row, `horizontal_align_items` in a column

    A row's cross axis is vertical, so `"start"` aligns children to the top, while
    `"end"` aligns them to the bottom. For columns, `"start"` is on the left if
    `text_direction` is `"ltr"`, and the right if `rtl`.
    """
    justify_content: str | None = validated_property(START, CENTER, END, initial=START)
    """The alignment of this box's children along the main axis.

    **Allowed values:** `"start"`, `"center"`, or `"end"`

    **Default value:** `"start"`

    **Aliases:** `horizontal_align_content` in a row, `vertical_align_content` in a
    column

    A column's main axis is vertical, so `"start"` aligns children to the top, while
    `"end"` aligns them to the bottom. For rows, `"start"` is on the left if
    `text_direction` is `"ltr"`, and the right if `"rtl"`.

    This property only has an effect if there is some free space in the main axis. For
    example, if any children have a non-zero `flex` value, then they will consume all
    the available space, and `justify_content` will make no difference to the layout.
    """
    gap: int = validated_property(integer=True, initial=0)
    """The amount of space to allocate between adjacent children, in
    [CSS pixels][css-units].

    **Allowed values:** an integer

    **Default value:** `0`
    """
    width: str | int = validated_property(NONE, integer=True, initial=NONE)
    """A specified fixed width for the box, in [CSS pixels][css-units].

    **Allowed values:** an integer or `"none"`

    **Default value:** `"none"`

    The final width for the box may be larger, if the children of the box cannot fit
    inside the specified space.
    """
    height: str | int = validated_property(NONE, integer=True, initial=NONE)
    """A specified fixed height for the box, in [CSS pixels][css-units].

    **Allowed values:** an integer or `"none"`

    **Default value:** `"none"`

    The final height for the box may be larger, if the children of the box cannot fit
    inside the specified space.
    """
    flex: float = validated_property(number=True, initial=0)
    """A weighting that is used to compare this box with its siblings when allocating
    remaining space in a box.

    **Allowed values:** a floating-point number

    **Default value:** `0.0`

    Once fixed space allocations have been performed, this box will assume `flex /
    (sum of all flex for all siblings)` of all remaining available space in the
    direction of the parent's layout.
    """
    margin_top: int = validated_property(integer=True, initial=0)
    """"""
    margin_right: int = validated_property(integer=True, initial=0)
    """"""
    margin_bottom: int = validated_property(integer=True, initial=0)
    """"""
    margin_left: int = validated_property(integer=True, initial=0)
    """The amount of space to allocate outside the edge of the box, in
    [CSS pixels][css-units].

    **Allowed values:** an integer

    **Default value:** `0`

    """
    margin: (
        int
        | tuple[int]
        | tuple[int, int]
        | tuple[int, int, int]
        | tuple[int, int, int, int]
    ) = directional_property("margin{}")
    """A shorthand for setting the top, right, bottom and left margin with a single
    declaration.

    **Allowed values:** a tuple consisting of `(margin_top, margin_right, margin_bottom,
    margin_left)`

    **Default value:** `(0, 0, 0, 0)`

    **Accepts:** an integer or a sequence of 1–4 integers

    If 1 integer is provided, that value will be used as the margin for all sides.

    If 2 integers are provided, the first value will be used as the margin for the top
    and bottom; the second will be used as the value for the left and right.

    If 3 integers are provided, the first value will be used as the top margin, the
    second for the left and right margin, and the third for the bottom margin.

    If 4 integers are provided, they will be used as the top, right, bottom and left
    margin, respectively.
    """
    color: ColorT | str | None = validated_property(color=True)
    """The foreground color for the object being rendered.

    **Allowed values:** a [color][toga.colors.ColorT] or `None`

    **Default value:** `None`; will use the system default

    Some objects may not use the value.
    """
    background_color: ColorT | str | None = validated_property(TRANSPARENT, color=True)
    """The background color for the object being rendered.

    **Allowed values:** a [color][toga.colors.ColorT], `"transparent"`, or `None`

    **Default value:** `None`; will use the system default

    Some objects may not use the value.
    """
    text_align: str | None = validated_property(LEFT, RIGHT, CENTER, JUSTIFY)
    """The alignment of text in the object being rendered.

    **Allowed values:** `"left"`, `"right"`, `"center"`, or `"justify"`

    **Default value:** `"left"` if `text_direction` is `"ltr"`; `"right"` if
    `text_direction` is `"rtl"`

    """
    text_direction: str | None = validated_property(RTL, LTR, initial=LTR)
    """The natural direction of horizontal content.

    **Allowed values:** `"rtl"` or `"ltr"`

    **Default value:** `"rtl"`
    """
    font_family: str | list[str] = list_property(
        *SYSTEM_DEFAULT_FONTS, string=True, initial=[SYSTEM]
    )
    """A list defining possible font families, in order of preference.

    **Value**: a list of strings

    **Default value:** `["system"]`

    **Accepts:** a string or a sequence of strings

    The first item that maps to a valid font will be used. If none can be resolved, the
    system font will be used. Setting to a single string value is the same as setting
    to a list containing that string as the only item.

    A value of `"system"` indicates that whatever is a system-appropriate font should be
    used.

    A value of `"serif"`, `"sans-serif"`, `"cursive"`, `"fantasy"`, or `"monospace"`
    will use a system-defined font that matches the description (e.g. Times New Roman
    for `"serif"`, Courier New for `"monospace"`).

    Any other value will be checked against the family names previously registered with
    [`Font.register`][toga.Font.register].

    On supported platforms (currently Windows and Linux), if Toga doesn't recognize the
    family as one of its predefined builtins or as a font you've registered, it will
    attempt to load the requested font from your system before falling back to the
    default system font.
    """
    font_style: str = validated_property(*FONT_STYLES, initial=NORMAL)
    """The style of the font to be used.

    **Allowed values:** `"normal"`, `"italic"`, or `"oblique"`

    **Default value:** `"normal"`

    **Note:** Windows and Android do not support the oblique font style. A request for
    an `"oblique"` font will be interpreted as `"italic"`.
    """
    font_variant: str = validated_property(*FONT_VARIANTS, initial=NORMAL)
    """The variant of the font to be used.

    **Allowed values:** `"normal"` or `"small_caps"`

    **Default value:** `"normal"`

    **Note:** Windows and Android do not support the small caps variant. A request for a
    `"small_caps"` font will be interpreted as `"normal"`.
    """
    font_weight: str = validated_property(*FONT_WEIGHTS, initial=NORMAL)
    """The weight of the font to be used.

    **Allowed values:** `"normal"` or `"bold"`

    **Default value:** `"normal"`
    """
    font_size: int = validated_property(integer=True, initial=SYSTEM_DEFAULT_FONT_SIZE)
    """The size of the font to be used, in [CSS points][css-units].

    **Allowed values:** an integer

    **Default value:** `-1`; will use the system default size. This is also stored as a
    constant named `SYSTEM_DEFAULT_FONT_SIZE`.
    """
    font: (
        tuple[int, list[str] | str]
        | tuple[str, int, list[str] | str]
        | tuple[str, str, int, list[str] | str]
        | tuple[str, str, str, int, list[str] | str]
    ) = composite_property(
        optional=("font_style", "font_variant", "font_weight"),
        required=("font_size", "font_family"),
    )
    """A shorthand for simultaneously setting multiple properties of a font.

    **Allowed values:** a tuple consisting of `(font_style, font_variant, font_weight,
    font_size, font_family)`

    **Default value:** `("normal", "normal", "normal", -1, ["system"])`

    **Accepts:** any valid values (in order) for `font_size` and `font_family`, preceded
    by any combination and order of valid values for `font_style`, `font_variant`, and
    `font_weight`.

    Any of the three optional values (style, variant, and weight) not
    specified will be reset to `"normal"`.
    """

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
