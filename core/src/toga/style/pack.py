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
from travertino.node import Node
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
        def content(self, name):
            return getattr(self, f"content_{name}")

        def min_content(self, name):
            return getattr(self, f"min_content_{name}")

    class IntrinsicSize(BaseIntrinsicSize):
        def dim(self, name):
            return getattr(self, name)

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

        return super().__setitem__(
            self._update_property_name(name.replace("-", "_")), value
        )

    def __delitem__(self, name):
        if name in {"padding", "margin"}:
            delattr(self, name)
            return

        return super().__delitem__(self._update_property_name(name.replace("-", "_")))

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

    @classmethod
    def layout(cls, node: Node, viewport: Any) -> None:
        # cls._debug("=" * 80)
        # cls._debug(
        #     f"Layout root {node}, available {viewport.width}x{viewport.height}"
        # )
        cls._depth = -1

        cls._layout_node(
            node,
            alloc_width=viewport.width,
            alloc_height=viewport.height,
            use_all_height=True,  # root node uses all height
            use_all_width=True,  # root node uses all width
        )
        node.layout.content_top = node.style.margin_top
        node.layout.content_bottom = node.style.margin_bottom

        node.layout.content_left = node.style.margin_left
        node.layout.content_right = node.style.margin_right

    @classmethod
    def _layout_node(
        cls,
        node: Node,
        alloc_width: int,
        alloc_height: int,
        use_all_width: bool,
        use_all_height: bool,
    ) -> None:
        cls._depth += 1
        # cls._debug(
        #     f"COMPUTE LAYOUT for {node} available "
        #     f"{alloc_width}{'+' if use_all_width else ''}"
        #     " x "
        #     f"{alloc_height}{'+' if use_all_height else ''}"
        # )

        # Establish available width
        if node.style.width != NONE:
            # If width is specified, use it
            available_width = node.style.width
            min_width = node.style.width
            # cls._debug(f"SPECIFIED WIDTH {node.style.width}")
        else:
            # If no width is specified, assume we're going to use all
            # the available width. If there is an intrinsic width,
            # use it to make sure the width is at least the amount specified.
            available_width = max(
                0, (alloc_width - node.style.margin_left - node.style.margin_right)
            )
            # cls._debug(f"INITIAL {available_width=}")
            if node.intrinsic.width is not None:
                # cls._debug(f"INTRINSIC WIDTH {node.intrinsic.width}")
                try:
                    min_width = node.intrinsic.width.value
                    available_width = max(available_width, min_width)
                except AttributeError:
                    available_width = node.intrinsic.width
                    min_width = node.intrinsic.width

                # cls._debug(f"ADJUSTED {available_width=}")
            else:
                # cls._debug(f"AUTO {available_width=}")
                min_width = 0

        # Establish available height
        if node.style.height != NONE:
            # If height is specified, use it.
            available_height = node.style.height
            min_height = node.style.height
            # cls._debug(f"SPECIFIED HEIGHT {node.style.height}")
        else:
            available_height = max(
                0,
                alloc_height - node.style.margin_top - node.style.margin_bottom,
            )
            # cls._debug(f"INITIAL {available_height=}")
            if node.intrinsic.height is not None:
                # cls._debug(f"INTRINSIC HEIGHT {node.intrinsic.height}")
                try:
                    min_height = node.intrinsic.height.value
                    available_height = max(available_height, min_height)
                except AttributeError:
                    available_height = node.intrinsic.height
                    min_height = node.intrinsic.height

                # cls._debug(f"ADJUSTED {available_height=}")
            else:
                # cls._debug(f"AUTO {available_height=}")
                min_height = 0

        if node.children:
            if node.style.direction == COLUMN:
                min_height, height, min_width, width = cls._layout_children(
                    node,
                    direction=COLUMN,
                    available_main=available_height,
                    available_cross=available_width,
                    use_all_main=use_all_height,
                    use_all_cross=use_all_width,
                )
            else:
                min_width, width, min_height, height = cls._layout_children(
                    node,
                    direction=ROW,
                    available_main=available_width,
                    available_cross=available_height,
                    use_all_main=use_all_width,
                    use_all_cross=use_all_height,
                )
            # cls._debug(f"HAS CHILDREN {min_width=} {width=} {min_height=} {height=}")
        else:
            width = available_width
            height = available_height
            # cls._debug(f"NO CHILDREN {min_width=} {width=} {min_height=} {height=}")

        # If an explicit width/height was given, that specification
        # overrides the width/height evaluated by the layout of children
        if node.style.width != NONE:
            width = node.style.width
            min_width = width
        if node.style.height != NONE:
            height = node.style.height
            min_height = height

        # cls._debug(f"FINAL SIZE {min_width}x{min_height} {width}x{height}")
        node.layout.content_width = int(width)
        node.layout.content_height = int(height)

        node.layout.min_content_width = int(min_width)
        node.layout.min_content_height = int(min_height)

        # cls._debug("END LAYOUT", node, node.layout)
        cls._depth -= 1

    @classmethod
    def _layout_node_in_direction(
        cls,
        node: Node,
        direction: str,  # ROW | COLUMN
        alloc_main: int,
        alloc_cross: int,
        use_all_main: bool,
        use_all_cross: bool,
    ) -> None:
        if direction == COLUMN:
            cls._layout_node(
                node,
                alloc_height=alloc_main,
                alloc_width=alloc_cross,
                use_all_height=use_all_main,
                use_all_width=use_all_cross,
            )
        else:
            cls._layout_node(
                node,
                alloc_width=alloc_main,
                alloc_height=alloc_cross,
                use_all_width=use_all_main,
                use_all_height=use_all_cross,
            )

    @classmethod
    def _layout_children(
        cls,
        node: Node,
        direction: str,  # ROW | COLUMN
        available_main: int,
        available_cross: int,
        use_all_main: bool,
        use_all_cross: bool,
    ) -> tuple[int, int, int, int]:  # min_main, main, min_cross, cross
        # Pass 1: Lay out all children with a hard-specified main-axis dimension, or an
        # intrinsic non-flexible dimension. While iterating, collect the flex
        # total of remaining elements.
        flex_total = 0
        min_flex = 0
        main = 0
        min_main = 0
        remaining_main = available_main

        horizontal = (
            (LEFT, RIGHT) if node.style.text_direction == LTR else (RIGHT, LEFT)
        )
        if direction == COLUMN:
            main_name, cross_name = "height", "width"
            main_start, main_end = TOP, BOTTOM
            cross_start, cross_end = horizontal
        else:
            main_name, cross_name = "width", "height"
            main_start, main_end = horizontal
            cross_start, cross_end = TOP, BOTTOM

        # cls._debug(
        #     f"LAYOUT {direction.upper()} CHILDREN "
        #     f"{main_name=} {available_main=} {available_cross=}"
        # )

        for i, child in enumerate(node.children):
            # cls._debug(f"PASS 1 {child}")
            if child.style[main_name] != NONE:
                # cls._debug(f"- fixed {main_name} {child.style[main_name]}")
                child.style._layout_node_in_direction(
                    child,
                    direction=direction,
                    alloc_main=remaining_main,
                    alloc_cross=available_cross,
                    use_all_main=False,
                    use_all_cross=child.style.direction == direction,
                )
                child_content_main = child.layout.content(main_name)

                # It doesn't matter how small the children can be laid out; we have an
                # intrinsic size; so don't use min_content.(main_name)
                min_child_content_main = child.layout.content(main_name)

            elif child.intrinsic.dim(main_name) is not None:
                if hasattr(child.intrinsic.dim(main_name), "value"):
                    if child.style.flex:
                        # cls._debug(
                        #     f"- intrinsic flex {main_name} "
                        #     f"{child.intrinsic.dim(main_name)=}"
                        # )
                        flex_total += child.style.flex
                        # Final child content size will be computed in pass 2, after the
                        # amount of flexible space is known. For now, set an initial
                        # content main-axis size based on the intrinsic size, which
                        # will be the minimum possible allocation.
                        child_content_main = child.intrinsic.dim(main_name).value
                        min_child_content_main = child.intrinsic.dim(main_name).value
                        min_flex += (
                            child.style[f"margin_{main_start}"]
                            + child_content_main
                            + child.style[f"margin_{main_end}"]
                        )
                    else:
                        # cls._debug(
                        #     f"- intrinsic non-flex {main_name} "
                        #     f"{child.intrinsic.dim(main_name)=}"
                        # )
                        child.style._layout_node_in_direction(
                            child,
                            direction=direction,
                            alloc_main=0,
                            alloc_cross=available_cross,
                            use_all_main=False,
                            use_all_cross=child.style.direction == direction,
                        )

                        child_content_main = child.layout.content(main_name)

                        # It doesn't matter how small the children can be laid out; we
                        # have an intrinsic size; so don't use
                        # layout.min_content(main_name)
                        min_child_content_main = child.layout.content(main_name)
                else:
                    # cls._debug(
                    #     f"- intrinsic {main_name} {child.intrinsic.dim(main_name)=}"
                    # )
                    child.style._layout_node_in_direction(
                        child,
                        direction=direction,
                        alloc_main=remaining_main,
                        alloc_cross=available_cross,
                        use_all_main=False,
                        use_all_cross=child.style.direction == direction,
                    )

                    child_content_main = child.layout.content(main_name)

                    # It doesn't matter how small the children can be laid out; we have
                    # an intrinsic size; so don't use layout.min_content(main_name)
                    min_child_content_main = child.layout.content(main_name)
            else:
                if child.style.flex:
                    # cls._debug(f"- unspecified flex {main_name}")
                    flex_total += child.style.flex
                    # Final child content size will be computed in pass 2, after the
                    # amount of flexible space is known. For now, use 0 as the minimum,
                    # as that's the best hint the widget style can give.
                    child_content_main = 0
                    min_child_content_main = 0
                else:
                    # cls._debug(f"- unspecified non-flex {main_name}")
                    child.style._layout_node_in_direction(
                        child,
                        direction=direction,
                        alloc_main=remaining_main,
                        alloc_cross=available_cross,
                        use_all_main=False,
                        use_all_cross=child.style.direction == direction,
                    )
                    child_content_main = child.layout.content(main_name)
                    min_child_content_main = child.layout.min_content(main_name)

            gap = 0 if i == 0 else node.style.gap
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

            # cls._debug(f"  {min_child_main=} {min_main=} {min_flex=}")
            # cls._debug(f"  {child_main=} {main=} {remaining_main=}")

        if flex_total > 0:
            quantum = (remaining_main + min_flex) / flex_total
            # In an ideal flex layout, all flex children will have a main-axis size
            # proportional to their flex value. However, if a flex child has a flexible
            # minimum main-axis size constraint that is greater than the ideal
            # main-axis size for a balanced flex layout, they need to be removed from
            # the flex calculation.

            # cls._debug(f"PASS 1a; {quantum=}")
            for child in node.children:
                child_intrinsic_main = child.intrinsic.dim(main_name)
                if child.style.flex and child_intrinsic_main is not None:
                    try:
                        ideal_main = quantum * child.style.flex
                        if child_intrinsic_main.value > ideal_main:
                            # cls._debug(f"- {child} overflows ideal main dimension")
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

        # cls._debug(f"END PASS 1; {min_main=} {main=} {min_flex=} {quantum=}")

        # Pass 2: Lay out children with an intrinsic flexible main-axis size, or no
        # main-axis size specification at all.
        for child in node.children:
            # cls._debug(f"PASS 2 {child}")
            if child.style[main_name] != NONE:
                # cls._debug(f"- already laid out (explicit {main_name})")
                pass
            elif child.style.flex:
                if child.intrinsic.dim(main_name) is not None:
                    try:
                        child_alloc_main = (
                            child.style[f"margin_{main_start}"]
                            + child.intrinsic.dim(main_name).value
                            + child.style[f"margin_{main_end}"]
                        )
                        ideal_main = quantum * child.style.flex
                        # cls._debug(
                        #     f"- flexible intrinsic {main_name} {child_alloc_main=}"
                        # )
                        if ideal_main > child_alloc_main:
                            # cls._debug(f"  {ideal_main=}")
                            child_alloc_main = ideal_main

                        child.style._layout_node_in_direction(
                            child,
                            direction=direction,
                            alloc_main=child_alloc_main,
                            alloc_cross=available_cross,
                            use_all_main=True,
                            use_all_cross=child.style.direction == direction,
                        )
                        # Our main-axis dimension calculation already takes into account
                        # the intrinsic size; that has now expanded as a result of
                        # layout, so adjust to use the new layout size. Min size may
                        # also change, by the same scheme, because the flex child can
                        # itself have children, and those grandchildren have now been
                        # laid out.

                        # cls._debug(
                        #     f"  sub {child.intrinsic.dim(main_name).value=}"
                        # )
                        # cls._debug(
                        #     f"  add {child.layout.content(main_name)=}"
                        # )
                        # cls._debug(
                        #     f"  add min {child.layout.min_content(main_name)=}"
                        # )
                        main = (
                            main
                            - child.intrinsic.dim(main_name).value
                            + child.layout.content(main_name)
                        )
                        min_main = (
                            min_main
                            - child.intrinsic.dim(main_name).value
                            + child.layout.min_content(main_name)
                        )
                    except AttributeError:
                        # cls._debug(
                        #     "- already laid out (fixed intrinsic main-axis dimension)"
                        # )
                        pass
                else:
                    if quantum:
                        # cls._debug(
                        #     f"- unspecified flex {main_name} with {quantum=}"
                        # )
                        child_alloc_main = quantum * child.style.flex
                    else:
                        # cls._debug(f"- unspecified flex {main_name}")
                        child_alloc_main = (
                            child.style[f"margin_{main_start}"]
                            + child.style[f"margin_{main_end}"]
                        )

                    child.style._layout_node_in_direction(
                        child,
                        direction=direction,
                        alloc_main=child_alloc_main,
                        alloc_cross=available_cross,
                        use_all_main=True,
                        use_all_cross=child.style.direction == direction,
                    )
                    # We now know the final min_main/main that accounts for flexible
                    # sizing; add that to the overall.

                    # cls._debug(f"  add {child.layout.min_content(main_name)=}")
                    # cls._debug(f"  add {child.layout.content(main_name)=}")
                    main += child.layout.content(main_name)
                    min_main += child.layout.min_content(main_name)

            else:
                # cls._debug(f"- already laid out (intrinsic non-flex {main_name})")
                pass

            # cls._debug(f"{main_name} {min_main=} {main=}")

        # cls._debug(f"PASS 2 COMPLETE; USED {main=} {main_name}")
        if use_all_main:
            main = max(main, available_main)
        # cls._debug(f"COMPUTED {main_name} {min_main=} {main=}")

        # Pass 3: Set the main-axis position of each element, and establish box's
        # cross-axis dimension
        offset = 0
        cross = 0
        min_cross = 0
        for child in node.children:
            # cls._debug(f"PASS 3: {child} AT MAIN-AXIS OFFSET {offset}")
            if main_start == RIGHT:
                # Needs special casing, since it's still ultimately content_left that
                # needs to be set.
                offset += child.layout.content_width + child.style.margin_right
                child.layout.content_left = main - offset
                offset += child.style.margin_left
            else:
                offset += child.style[f"margin_{main_start}"]
                setattr(child.layout, f"content_{main_start}", offset)
                offset += child.layout.content(main_name)
                offset += child.style[f"margin_{main_end}"]

            offset += node.style.gap

            child_cross = (
                child.layout.content(cross_name)
                + child.style[f"margin_{cross_start}"]
                + child.style[f"margin_{cross_end}"]
            )
            cross = max(cross, child_cross)

            min_child_cross = (
                child.style[f"margin_{cross_start}"]
                + child.layout.min_content(cross_name)
                + child.style[f"margin_{cross_end}"]
            )
            min_cross = max(min_cross, min_child_cross)

        # cls._debug(f"{direction.upper()} {min_cross=} {cross=}")
        if use_all_cross:
            cross = max(cross, available_cross)
        # cls._debug(f"FINAL {direction.upper()} {min_width=} {width=}")

        # Pass 4: Set cross-axis position of each child.

        # Translate RTL into left-origin, which effectively flips start/end item
        # alignment.
        align_items = node.style.align_items
        if cross_start == RIGHT:
            cross_start = LEFT

            if align_items == START:
                align_items = END
            elif align_items == END:
                align_items = START

        for child in node.children:
            # cls._debug(f"PASS 4: {child}")
            extra = cross - (
                child.layout.content(cross_name)
                + child.style[f"margin_{cross_start}"]
                + child.style[f"margin_{cross_end}"]
            )
            # cls._debug(f"-  {direction} extra {cross_name} {extra}")

            if align_items == END:
                cross_start_value = extra + child.style[f"margin_{cross_start}"]
                # cls._debug(f"  align {child} to {cross_end}")

            elif align_items == CENTER:
                cross_start_value = (
                    int(extra / 2) + child.style[f"margin_{cross_start}"]
                )
                # cls._debug(f"  align {child} to center")

            else:
                cross_start_value = child.style[f"margin_{cross_start}"]
                # cls._debug(f"  align {child} to {cross_start} ")

            setattr(child.layout, f"content_{cross_start}", cross_start_value)
            # cls._debug(f"  {child.layout.content(cross_start)=}")

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
