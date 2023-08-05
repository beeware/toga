from travertino.constants import (
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

from toga.fonts import SYSTEM_DEFAULT_FONT_SIZE, Font

######################################################################
# Display
######################################################################

PACK = "pack"

######################################################################
# Declaration choices
######################################################################

DISPLAY_CHOICES = Choices(PACK, NONE)
VISIBILITY_CHOICES = Choices(VISIBLE, HIDDEN)
DIRECTION_CHOICES = Choices(ROW, COLUMN)
ALIGNMENT_CHOICES = Choices(LEFT, RIGHT, TOP, BOTTOM, CENTER, default=True)

SIZE_CHOICES = Choices(NONE, integer=True)
FLEX_CHOICES = Choices(number=True)

PADDING_CHOICES = Choices(integer=True)

TEXT_ALIGN_CHOICES = Choices(LEFT, RIGHT, CENTER, JUSTIFY, default=True)
TEXT_DIRECTION_CHOICES = Choices(RTL, LTR)

COLOR_CHOICES = Choices(color=True, default=True)
BACKGROUND_COLOR_CHOICES = Choices(TRANSPARENT, color=True, default=True)

FONT_FAMILY_CHOICES = Choices(
    SYSTEM, SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE, string=True
)
# FONT_FAMILY_CHOICES = Choices(SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE, string=True, default=True)
FONT_STYLE_CHOICES = Choices(NORMAL, ITALIC, OBLIQUE)
FONT_VARIANT_CHOICES = Choices(NORMAL, SMALL_CAPS)
FONT_WEIGHT_CHOICES = Choices(NORMAL, BOLD)
FONT_SIZE_CHOICES = Choices(integer=True)


class Pack(BaseStyle):
    class Box(BaseBox):
        pass

    class IntrinsicSize(BaseIntrinsicSize):
        pass

    _depth = -1

    def _debug(self, *args):  # pragma: no cover
        print("    " * self.__class__._depth, *args)

    @property
    def _hidden(self):
        "Does this style declaration define a object that should be hidden"
        return self.visibility == HIDDEN

    def apply(self, prop, value):
        if self._applicator:
            if prop == "text_align":
                if value is None:
                    if self.text_direction == RTL:
                        value = RIGHT
                    else:
                        value = LEFT
                self._applicator.set_text_alignment(value)
            elif prop == "text_direction":
                if self.text_align is None:
                    self._applicator.set_text_alignment(RIGHT if value == RTL else LEFT)
            elif prop == "color":
                self._applicator.set_color(value)
            elif prop == "background_color":
                self._applicator.set_background_color(value)
            elif prop == "visibility":
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

    def layout(self, node, viewport):
        # Precompute `scale_factor` by providing it as a default param.
        # self._debug("=" * 80)
        # self._debug(f"Layout root {node}, available {viewport.width}x{viewport.height}")
        self.__class__._depth = -1

        def scale(value, scale_factor=viewport.dpi / viewport.baseline_dpi):
            return int(value * scale_factor)

        self._layout_node(
            node,
            alloc_width=viewport.width,
            alloc_height=viewport.height,
            scale=scale,
            use_all_height=True,  # root node uses all height
            use_all_width=True,  # root node uses all width
        )
        node.layout.content_top = scale(node.style.padding_top)
        node.layout.content_bottom = scale(node.style.padding_bottom)

        node.layout.content_left = scale(node.style.padding_left)
        node.layout.content_right = scale(node.style.padding_right)

    def _layout_node(
        self,
        node,
        alloc_width,
        alloc_height,
        scale,
        use_all_width,
        use_all_height,
    ):
        self.__class__._depth += 1
        # self._debug(
        #     f"COMPUTE LAYOUT for {node} available "
        #     f"{alloc_width}{'+' if use_all_width else ''}"
        #     " x "
        #     f"{alloc_height}{'+' if use_all_height else ''}"
        # )

        # Establish available width
        if self.width != NONE:
            # If width is specified, use it
            available_width = scale(self.width)
            # self._debug(f"SPECIFIED WIDTH {self.width} (scaled to {available_width})")
        else:
            # If no width is specified, assume we're going to use all
            # the available width. If there is an intrinsic width,
            # use it to make sure the width is at least the amount specified.
            available_width = max(
                0, (alloc_width - scale(self.padding_left) - scale(self.padding_right))
            )
            # self._debug(f"INITIAL {available_width=}")
            if node.intrinsic.width is not None:
                # self._debug(f"INTRINSIC WIDTH {node.intrinsic.width}")
                try:
                    available_width = max(available_width, node.intrinsic.width.value)
                except AttributeError:
                    available_width = node.intrinsic.width

                # self._debug(f"ADJUSTED {available_width=}")
            else:
                # self._debug(f"AUTO {available_width=}")
                pass

        # Establish available height
        if self.height != NONE:
            # If height is specified, use it.
            available_height = scale(self.height)
            # self._debug(f"SPECIFIED HEIGHT {self.height} (scaled to {available_height})")
        else:
            available_height = max(
                0, alloc_height - scale(self.padding_top) - scale(self.padding_bottom)
            )
            # self._debug(f"INITIAL {available_height=}")
            if node.intrinsic.height is not None:
                # self._debug(f"INTRINSIC HEIGHT {node.intrinsic.height}")
                try:
                    available_height = max(
                        available_height, node.intrinsic.height.value
                    )
                except AttributeError:
                    available_height = node.intrinsic.height

                # self._debug(f"ADJUSTED {available_height=}")
            else:
                # self._debug(f"AUTO {available_height=}")
                pass

        if node.children:
            if self.direction == COLUMN:
                width, height = self._layout_column_children(
                    node,
                    available_width=available_width,
                    available_height=available_height,
                    scale=scale,
                    use_all_height=use_all_height,
                    use_all_width=use_all_width,
                )
            else:
                width, height = self._layout_row_children(
                    node,
                    available_width=available_width,
                    available_height=available_height,
                    scale=scale,
                    use_all_height=use_all_height,
                    use_all_width=use_all_width,
                )
            # self._debug(f"HAS CHILDREN {width=} {height=}")
        else:
            width = available_width
            height = available_height
            # self._debug(f"NO CHILDREN {width=} {height=}")

        # If an explicit width/height was given, that specification
        # overrides the width/height evaluated by the layout of children
        if self.width != NONE:
            width = scale(self.width)
        if self.height != NONE:
            height = scale(self.height)

        # self._debug(f"FINAL SIZE {width}x{height}")
        node.layout.content_width = int(width)
        node.layout.content_height = int(height)

        # self._debug("END LAYOUT", node, node.layout)
        self.__class__._depth -= 1

    def _layout_row_children(
        self,
        node,
        available_width,
        available_height,
        scale,
        use_all_width,
        use_all_height,
    ):
        # self._debug(f"LAYOUT ROW CHILDREN {available_width=} {available_height=}")
        # Pass 1: Lay out all children with a hard-specified width, or an
        # intrinsic non-flexible width. While iterating, collect the flex
        # total of remaining elements.
        flex_total = 0
        min_flex_width = 0
        width = 0
        remaining_width = available_width
        for child in node.children:
            # self._debug(f"PASS 1 {child}")
            if child.style.width != NONE:
                # self._debug(f"- fixed width {child.style.width}")
                child.style._layout_node(
                    child,
                    alloc_width=remaining_width,
                    alloc_height=available_height,
                    scale=scale,
                    use_all_width=False,
                    use_all_height=child.style.direction == ROW,
                )
                child_width = (
                    scale(child.style.padding_left)
                    + child.layout.content_width
                    + scale(child.style.padding_right)
                )
                width += child_width
                remaining_width -= child_width
            elif child.intrinsic.width is not None:
                if hasattr(child.intrinsic.width, "value"):
                    if child.style.flex:
                        # self._debug(f"- intrinsic flex width {child.intrinsic.width}")
                        flex_total += child.style.flex
                        child_width = child.intrinsic.width.value
                        remaining_width -= child_width
                        min_flex_width += child_width
                    else:
                        # self._debug(f"- intrinsic non-flex width {child.intrinsic.width}")
                        child.style._layout_node(
                            child,
                            alloc_width=0,
                            alloc_height=available_height,
                            scale=scale,
                            use_all_width=False,
                            use_all_height=child.style.direction == ROW,
                        )
                        child_width = (
                            scale(child.style.padding_left)
                            + child.layout.content_width
                            + scale(child.style.padding_right)
                        )
                        width += child_width
                        remaining_width -= child_width
                else:
                    # self._debug(f"- intrinsic width {child.intrinsic.width}")
                    child.style._layout_node(
                        child,
                        alloc_width=remaining_width,
                        alloc_height=available_height,
                        scale=scale,
                        use_all_width=False,
                        use_all_height=child.style.direction == ROW,
                    )
                    child_width = (
                        scale(child.style.padding_left)
                        + child.layout.content_width
                        + scale(child.style.padding_right)
                    )
                    width += child_width
                    remaining_width -= child_width
            else:
                if child.style.flex:
                    # self._debug("- unspecified flex width")
                    flex_total += child.style.flex
                    child_width = None
                else:
                    # self._debug("- unspecified non-flex width")
                    child.style._layout_node(
                        child,
                        alloc_width=remaining_width,
                        alloc_height=available_height,
                        scale=scale,
                        use_all_width=False,
                        use_all_height=child.style.direction == ROW,
                    )
                    child_width = (
                        scale(child.style.padding_left)
                        + child.layout.content_width
                        + scale(child.style.padding_right)
                    )
                    width += child_width
                    remaining_width -= child_width

            # self._debug(f"  {child_width=} {width=} {remaining_width=} {min_flex_width=}")

        if flex_total > 0:
            quantum = (remaining_width + min_flex_width) / flex_total
            # In an ideal flex layout, all flex children will have a width proportional
            # to their flex value. However, if a flex child has a flexible minimum width
            # constraint that is greater than the ideal width for a balanced flex layout,
            # they need to be removed from the flex calculation.
            # self._debug(f"PASS 1a; {quantum=}")
            for child in node.children:
                if child.style.flex and child.intrinsic.width is not None:
                    try:
                        ideal_width = quantum * child.style.flex
                        if child.intrinsic.width.value > ideal_width:
                            # self._debug(f"- {child} overflows ideal width")
                            flex_total -= child.style.flex
                            min_flex_width -= child.intrinsic.width.value
                    except AttributeError:
                        # Intrinsic width isn't flexible
                        pass

            if flex_total > 0:
                quantum = (remaining_width + min_flex_width) / flex_total
            else:
                quantum = 0
        else:
            quantum = 0
        # self._debug(f"END PASS 1; {min_flex_width=} {quantum=}")

        # Pass 2: Lay out children with an intrinsic flexible width,
        # or no width specification at all.
        for child in node.children:
            # self._debug(f"PASS 2 {child}")
            if child.style.width != NONE:
                # self._debug("- already laid out (explicit width)")
                pass
            elif child.style.flex:
                if child.intrinsic.width is not None:
                    try:
                        child_alloc_width = child.intrinsic.width.value
                        ideal_width = quantum * child.style.flex
                        if ideal_width > child_alloc_width:
                            child_alloc_width = ideal_width
                            # self._debug(f"- flexible intrinsic {child_alloc_width=}")
                        else:
                            # self._debug(f"- overflow flex intrinsic {ideal_width=} {child_alloc_width=}")
                            pass

                        child.style._layout_node(
                            child,
                            alloc_width=child_alloc_width,
                            alloc_height=available_height,
                            scale=scale,
                            use_all_width=True,
                            use_all_height=child.style.direction == ROW,
                        )
                        child_width = (
                            scale(child.style.padding_left)
                            + child.layout.content_width
                            + scale(child.style.padding_right)
                        )
                        width += child_width
                    except AttributeError:
                        # self._debug("- already laid out (fixed intrinsic width)")
                        child_width = None
                else:
                    if quantum:
                        # self._debug(f"- unspecified flex width with {quantum=}")
                        child_width = quantum * child.style.flex
                    else:
                        # self._debug("- unspecified flex width")
                        child_width = 0

                    child.style._layout_node(
                        child,
                        alloc_width=child_width,
                        alloc_height=available_height,
                        scale=scale,
                        use_all_width=True,
                        use_all_height=child.style.direction == ROW,
                    )
                    width += (
                        scale(child.style.padding_left)
                        + child.layout.content_width
                        + scale(child.style.padding_right)
                    )
            else:
                # self._debug("- already laid out (intrinsic non-flex width)")
                child_width = None

            # self._debug(f"  {child_width=}")

        # self._debug(f"PASS 2 COMPLETE; USED {width=}")
        if use_all_width:
            width = max(width, available_width)
        # self._debug(f"COMPUTED {width=}")

        # Pass 3: Set the horizontal position of each child, and establish row height
        offset = 0
        height = 0
        if node.style.text_direction is RTL:
            for child in node.children:
                # self._debug(f"PASS 3 RTL: {child} AT HORIZONTAL {offset=}")
                offset += child.layout.content_width + scale(child.style.padding_right)
                child.layout.content_left = width - offset
                offset += scale(child.style.padding_left)
                child_height = (
                    child.layout.content_height
                    + scale(child.style.padding_top)
                    + scale(child.style.padding_bottom)
                )
                height = max(height, child_height)
        else:
            for child in node.children:
                # self._debug(f"PASS 3 LTR: {child} AT HORIZONTAL {offset=}")
                offset += scale(child.style.padding_left)
                child.layout.content_left = offset
                offset += child.layout.content_width + scale(child.style.padding_right)
                child_height = (
                    child.layout.content_height
                    + scale(child.style.padding_top)
                    + scale(child.style.padding_bottom)
                )
                height = max(height, child_height)

        # self._debug(f"ROW {height=}")
        if use_all_height:
            height = max(height, available_height)
        # self._debug(f"FINAL ROW {height=}")

        # Pass 4: set vertical position of each child.
        for child in node.children:
            # self._debug(f"PASS 4: {child}")
            extra = height - (
                child.layout.content_height
                + scale(child.style.padding_top)
                + scale(child.style.padding_bottom)
            )
            # self._debug(f"- row extra width {extra}")
            if self.alignment is BOTTOM:
                child.layout.content_top = extra + scale(child.style.padding_top)
                # self._debug(f"  align {child} to bottom {child.layout.content_top=}")
            elif self.alignment is CENTER:
                child.layout.content_top = int(extra / 2) + scale(
                    child.style.padding_top
                )
                # self._debug(f"  align {child} to center {child.layout.content_top=}")
            else:
                child.layout.content_top = scale(child.style.padding_top)
                # self._debug(f"  align {child} to top {child.layout.content_top=}")

        return width, height

    def _layout_column_children(
        self,
        node,
        available_width,
        available_height,
        scale,
        use_all_width,
        use_all_height,
    ):
        # self._debug(f"LAYOUT COLUMN CHILDREN {available_width=} {available_height=}")
        # Pass 1: Lay out all children with a hard-specified height, or an
        # intrinsic non-flexible height. While iterating, collect the flex
        # total of remaining elements.
        flex_total = 0
        min_flex_height = 0
        height = 0
        remaining_height = available_height
        for child in node.children:
            # self._debug(f"PASS 1 {child}")
            if child.style.height != NONE:
                # self._debug(f"- fixed height {child.style.height}")
                child.style._layout_node(
                    child,
                    alloc_width=available_width,
                    alloc_height=remaining_height,
                    scale=scale,
                    use_all_width=child.style.direction == COLUMN,
                    use_all_height=False,
                )
                child_height = (
                    scale(child.style.padding_top)
                    + child.layout.content_height
                    + scale(child.style.padding_bottom)
                )
                height += child_height
                remaining_height -= child_height
            elif child.intrinsic.height is not None:
                if hasattr(child.intrinsic.height, "value"):
                    if child.style.flex:
                        # self._debug(f"- intrinsic flex height {child.intrinsic.height}")
                        flex_total += child.style.flex
                        child_height = child.intrinsic.height.value
                        remaining_height -= child_height
                        min_flex_height += child_height
                    else:
                        # self._debug(f"- intrinsic non-flex height {child.intrinsic.height}")
                        child.style._layout_node(
                            child,
                            alloc_width=available_width,
                            alloc_height=0,
                            scale=scale,
                            use_all_width=child.style.direction == COLUMN,
                            use_all_height=False,
                        )
                        child_height = (
                            scale(child.style.padding_top)
                            + child.layout.content_height
                            + scale(child.style.padding_bottom)
                        )
                        height += child_height
                        remaining_height -= child_height
                else:
                    # self._debug(f"- intrinsic height {child.intrinsic.height}")
                    child.style._layout_node(
                        child,
                        alloc_width=available_width,
                        alloc_height=remaining_height,
                        scale=scale,
                        use_all_width=child.style.direction == COLUMN,
                        use_all_height=False,
                    )
                    child_height = (
                        scale(child.style.padding_top)
                        + child.layout.content_height
                        + scale(child.style.padding_bottom)
                    )
                    height += child_height
                    remaining_height -= child_height
            else:
                if child.style.flex:
                    # self._debug("- unspecified flex height")
                    flex_total += child.style.flex
                    child_height = None
                else:
                    # self._debug("- unspecified non-flex height")
                    child.style._layout_node(
                        child,
                        alloc_width=available_width,
                        alloc_height=remaining_height,
                        scale=scale,
                        use_all_width=child.style.direction == COLUMN,
                        use_all_height=False,
                    )
                    child_height = (
                        scale(child.style.padding_top)
                        + child.layout.content_height
                        + scale(child.style.padding_bottom)
                    )
                    height += child_height
                    remaining_height -= child_height
            # self._debug(f"  {child_height=} {height=} {remaining_height=} {min_flex_height=}")

        if flex_total > 0:
            quantum = (remaining_height + min_flex_height) / flex_total
            # In an ideal flex layout, all flex children will have a height proportional
            # to their flex value. However, if a flex child has a flexible minimum
            # height constraint that is greater than the ideal height for a balanced
            # flex layout, they need to be removed from the flex calculation.
            # self._debug(f"PASS 1a; {quantum=}")
            for child in node.children:
                if child.style.flex and child.intrinsic.height is not None:
                    try:
                        ideal_height = quantum * child.style.flex
                        if child.intrinsic.height.value > ideal_height:
                            # self._debug(f"- {child} overflows ideal height")
                            flex_total -= child.style.flex
                            min_flex_height -= child.intrinsic.height.value
                    except AttributeError:
                        # Intrinsic height isn't flexible
                        pass

            if flex_total > 0:
                quantum = (min_flex_height + remaining_height) / flex_total
            else:
                quantum = 0
        else:
            quantum = 0

        # self._debug(f"END PASS 1; {min_flex_height=} {quantum=}")

        # Pass 2: Lay out children with an intrinsic flexible height,
        # or no height specification at all.
        for child in node.children:
            # self._debug(f"PASS 2 {child}")
            if child.style.height != NONE:
                # self._debug("- already laid out (explicit height)")
                pass
            elif child.style.flex:
                if child.intrinsic.height is not None:
                    try:
                        child_alloc_height = child.intrinsic.height.value
                        ideal_height = quantum * child.style.flex
                        if ideal_height > child_alloc_height:
                            child_alloc_height = ideal_height
                            # self._debug(f"- flexible intrinsic {child_alloc_height=}")
                        else:
                            # self._debug(f"- overflow flex intrinsic {ideal_height=} {child_alloc_height=}")
                            pass

                        child.style._layout_node(
                            child,
                            alloc_width=available_width,
                            alloc_height=child_alloc_height,
                            scale=scale,
                            use_all_width=child.style.direction == COLUMN,
                            use_all_height=True,
                        )
                        child_height = (
                            scale(child.style.padding_top)
                            + child.layout.content_height
                            + scale(child.style.padding_bottom)
                        )
                        height += child_height
                    except AttributeError:
                        # self._debug("- already laid out (fixed intrinsic height)")
                        child_height = None
                else:
                    if quantum:
                        # self._debug(f"- unspecified flex height with {quantum=}")
                        child_height = quantum * child.style.flex
                    else:
                        # self._debug("- unspecified flex height")
                        child_height = 0

                    child.style._layout_node(
                        child,
                        alloc_width=available_width,
                        alloc_height=child_height,
                        scale=scale,
                        use_all_width=child.style.direction == COLUMN,
                        use_all_height=True,
                    )
                    child_height = (
                        scale(child.style.padding_top)
                        + child.layout.content_height
                        + scale(child.style.padding_bottom)
                    )
                    height += child_height
            else:
                # self._debug("- already laid out (intrinsic non-flex height)")
                child_height = None

            # self._debug(f"  {child_height=}")

        # self._debug(f"PASS 2 COMPLETE; USED {height=}")
        if use_all_height:
            height = max(height, available_height)
        # self._debug(f"COMPUTED {height=}")

        # Pass 3: Set the vertical position of each element, and establish column width
        offset = 0
        width = 0
        for child in node.children:
            # self._debug(f"PASS 3: {child} AT VERTICAL OFFSET {offset}")
            offset += scale(child.style.padding_top)
            child.layout.content_top = offset
            offset += child.layout.content_height + scale(child.style.padding_bottom)
            child_width = (
                child.layout.content_width
                + scale(child.style.padding_left)
                + scale(child.style.padding_right)
            )
            width = max(width, child_width)

        # self._debug(f"ROW {width=}")
        if use_all_width:
            width = max(width, available_width)
        # self._debug(f"FINAL ROW {width=}")

        # Pass 4: set horizontal position of each child.
        for child in node.children:
            # self._debug(f"PASS 4: {child}")
            extra = width - (
                child.layout.content_width
                + scale(child.style.padding_left)
                + scale(child.style.padding_right)
            )
            # self._debug(f"-  row extra width {extra}")
            if self.alignment is RIGHT:
                child.layout.content_left = extra + scale(child.style.padding_left)
                # self._debug(f"  align {child} to right {child.layout.content_left=}")
            elif self.alignment is CENTER:
                child.layout.content_left = int(extra / 2) + scale(
                    child.style.padding_left
                )
                # self._debug(f"  align {child} to center {child.layout.content_left=}")
            else:
                child.layout.content_left = scale(child.style.padding_left)
                # self._debug(f"  align {child} to left {child.layout.content_left=}")

        return width, height

    def __css__(self):
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

        # alignment
        if self.direction == ROW:
            if self.alignment:
                if self.alignment == LEFT:
                    css.append("align-items: start;")
                elif self.alignment == RIGHT:
                    css.append("align-items: end;")
                elif self.alignment == CENTER:
                    css.append("align-items: center;")
        else:
            if self.alignment:
                if self.alignment == TOP:
                    css.append("align-items: start;")
                elif self.alignment == BOTTOM:
                    css.append("align-items: end;")
                elif self.alignment == CENTER:
                    css.append("align-items: center;")

        # padding_*
        if self.padding_top:
            css.append(f"margin-top: {self.padding_top}px;")
        if self.padding_bottom:
            css.append(f"margin-bottom: {self.padding_bottom}px;")
        if self.padding_left:
            css.append(f"margin-left: {self.padding_left}px;")
        if self.padding_right:
            css.append(f"margin-right: {self.padding_right}px;")

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
Pack.validated_property("alignment", choices=ALIGNMENT_CHOICES)

Pack.validated_property("width", choices=SIZE_CHOICES, initial=NONE)
Pack.validated_property("height", choices=SIZE_CHOICES, initial=NONE)
Pack.validated_property("flex", choices=FLEX_CHOICES, initial=0)

Pack.validated_property("padding_top", choices=PADDING_CHOICES, initial=0)
Pack.validated_property("padding_right", choices=PADDING_CHOICES, initial=0)
Pack.validated_property("padding_bottom", choices=PADDING_CHOICES, initial=0)
Pack.validated_property("padding_left", choices=PADDING_CHOICES, initial=0)
Pack.directional_property("padding%s")

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
