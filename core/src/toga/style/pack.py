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

    # Allow direction to be an anonymous first argument
    # def __init__(self, direction=ROW, **style):
    #     style['direction'] = direction
    #     super().__init__(**style)

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
        def scale(value, scale_factor=viewport.dpi / viewport.baseline_dpi):
            return int(value * scale_factor)

        self._layout_node(node, viewport.width, viewport.height, scale, root=True)
        node.layout.content_top = scale(node.style.padding_top)
        node.layout.content_bottom = scale(node.style.padding_bottom)

        node.layout.content_left = scale(node.style.padding_left)
        node.layout.content_right = scale(node.style.padding_right)

    def _layout_node(self, node, alloc_width, alloc_height, scale, root=False):
        self.__class__._depth += 1
        # self._debug("COMPUTE LAYOUT for", node, "available", alloc_width, alloc_height)

        # Establish available width
        if self.width:
            # If width is specified, use it
            available_width = scale(self.width)
            # self._debug("SPECIFIED WIDTH", available_width)
        else:
            # If no width is specified, assume we're going to use all
            # the available width. If there is an intrinsic width,
            # use it to make sure the width is at least the amount specified.
            available_width = max(
                0, (alloc_width - scale(self.padding_left) - scale(self.padding_right))
            )
            # self._debug("INITIAL AVAILABLE WIDTH", available_width)
            if node.intrinsic.width:
                # self._debug("INTRINSIC WIDTH", node.intrinsic.width)
                try:
                    available_width = max(available_width, node.intrinsic.width.value)
                except AttributeError:
                    available_width = node.intrinsic.width

                # self._debug("ADJUSTED WIDTH", available_width)
            else:
                # self._debug("USE ALL AVAILABLE WIDTH", available_width)
                pass

        # Establish available height
        if self.height:
            # If height is specified, use it.
            available_height = scale(self.height)
            # self._debug("SPECIFIED HEIGHT", available_height)
        else:
            available_height = max(
                0, alloc_height - scale(self.padding_top) - scale(self.padding_bottom)
            )
            # self._debug("INITIAL AVAILABLE HEIGHT", available_height)
            if node.intrinsic.height:
                # self._debug("INTRINSIC HEIGHT", node.intrinsic.height)
                try:
                    available_height = max(
                        available_height, node.intrinsic.height.value
                    )
                except AttributeError:
                    available_height = node.intrinsic.height

                # self._debug("ADJUSTED HEIGHT", available_height)
            else:
                # self._debug("USE ALL AVAILABLE HEIGHT", available_height)
                pass

        if node.children:
            if self.direction == COLUMN:
                width, height = self._layout_column_children(
                    node, available_width, available_height, scale
                )
            else:
                width, height = self._layout_row_children(
                    node, available_width, available_height, scale
                )
        else:
            # self._debug("NO CHILDREN", available_width)
            width = available_width
            height = available_height

        if root:
            # A root node always expands to all available width and height,
            # no matter how much space the child layout requires.
            # self._debug("ROOT NODE")
            width = max(width, available_width)
            height = max(height, available_height)
        else:
            # If an explicit width/height was given, that specification
            # overrides the width/height evaluated by the layout of children
            if self.width:
                width = scale(self.width)
            if self.height:
                height = scale(self.height)

        # self._debug("FINAL SIZE", width, height)
        node.layout.content_width = int(width)
        node.layout.content_height = int(height)

        # self._debug("END LAYOUT", node, node.layout)
        self.__class__._depth -= 1

    def _layout_row_children(self, node, available_width, available_height, scale):
        # self._debug("LAYOUT ROW CHILDREN", available_width)
        # Pass 1: Lay out all children with a hard-specified width, or an
        # intrinsic non-flexible width. While iterating, collect the flex
        # total of remaining elements.
        full_flex = 0
        width = 0
        height = 0
        for child in node.children:
            if child.style.width:
                # self._debug("PASS 1 fixed width", child.style.width)
                child.style._layout_node(
                    child, available_width, available_height, scale
                )
                child_width = (
                    scale(child.style.padding_left)
                    + child.layout.content_width
                    + scale(child.style.padding_right)
                )
                width += child_width
                available_width -= child_width
            elif child.intrinsic.width:
                if hasattr(child.intrinsic.width, "value"):
                    if child.style.flex:
                        full_flex += child.style.flex
                        # self._debug("PASS 1 intrinsic flex width", child.intrinsic.width)
                    else:
                        # self._debug("PASS 1 intrinsic non-flex width", child.intrinsic.width)
                        child.style._layout_node(child, 0, available_height, scale)
                        child_width = (
                            scale(child.style.padding_left)
                            + child.layout.content_width
                            + scale(child.style.padding_right)
                        )
                        width += child_width
                        available_width -= child_width
                else:
                    # self._debug("PASS 1 intrinsic width", child.intrinsic.width)
                    child.style._layout_node(
                        child, available_width, available_height, scale
                    )
                    child_width = (
                        scale(child.style.padding_left)
                        + child.layout.content_width
                        + scale(child.style.padding_right)
                    )
                    width += child_width
                    available_width -= child_width
            else:
                if child.style.flex:
                    # self._debug("PASS 1 unspecified flex width")
                    full_flex += child.style.flex
                else:
                    # self._debug("PASS 1 unspecified non-flex width")
                    child.style._layout_node(
                        child, available_width, available_height, scale
                    )
                    child_width = (
                        scale(child.style.padding_left)
                        + child.layout.content_width
                        + scale(child.style.padding_right)
                    )
                    width += child_width
                    available_width -= child_width

            available_width = max(0, available_width)

        if full_flex:
            # self._debug("q =", available_width, full_flex, available_width / full_flex)
            quantum = available_width / full_flex
        else:
            quantum = 0
        # self._debug("WIDTH QUANTUM", quantum)

        # Pass 2: Lay out children with an intrinsic flexible width,
        # or no width specification at all.
        for child in node.children:
            if child.style.width:
                pass  # Already laid out
            elif child.style.flex:
                if child.intrinsic.width:
                    try:
                        child_alloc_width = max(
                            quantum * child.style.flex, child.intrinsic.width.value
                        )
                        # self._debug("PASS 2 intrinsic flex width", child_alloc_width)

                        child.style._layout_node(
                            child, child_alloc_width, available_height, scale
                        )
                        width += (
                            scale(child.style.padding_left)
                            + child.layout.content_width
                            + scale(child.style.padding_right)
                        )
                    except AttributeError:
                        pass  # Already laid out
                else:
                    if quantum:
                        child_width = quantum * child.style.flex
                    else:
                        child_width = 0

                    # self._debug("PASS 2 unspecified flex width", child_width)
                    available_width -= child_width
                    child.style._layout_node(
                        child, child_width, available_height, scale
                    )
                    width += (
                        scale(child.style.padding_left)
                        + child.layout.content_width
                        + scale(child.style.padding_right)
                    )

        # self._debug("USED WIDTH", width)

        # Pass 3: Set the horizontal position of each child, and establish row height
        offset = 0
        if node.style.text_direction is RTL:
            for child in node.children:
                # self._debug("START CHILD AT RTL HORIZONTAL OFFSET", child, offset)
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
                # self._debug("START CHILD AT LTR HORIZONTAL OFFSET", child, offset)
                offset += scale(child.style.padding_left)
                child.layout.content_left = offset
                offset += child.layout.content_width + scale(child.style.padding_right)
                child_height = (
                    child.layout.content_height
                    + scale(child.style.padding_top)
                    + scale(child.style.padding_bottom)
                )
                height = max(height, child_height)

        # Pass 4: set vertical position of each child.
        for child in node.children:
            extra = height - (
                child.layout.content_height
                + scale(child.style.padding_top)
                + scale(child.style.padding_bottom)
            )
            # self._debug("row extra height", extra)
            if self.alignment is BOTTOM:
                child.layout.content_top = extra + scale(child.style.padding_top)
                # self._debug("align to bottom", child, child.layout.content_top)
            elif self.alignment is CENTER:
                child.layout.content_top = int(extra / 2) + scale(
                    child.style.padding_top
                )
                # self._debug("align to center", child, child.layout.content_top)
            else:
                child.layout.content_top = scale(child.style.padding_top)
                # self._debug("align to top", child, child.layout.content_top)

        return width, height

    def _layout_column_children(self, node, available_width, available_height, scale):
        # self._debug("LAYOUT COLUMN CHILDREN", available_height)
        # Pass 1: Lay out all children with a hard-specified height, or an
        # intrinsic non-flexible height. While iterating, collect the flex
        # total of remaining elements.
        full_flex = 0
        height = 0
        for child in node.children:
            if child.style.height:
                # self._debug("PASS 1 fixed height", child.style.height)
                child.style._layout_node(
                    child, available_width, available_height, scale
                )
                child_height = (
                    scale(child.style.padding_top)
                    + child.layout.content_height
                    + scale(child.style.padding_bottom)
                )
                height += child_height
                available_height -= child_height
            elif child.intrinsic.height:
                if hasattr(child.intrinsic.height, "value"):
                    if child.style.flex:
                        full_flex += child.style.flex
                        # self._debug("PASS 1 intrinsic flex height", child.intrinsic.height)
                    else:
                        # self._debug("PASS 1 intrinsic non-flex height", child.intrinsic.height)
                        child.style._layout_node(child, available_width, 0, scale)
                        child_height = (
                            scale(child.style.padding_top)
                            + child.layout.content_height
                            + scale(child.style.padding_bottom)
                        )
                        height += child_height
                        available_height -= child_height
                else:
                    # self._debug("PASS 1 intrinsic height", child.intrinsic.height)
                    child.style._layout_node(
                        child, available_width, available_height, scale
                    )
                    child_height = (
                        scale(child.style.padding_top)
                        + child.layout.content_height
                        + scale(child.style.padding_bottom)
                    )
                    height += child_height
                    available_height -= child_height
            else:
                if child.style.flex:
                    # self._debug("PASS 1 unspecified flex height")
                    full_flex += child.style.flex
                else:
                    # self._debug("PASS 1 unspecified non-flex height")
                    child.style._layout_node(
                        child, available_width, available_height, scale
                    )
                    child_height = (
                        scale(child.style.padding_top)
                        + child.layout.content_height
                        + scale(child.style.padding_bottom)
                    )
                    height += child_height
                    available_height -= child_height

        available_height = max(0, available_height)
        if full_flex:
            # self._debug("q =", available_height, full_flex, available_height / full_flex)
            quantum = available_height / full_flex
        else:
            quantum = 0
        # self._debug("HEIGHT QUANTUM", quantum)

        # Pass 2: Lay out children with an intrinsic flexible height,
        # or no height specification at all.
        for child in node.children:
            if child.style.height:
                pass  # Already laid out
            elif child.style.flex:
                if child.intrinsic.height:
                    try:
                        child_alloc_height = max(
                            quantum * child.style.flex, child.intrinsic.height.value
                        )
                        # self._debug("PASS 2 intrinsic height", child_alloc_height)

                        child.style._layout_node(
                            child, available_width, child_alloc_height, scale
                        )
                        height += (
                            scale(child.style.padding_top)
                            + child.layout.content_height
                            + scale(child.style.padding_bottom)
                        )
                    except AttributeError:
                        pass  # Already laid out
                else:
                    if quantum:
                        child_height = quantum * child.style.flex
                    else:
                        child_height = 0

                    # self._debug("PASS 2 unspecified height", child_height)
                    available_height -= child_height
                    child.style._layout_node(
                        child, available_width, child_height, scale
                    )
                    height += (
                        scale(child.style.padding_top)
                        + child.layout.content_height
                        + scale(child.style.padding_bottom)
                    )

        # self._debug("USED HEIGHT", height)

        # Pass 3: Set the vertical position of each element, and establish column width
        offset = 0
        width = 0
        for child in node.children:
            # self._debug("START CHILD AT VERTICAL OFFSET", offset)
            offset += scale(child.style.padding_top)
            child.layout.content_top = offset
            offset += child.layout.content_height + scale(child.style.padding_bottom)
            child_width = (
                child.layout.content_width
                + scale(child.style.padding_left)
                + scale(child.style.padding_right)
            )
            width = max(width, child_width)

        # Pass 4: set horizontal position of each child.
        for child in node.children:
            extra = width - (
                child.layout.content_width
                + scale(child.style.padding_left)
                + scale(child.style.padding_right)
            )
            # self._debug("row extra width", extra)
            if self.alignment is RIGHT:
                child.layout.content_left = extra + scale(child.style.padding_left)
                # self._debug("align to right", child, child.layout.content_left)
            elif self.alignment is CENTER:
                child.layout.content_left = int(extra / 2) + scale(
                    child.style.padding_left
                )
                # self._debug("align to center", child, child.layout.content_left)
            else:
                child.layout.content_left = scale(child.style.padding_left)
                # self._debug("align to left", child, child.layout.content_left)

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
            css.append(f"visibility: {self.visibility}")

        # direction
        css.append(f"flex-direction: {self.direction.lower()};")

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

        # width/flex
        if self.width:
            css.append(f"width: {self.width}px;")
        elif self.direction == ROW:
            css.append(f"flex: {self.flex} 0 0;")

        # height/flex
        if self.height:
            css.append(f"width: {self.width}px;")
        elif self.direction == COLUMN:
            css.append(f"flex: {self.flex} 0 0;")

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
            css.append(f"text-align: {self.text_align}")

        # text_direction
        if self.text_direction != LTR:
            css.append(f"text-direction: {self.text_direction}")

        # font-*
        if self.font_family != SYSTEM:
            css.append(f"font-family: {self.font_family};")
        if self.font_size != SYSTEM_DEFAULT_FONT_SIZE:
            css.append(f"font-size: {self.font_size};")
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

Pack.validated_property("width", choices=SIZE_CHOICES, initial=0)
Pack.validated_property("height", choices=SIZE_CHOICES, initial=0)
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
