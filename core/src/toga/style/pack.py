from __future__ import annotations

import warnings
from typing import Any

from travertino.constants import (  # noqa: F401
    BOLD,
    BOTTOM,
    CENTER,
    COLUMN,
    CURSIVE,
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
    SYSTEM,
    TOP,
    TRANSPARENT,
    VISIBLE,
)
from travertino.declaration import BaseStyle, Choices
from travertino.layout import BaseBox
from travertino.size import BaseIntrinsicSize

from toga.fonts import (
    FONT_STYLES,
    FONT_VARIANTS,
    FONT_WEIGHTS,
    SYSTEM_DEFAULT_FONT_SIZE,
    SYSTEM_DEFAULT_FONTS,
    Font,
)

# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)

######################################################################
# Display
######################################################################

PACK = "pack"

######################################################################
# Declaration choices
######################################################################

# Define here, since they're not available in Travertino 0.3.0
START = "start"
END = "end"

# Used in backwards compatibility section below
ALIGNMENT = "alignment"
ALIGN_ITEMS = "align_items"

DISPLAY_CHOICES = Choices(PACK, NONE)
VISIBILITY_CHOICES = Choices(VISIBLE, HIDDEN)
DIRECTION_CHOICES = Choices(ROW, COLUMN)
ALIGN_ITEMS_CHOICES = Choices(START, CENTER, END)
ALIGNMENT_CHOICES = Choices(LEFT, RIGHT, TOP, BOTTOM, CENTER)  # Deprecated
JUSTIFY_CONTENT_CHOICES = Choices(START, CENTER, END)
GAP_CHOICES = Choices(integer=True)

SIZE_CHOICES = Choices(NONE, integer=True)
FLEX_CHOICES = Choices(number=True)

MARGIN_CHOICES = Choices(integer=True)

TEXT_ALIGN_CHOICES = Choices(LEFT, RIGHT, CENTER, JUSTIFY)
TEXT_DIRECTION_CHOICES = Choices(RTL, LTR)

COLOR_CHOICES = Choices(color=True)
BACKGROUND_COLOR_CHOICES = Choices(TRANSPARENT, color=True)

FONT_FAMILY_CHOICES = Choices(*SYSTEM_DEFAULT_FONTS, string=True)
FONT_STYLE_CHOICES = Choices(*FONT_STYLES)
FONT_VARIANT_CHOICES = Choices(*FONT_VARIANTS)
FONT_WEIGHT_CHOICES = Choices(*FONT_WEIGHTS)
FONT_SIZE_CHOICES = Choices(integer=True)


class Pack(BaseStyle):
    class Box(BaseBox):
        pass

    class IntrinsicSize(BaseIntrinsicSize):
        pass

    _depth = -1

    @classmethod
    def _debug(cls, *args: str) -> None:  # pragma: no cover
        print("    " * cls._depth, *args)

    @property
    def _hidden(self) -> bool:
        """Does this style declaration define an object that should be hidden."""
        return self.visibility == HIDDEN

    ######################################################################
    # 2024-12: Backwards compatibility for Toga <= 0.4.8
    ######################################################################

    def update(self, **properties):
        properties = {
            self._update_property_name(name.replace("-", "_")): value
            for name, value in properties.items()
        }
        super().update(**properties)

    # Pack.alignment is still an actual property, despite being deprecated, so we need
    # to suppress deprecation warnings when reapply is called.
    def reapply(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            super().reapply(*args, **kwargs)

    DEPRECATED_PROPERTIES = {
        # Map each deprecated property name to its replacement.
        # alignment / align_items is handled separately.
        "padding": "margin",
        "padding_top": "margin_top",
        "padding_right": "margin_right",
        "padding_bottom": "margin_bottom",
        "padding_left": "margin_left",
    }

    @classmethod
    def _update_property_name(cls, name):
        if new_name := cls.DEPRECATED_PROPERTIES.get(name):
            cls._warn_deprecated(name, new_name, stacklevel=4)
            name = new_name

        return name

    @staticmethod
    def _warn_deprecated(old_name, new_name, stacklevel=3):
        msg = f"Pack.{old_name} is deprecated; use {new_name} instead"
        warnings.warn(msg, DeprecationWarning, stacklevel=stacklevel)

    # Dot lookup

    def __getattribute__(self, name):
        # Align_items and alignment are paired. Both can never be set at the same time;
        # if one is requested, and the other one is set, compute the requested value
        # from the one that is set.
        if name == ALIGN_ITEMS and (alignment := super().__getattribute__(ALIGNMENT)):
            if alignment == CENTER:
                return CENTER

            if self.direction == ROW:
                if alignment == TOP:
                    return START
                if alignment == BOTTOM:
                    return END

                # No remaining valid combinations
                return None

            # direction must be COLUMN
            if alignment == LEFT:
                return START if self.text_direction == LTR else END
            if alignment == RIGHT:
                return START if self.text_direction == RTL else END

            # No remaining valid combinations
            return None

        if name == ALIGNMENT:
            # Warn, whether it's set or not.
            self._warn_deprecated(ALIGNMENT, ALIGN_ITEMS)

            if align_items := super().__getattribute__(ALIGN_ITEMS):
                if align_items == START:
                    if self.direction == COLUMN:
                        return LEFT if self.text_direction == LTR else RIGHT
                    return TOP  # for ROW

                if align_items == END:
                    if self.direction == COLUMN:
                        return RIGHT if self.text_direction == LTR else LEFT
                    return BOTTOM  # for ROW

                # Only CENTER remains
                return CENTER

        return super().__getattribute__(type(self)._update_property_name(name))

    def __setattr__(self, name, value):
        # Only one of these can be set at a time.
        if name == ALIGN_ITEMS:
            super().__delattr__(ALIGNMENT)
        elif name == ALIGNMENT:
            self._warn_deprecated(ALIGNMENT, ALIGN_ITEMS)
            super().__delattr__(ALIGN_ITEMS)

        super().__setattr__(self._update_property_name(name), value)

    def __delattr__(self, name):
        # If one of the two is being deleted, delete the other also.
        if name == ALIGN_ITEMS:
            super().__delattr__(ALIGNMENT)
        elif name == ALIGNMENT:
            self._warn_deprecated(ALIGNMENT, ALIGN_ITEMS)
            super().__delattr__(ALIGN_ITEMS)

        super().__delattr__(self._update_property_name(name))

    # Index notation

    def __getitem__(self, name):
        # As long as we're mucking about with backwards compatibility: Travertino 0.3.0
        # doesn't support accessing directional properties via bracket notation, so
        # special-case it here to gain access to the FUTURE.
        if name in {"padding", "margin"}:
            return getattr(self, name)

        return super().__getitem__(self._update_property_name(name.replace("-", "_")))

    def __setitem__(self, name, value):
        if name in {"padding", "margin"}:
            setattr(self, name, value)
            return

        super().__setitem__(self._update_property_name(name.replace("-", "_")), value)

    def __delitem__(self, name):
        if name in {"padding", "margin"}:
            delattr(self, name)
            return

        super().__delitem__(self._update_property_name(name.replace("-", "_")))

    ######################################################################
    # End backwards compatibility
    ######################################################################

    def apply(self, prop: str, value: object) -> None:
        if self._applicator:
            if prop == "text_align":
                if value is None:
                    if self.text_direction == RTL:
                        value = RIGHT
                    else:
                        value = LEFT
                self._applicator.set_text_align(value)
            elif prop == "text_direction":
                if self.text_align is None:
                    self._applicator.set_text_align(RIGHT if value == RTL else LEFT)
            elif prop == "color":
                self._applicator.set_color(value)
            elif prop == "background_color":
                self._applicator.set_background_color(value)
            elif prop == "visibility":
                if value == VISIBLE:
                    # If visibility is being set to VISIBLE, look up the chain to see if
                    # an ancestor is hidden.
                    widget = self._applicator.widget
                    while widget := widget.parent:
                        if widget.style._hidden:
                            value = HIDDEN
                            break

                self._applicator.set_hidden(value == HIDDEN)
            elif prop in (
                "font_family",
                "font_size",
                "font_style",
                "font_variant",
                "font_weight",
            ):
                self._applicator.set_font(
                    Font(
                        self.font_family,
                        self.font_size,
                        style=self.font_style,
                        variant=self.font_variant,
                        weight=self.font_weight,
                    )
                )
            else:
                # Any other style change will cause a change in layout geometry,
                # so perform a refresh.
                self._applicator.refresh()

    def layout(self, viewport: Any, _deprecated_usage=None) -> None:
        ######################################################################
        # 2024-12: Backwards compatibility for Travertino 0.3.0
        ######################################################################

        if _deprecated_usage is not None:
            # Was called with (self, viewport)
            viewport = _deprecated_usage

        ######################################################################
        # End backwards compatibility
        ######################################################################

        # self._debug("=" * 80)
        # self._debug(
        #     f"Layout root {node}, available {viewport.width}x{viewport.height}"
        # )
        self.__class__._depth = -1

        self._layout_node(
            alloc_width=viewport.width,
            alloc_height=viewport.height,
            use_all_height=True,  # root node uses all height
            use_all_width=True,  # root node uses all width
        )

        node = self._applicator.node

        node.layout.content_top = self.margin_top
        node.layout.content_bottom = self.margin_bottom

        node.layout.content_left = self.margin_left
        node.layout.content_right = self.margin_right

    def _layout_node(
        self,
        alloc_width: int,
        alloc_height: int,
        use_all_width: bool,
        use_all_height: bool,
    ) -> None:
        self.__class__._depth += 1
        # self._debug(
        #     f"COMPUTE LAYOUT for {node} available "
        #     f"{alloc_width}{'+' if use_all_width else ''}"
        #     " x "
        #     f"{alloc_height}{'+' if use_all_height else ''}"
        # )

        node = self._applicator.node

        # Establish available width
        if self.width != NONE:
            # If width is specified, use it
            available_width = self.width
            min_width = self.width
            # self._debug(f"SPECIFIED WIDTH {self.width}")
        else:
            # If no width is specified, assume we're going to use all
            # the available width. If there is an intrinsic width,
            # use it to make sure the width is at least the amount specified.
            available_width = max(
                0, (alloc_width - self.margin_left - self.margin_right)
            )
            # self._debug(f"INITIAL {available_width=}")
            if node.intrinsic.width is not None:
                # self._debug(f"INTRINSIC WIDTH {node.intrinsic.width}")
                try:
                    min_width = node.intrinsic.width.value
                    available_width = max(available_width, min_width)
                except AttributeError:
                    available_width = node.intrinsic.width
                    min_width = node.intrinsic.width

                # self._debug(f"ADJUSTED {available_width=}")
            else:
                # self._debug(f"AUTO {available_width=}")
                min_width = 0

        # Establish available height
        if self.height != NONE:
            # If height is specified, use it.
            available_height = self.height
            min_height = self.height
            # self._debug(f"SPECIFIED HEIGHT {self.height}")
        else:
            available_height = max(
                0,
                alloc_height - self.margin_top - self.margin_bottom,
            )
            # self._debug(f"INITIAL {available_height=}")
            if node.intrinsic.height is not None:
                # self._debug(f"INTRINSIC HEIGHT {node.intrinsic.height}")
                try:
                    min_height = node.intrinsic.height.value
                    available_height = max(available_height, min_height)
                except AttributeError:
                    available_height = node.intrinsic.height
                    min_height = node.intrinsic.height

                # self._debug(f"ADJUSTED {available_height=}")
            else:
                # self._debug(f"AUTO {available_height=}")
                min_height = 0

        if node.children:
            min_width, width, min_height, height = self._layout_children(
                available_width=available_width,
                available_height=available_height,
                use_all_width=use_all_width,
                use_all_height=use_all_height,
            )
            # self._debug(f"HAS CHILDREN {min_width=} {width=} {min_height=} {height=}")
        else:
            width = available_width
            height = available_height
            # self._debug(f"NO CHILDREN {min_width=} {width=} {min_height=} {height=}")

        # If an explicit width/height was given, that specification
        # overrides the width/height evaluated by the layout of children
        if self.width != NONE:
            width = self.width
            min_width = width
        if self.height != NONE:
            height = self.height
            min_height = height

        # self._debug(f"FINAL SIZE {min_width}x{min_height} {width}x{height}")
        node.layout.content_width = int(width)
        node.layout.content_height = int(height)

        node.layout.min_content_width = int(min_width)
        node.layout.min_content_height = int(min_height)

        # self._debug("END LAYOUT", node, node.layout)
        self.__class__._depth -= 1

    def _layout_node_in_direction(
        self,
        direction: str,  # ROW | COLUMN
        alloc_main: int,
        alloc_cross: int,
        use_all_main: bool,
        use_all_cross: bool,
    ) -> None:
        if direction == COLUMN:
            self._layout_node(
                alloc_height=alloc_main,
                alloc_width=alloc_cross,
                use_all_height=use_all_main,
                use_all_width=use_all_cross,
            )
        else:
            self._layout_node(
                alloc_width=alloc_main,
                alloc_height=alloc_cross,
                use_all_width=use_all_main,
                use_all_height=use_all_cross,
            )

    def _layout_children(
        self,
        available_width: int,
        available_height: int,
        use_all_width: bool,
        use_all_height: bool,
    ) -> tuple[int, int, int, int]:  # min_width, width, min_height, height
        # Assign the appropriate dimensions to main and cross axes, depending on row /
        # column direction.
        horizontal = (LEFT, RIGHT) if self.text_direction == LTR else (RIGHT, LEFT)
        if self.direction == COLUMN:
            available_main, available_cross = available_height, available_width
            use_all_main, use_all_cross = use_all_height, use_all_width
            main_name, cross_name = "height", "width"
            main_start, main_end = TOP, BOTTOM
            cross_start, cross_end = horizontal
        else:
            available_main, available_cross = available_width, available_height
            use_all_main, use_all_cross = use_all_width, use_all_height
            main_name, cross_name = "width", "height"
            main_start, main_end = horizontal
            cross_start, cross_end = TOP, BOTTOM

        node = self._applicator.node
        flex_total = 0
        min_flex = 0
        main = 0
        min_main = 0
        remaining_main = available_main

        # self._debug(
        #     f"LAYOUT {self.direction.upper()} CHILDREN "
        #     f"{main_name=} {available_main=} {available_cross=}"
        # )

        # Pass 1: Lay out all children with a hard-specified main-axis dimension, or an
        # intrinsic non-flexible dimension. While iterating, collect the flex
        # total of remaining elements.

        for i, child in enumerate(node.children):
            # self._debug(f"PASS 1 {child}")
            if child.style[main_name] != NONE:
                # self._debug(f"- fixed {main_name} {child.style[main_name]}")
                child.style._layout_node_in_direction(
                    direction=self.direction,
                    alloc_main=remaining_main,
                    alloc_cross=available_cross,
                    use_all_main=False,
                    use_all_cross=child.style.direction == self.direction,
                )
                child_content_main = getattr(child.layout, f"content_{main_name}")

                # It doesn't matter how small the children can be laid out; we have an
                # intrinsic size; so don't use min_content.(main_name)
                min_child_content_main = getattr(child.layout, f"content_{main_name}")

            elif getattr(child.intrinsic, main_name) is not None:
                if hasattr(getattr(child.intrinsic, main_name), "value"):
                    if child.style.flex:
                        # self._debug(
                        #     f"- intrinsic flex {main_name} "
                        #     f"{getattr(child.intrinsic, main_name)=}"
                        # )
                        flex_total += child.style.flex
                        # Final child content size will be computed in pass 2, after the
                        # amount of flexible space is known. For now, set an initial
                        # content main-axis size based on the intrinsic size, which
                        # will be the minimum possible allocation.
                        child_content_main = getattr(child.intrinsic, main_name).value
                        min_child_content_main = child_content_main

                        min_flex += (
                            child.style[f"margin_{main_start}"]
                            + child_content_main
                            + child.style[f"margin_{main_end}"]
                        )
                    else:
                        # self._debug(
                        #     f"- intrinsic non-flex {main_name} "
                        #     f"{getattr(child.intrinsic, main_name)=}"
                        # )
                        child.style._layout_node_in_direction(
                            direction=self.direction,
                            alloc_main=0,
                            alloc_cross=available_cross,
                            use_all_main=False,
                            use_all_cross=child.style.direction == self.direction,
                        )

                        child_content_main = getattr(
                            child.layout, f"content_{main_name}"
                        )

                        # It doesn't matter how small the children can be laid out; we
                        # have an intrinsic size; so don't use
                        # layout._min_content(main_name)
                        min_child_content_main = child_content_main
                else:
                    # self._debug(
                    #     f"- intrinsic {main_name} "
                    #     f"{getattr(child.intrinsic, main_name)=}"
                    # )
                    child.style._layout_node_in_direction(
                        direction=self.direction,
                        alloc_main=remaining_main,
                        alloc_cross=available_cross,
                        use_all_main=False,
                        use_all_cross=child.style.direction == self.direction,
                    )

                    child_content_main = getattr(child.layout, f"content_{main_name}")

                    # It doesn't matter how small the children can be laid out; we have
                    # an intrinsic size; so don't use layout._min_content(main_name)
                    min_child_content_main = child_content_main
            else:
                if child.style.flex:
                    # self._debug(f"- unspecified flex {main_name}")
                    flex_total += child.style.flex
                    # Final child content size will be computed in pass 2, after the
                    # amount of flexible space is known. For now, use 0 as the minimum,
                    # as that's the best hint the widget style can give.
                    child_content_main = 0
                    min_child_content_main = 0
                else:
                    # self._debug(f"- unspecified non-flex {main_name}")
                    child.style._layout_node_in_direction(
                        direction=self.direction,
                        alloc_main=remaining_main,
                        alloc_cross=available_cross,
                        use_all_main=False,
                        use_all_cross=child.style.direction == self.direction,
                    )
                    child_content_main = getattr(child.layout, f"content_{main_name}")
                    min_child_content_main = getattr(
                        child.layout, f"min_content_{main_name}"
                    )

            gap = 0 if i == 0 else self.gap
            child_main = (
                child.style[f"margin_{main_start}"]
                + child_content_main
                + child.style[f"margin_{main_end}"]
            )
            main += gap + child_main
            remaining_main -= gap + child_main

            min_child_main = (
                child.style[f"margin_{main_start}"]
                + min_child_content_main
                + child.style[f"margin_{main_end}"]
            )
            min_main += gap + min_child_main

            # self._debug(f"  {min_child_main=} {min_main=} {min_flex=}")
            # self._debug(f"  {child_main=} {main=} {remaining_main=}")

        if flex_total > 0:
            quantum = (remaining_main + min_flex) / flex_total
            # In an ideal flex layout, all flex children will have a main-axis size
            # proportional to their flex value. However, if a flex child has a flexible
            # minimum main-axis size constraint that is greater than the ideal
            # main-axis size for a balanced flex layout, they need to be removed from
            # the flex calculation.

            # self._debug(f"PASS 1a; {quantum=}")
            for child in node.children:
                child_intrinsic_main = getattr(child.intrinsic, main_name)
                if child.style.flex and child_intrinsic_main is not None:
                    try:
                        ideal_main = quantum * child.style.flex
                        if child_intrinsic_main.value > ideal_main:
                            # self._debug(f"- {child} overflows ideal main dimension")
                            flex_total -= child.style.flex
                            min_flex -= (
                                child.style[f"margin_{main_start}"]
                                + child_intrinsic_main.value
                                + child.style[f"margin_{main_end}"]
                            )
                    except AttributeError:
                        # Intrinsic main-axis size isn't flexible
                        pass

            if flex_total > 0:
                quantum = (min_flex + remaining_main) / flex_total
            else:
                quantum = 0
        else:
            quantum = 0

        # self._debug(f"END PASS 1; {min_main=} {main=} {min_flex=} {quantum=}")

        # Pass 2: Lay out children with an intrinsic flexible main-axis size, or no
        # main-axis size specification at all.
        for child in node.children:
            # self._debug(f"PASS 2 {child}")
            if child.style[main_name] != NONE:
                # self._debug(f"- already laid out (explicit {main_name})")
                pass
            elif child.style.flex:
                if getattr(child.intrinsic, main_name) is not None:
                    try:
                        child_alloc_main = (
                            child.style[f"margin_{main_start}"]
                            + getattr(child.intrinsic, main_name).value
                            + child.style[f"margin_{main_end}"]
                        )
                        ideal_main = quantum * child.style.flex
                        # self._debug(
                        #     f"- flexible intrinsic {main_name} {child_alloc_main=}"
                        # )
                        if ideal_main > child_alloc_main:
                            # self._debug(f"  {ideal_main=}")
                            child_alloc_main = ideal_main

                        child.style._layout_node_in_direction(
                            direction=self.direction,
                            alloc_main=child_alloc_main,
                            alloc_cross=available_cross,
                            use_all_main=True,
                            use_all_cross=child.style.direction == self.direction,
                        )
                        # Our main-axis dimension calculation already takes into account
                        # the intrinsic size; that has now expanded as a result of
                        # layout, so adjust to use the new layout size. Min size may
                        # also change, by the same scheme, because the flex child can
                        # itself have children, and those grandchildren have now been
                        # laid out.

                        # self._debug(
                        #     f"  sub {getattr(child.intrinsic, main_name).value=}"
                        # )
                        # self._debug(
                        #     f"  add {getattr(child.layout, f'content_{main_name}')=}"
                        # )
                        # self._debug(
                        #     f"  add min "
                        #     f"{getattr(child.layout, f'min_content_{main_name}')=}"
                        # )
                        main = (
                            main
                            - getattr(child.intrinsic, main_name).value
                            + getattr(child.layout, f"content_{main_name}")
                        )
                        min_main = (
                            min_main
                            - getattr(child.intrinsic, main_name).value
                            + getattr(child.layout, f"min_content_{main_name}")
                        )
                    except AttributeError:
                        # self._debug(
                        #     "- already laid out (fixed intrinsic main-axis dimension)"
                        # )
                        pass
                else:
                    if quantum:
                        # self._debug(
                        #     f"- unspecified flex {main_name} with {quantum=}"
                        # )
                        child_alloc_main = quantum * child.style.flex
                    else:
                        # self._debug(f"- unspecified flex {main_name}")
                        child_alloc_main = (
                            child.style[f"margin_{main_start}"]
                            + child.style[f"margin_{main_end}"]
                        )

                    child.style._layout_node_in_direction(
                        direction=self.direction,
                        alloc_main=child_alloc_main,
                        alloc_cross=available_cross,
                        use_all_main=True,
                        use_all_cross=child.style.direction == self.direction,
                    )
                    # We now know the final min_main/main that accounts for flexible
                    # sizing; add that to the overall.

                    # self._debug(
                    #     f"  add {getattr(child.layout, f'min_content_{main_name}')=}"
                    # )
                    # self._debug(
                    #     f"  add {getattr(child.layout, f'content_{main_name}')=}"
                    # )
                    main += getattr(child.layout, f"content_{main_name}")
                    min_main += getattr(child.layout, f"min_content_{main_name}")

            else:
                # self._debug(f"- already laid out (intrinsic non-flex {main_name})")
                pass

            # self._debug(f"{main_name} {min_main=} {main=}")

        # self._debug(f"PASS 2 COMPLETE; USED {main=} {main_name}")
        if use_all_main or self[main_name] != NONE:
            extra = max(0, available_main - main)
            main += extra
        else:
            extra = 0
        # self._debug(f"COMPUTED {main_name} {min_main=} {main=}")

        # Pass 3: Set the main-axis position of each element, and establish box's
        # cross-axis dimension
        if self.justify_content == END:
            offset = extra
        elif self.justify_content == CENTER:
            offset = extra / 2
        else:  # START
            offset = 0

        cross = 0
        min_cross = 0

        for child in node.children:
            # self._debug(f"PASS 3: {child} AT MAIN-AXIS OFFSET {offset}")
            if main_start == RIGHT:
                # Needs special casing, since it's still ultimately content_left that
                # needs to be set.
                offset += child.layout.content_width + child.style.margin_right
                child.layout.content_left = main - offset
                offset += child.style.margin_left
            else:
                offset += child.style[f"margin_{main_start}"]
                setattr(child.layout, f"content_{main_start}", offset)
                offset += getattr(child.layout, f"content_{main_name}")
                offset += child.style[f"margin_{main_end}"]

            offset += self.gap

            child_cross = (
                getattr(child.layout, f"content_{cross_name}")
                + child.style[f"margin_{cross_start}"]
                + child.style[f"margin_{cross_end}"]
            )
            cross = max(cross, child_cross)

            min_child_cross = (
                child.style[f"margin_{cross_start}"]
                + getattr(child.layout, f"min_content_{cross_name}")
                + child.style[f"margin_{cross_end}"]
            )
            min_cross = max(min_cross, min_child_cross)

        # self._debug(f"{self.direction.upper()} {min_cross=} {cross=}")
        if use_all_cross:
            cross = max(cross, available_cross)
        # self._debug(f"FINAL {self.direction.upper()} {min_cross=} {cross=}")

        # Pass 4: Set cross-axis position of each child.

        # The "effective" start, end, and align-items values are normally their "real"
        # values. However, if the cross-axis is horizontal and text-direction RTL,
        # they're flipped. This is necessary because final positioning is always set
        # using a top-left origin, even if the "real" start is on the right.
        effective_align_items = self.align_items

        if cross_start == RIGHT:
            effective_cross_start = LEFT
            effective_cross_end = RIGHT

            if self.align_items == START:
                effective_align_items = END
            elif self.align_items == END:
                effective_align_items = START

        else:
            effective_cross_start = cross_start
            effective_cross_end = cross_end

        for child in node.children:
            # self._debug(f"PASS 4: {child}")
            extra = cross - (
                getattr(child.layout, f"content_{cross_name}")
                + child.style[f"margin_{effective_cross_start}"]
                + child.style[f"margin_{effective_cross_end}"]
            )
            # self._debug(f"-  {self.direction} extra {cross_name} {extra}")

            if effective_align_items == END:
                cross_start_value = extra + child.style[f"margin_{cross_start}"]
                # self._debug(f"  align {child} to {cross_end}")

            elif effective_align_items == CENTER:
                cross_start_value = (
                    int(extra / 2) + child.style[f"margin_{cross_start}"]
                )
                # self._debug(f"  align {child} to center")

            else:
                cross_start_value = child.style[f"margin_{cross_start}"]
                # self._debug(f"  align {child} to {cross_start} ")

            setattr(child.layout, f"content_{effective_cross_start}", cross_start_value)
            # self._debug(f"  {getattr(child.layout, f'content_{cross_start}')=}")

        if self.direction == COLUMN:
            return min_cross, cross, min_main, main
        else:
            return min_main, main, min_cross, cross

    def __css__(self) -> str:
        css = []
        # display
        if self.display == NONE:
            css.append("display: none;")
        else:
            # if self.display != NONE, it must be pack; it will inherit
            # the pack definition from the Toga stylesheet.
            pass

        # visibility
        if self.visibility != VISIBLE:
            css.append(f"visibility: {self.visibility};")

        # direction
        css.append(f"flex-direction: {self.direction.lower()};")
        # flex
        if (self.width == NONE and self.direction == ROW) or (
            self.height == NONE and self.direction == COLUMN
        ):
            css.append(f"flex: {self.flex} 0 auto;")

        # width/flex
        if self.width != NONE:
            css.append(f"width: {self.width}px;")

        # height/flex
        if self.height != NONE:
            css.append(f"height: {self.height}px;")

        # align_items
        if self.align_items:
            css.append(f"align-items: {self.align_items};")

        # justify_content
        if self.justify_content != START:
            css.append(f"justify-content: {self.justify_content};")

        # gap
        if self.gap:
            css.append(f"gap: {self.gap}px;")

        # margin_*
        if self.margin_top:
            css.append(f"margin-top: {self.margin_top}px;")
        if self.margin_bottom:
            css.append(f"margin-bottom: {self.margin_bottom}px;")
        if self.margin_left:
            css.append(f"margin-left: {self.margin_left}px;")
        if self.margin_right:
            css.append(f"margin-right: {self.margin_right}px;")

        # color
        if self.color:
            css.append(f"color: {self.color};")

        # background_color
        if self.background_color:
            css.append(f"background-color: {self.background_color};")

        # text_align
        if self.text_align:
            css.append(f"text-align: {self.text_align};")

        # text_direction
        if self.text_direction != LTR:
            css.append(f"text-direction: {self.text_direction};")

        # font-*
        if self.font_family != SYSTEM:
            if " " in self.font_family:
                css.append(f'font-family: "{self.font_family}";')
            else:
                css.append(f"font-family: {self.font_family};")
        if self.font_size != SYSTEM_DEFAULT_FONT_SIZE:
            css.append(f"font-size: {self.font_size}pt;")
        if self.font_weight != NORMAL:
            css.append(f"font-weight: {self.font_weight};")
        if self.font_style != NORMAL:
            css.append(f"font-style: {self.font_style};")
        if self.font_variant != NORMAL:
            css.append(f"font-variant: {self.font_variant};")

        return " ".join(css)


Pack.validated_property("display", choices=DISPLAY_CHOICES, initial=PACK)
Pack.validated_property("visibility", choices=VISIBILITY_CHOICES, initial=VISIBLE)
Pack.validated_property("direction", choices=DIRECTION_CHOICES, initial=ROW)
Pack.validated_property("align_items", choices=ALIGN_ITEMS_CHOICES)
Pack.validated_property("alignment", choices=ALIGNMENT_CHOICES)  # Deprecated
Pack.validated_property(
    "justify_content", choices=JUSTIFY_CONTENT_CHOICES, initial=START
)
Pack.validated_property("gap", choices=GAP_CHOICES, initial=0)

Pack.validated_property("width", choices=SIZE_CHOICES, initial=NONE)
Pack.validated_property("height", choices=SIZE_CHOICES, initial=NONE)
Pack.validated_property("flex", choices=FLEX_CHOICES, initial=0)

Pack.validated_property("margin_top", choices=MARGIN_CHOICES, initial=0)
Pack.validated_property("margin_right", choices=MARGIN_CHOICES, initial=0)
Pack.validated_property("margin_bottom", choices=MARGIN_CHOICES, initial=0)
Pack.validated_property("margin_left", choices=MARGIN_CHOICES, initial=0)
Pack.directional_property("margin%s")

Pack.validated_property("color", choices=COLOR_CHOICES)
Pack.validated_property("background_color", choices=BACKGROUND_COLOR_CHOICES)

Pack.validated_property("text_align", choices=TEXT_ALIGN_CHOICES)
Pack.validated_property("text_direction", choices=TEXT_DIRECTION_CHOICES, initial=LTR)

Pack.validated_property("font_family", choices=FONT_FAMILY_CHOICES, initial=SYSTEM)
# Pack.list_property('font_family', choices=FONT_FAMILY_CHOICES)
Pack.validated_property("font_style", choices=FONT_STYLE_CHOICES, initial=NORMAL)
Pack.validated_property("font_variant", choices=FONT_VARIANT_CHOICES, initial=NORMAL)
Pack.validated_property("font_weight", choices=FONT_WEIGHT_CHOICES, initial=NORMAL)
Pack.validated_property(
    "font_size", choices=FONT_SIZE_CHOICES, initial=SYSTEM_DEFAULT_FONT_SIZE
)
# Pack.composite_property([
#     'font_family', 'font_style', 'font_variant', 'font_weight', 'font_size'
#     FONT_CHOICES
# ])
