from travertino.constants import (
    NORMAL, SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE, ITALIC, OBLIQUE, SMALL_CAPS, BOLD,
    LEFT, RIGHT, TOP, BOTTOM, CENTER, JUSTIFY, RTL, LTR, TRANSPARENT
)
from travertino.declaration import (
    Choices, validated_property, directional_property, BaseStyle
)
from travertino.layout import BaseBox
from travertino.size import BaseIntrinsicSize

######################################################################
# Display
######################################################################

FLOW = 'flow'

######################################################################
# Visibility
######################################################################

VISIBLE = 'visible'
HIDDEN = 'hidden'
NONE = 'none'

######################################################################
# Direction
######################################################################

ROW = 'row'
COLUMN = 'column'


DISPLAY_CHOICES = Choices(FLOW, NONE)
VISIBILITY_CHOICES = Choices(VISIBLE, HIDDEN, NONE)
DIRECTION_CHOICES = Choices(ROW, COLUMN)
ALIGNMENT_CHOICES = Choices(LEFT, RIGHT, TOP, BOTTOM, CENTER, default=True)

SIZE_CHOICES = Choices(NONE, integer=True)
FLEX_CHOICES = Choices(number=True)

PADDING_CHOICES = Choices(integer=True)

TEXT_ALIGN_CHOICES = Choices(LEFT, RIGHT, CENTER, JUSTIFY, default=True)
TEXT_DIRECTION_CHOICES = Choices(RTL, LTR)

COLOR_CHOICES = Choices(color=True, default=True)
BACKGROUND_COLOR_CHOICES = Choices(TRANSPARENT, color=True, default=True)

FONT_FAMILY_CHOICES = Choices(SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE, string=True, default=True)
FONT_STYLE_CHOICES = Choices(NORMAL, ITALIC, OBLIQUE)
FONT_VARIANT_CHOICES = Choices(NORMAL, SMALL_CAPS)
FONT_WEIGHT_CHOICES = Choices(NORMAL, BOLD)
FONT_SIZE_CHOICES = Choices(integer=True, default=True)


class Flow(BaseStyle):
    class Box(BaseBox):
        pass

    class IntrinsicSize(BaseIntrinsicSize):
        pass

    # Allow direction to be an anonymous first argument
    # def __init__(self, direction=ROW, **style):
    #     style['direction'] = direction
    #     super().__init__(**style)

    display = validated_property('display', choices=DISPLAY_CHOICES, initial=FLOW)
    visibility = validated_property('visibility', choices=VISIBILITY_CHOICES, initial=VISIBLE)
    direction = validated_property('direction', choices=DIRECTION_CHOICES, initial=ROW)
    alignment = validated_property('alignment', choices=ALIGNMENT_CHOICES)

    width = validated_property('width', choices=SIZE_CHOICES, initial=0)
    height = validated_property('height', choices=SIZE_CHOICES, initial=0)
    flex = validated_property('flex', choices=FLEX_CHOICES, initial=0)

    padding_top = validated_property('padding_top', choices=PADDING_CHOICES, initial=0)
    padding_right = validated_property('padding_right', choices=PADDING_CHOICES, initial=0)
    padding_bottom = validated_property('padding_bottom', choices=PADDING_CHOICES, initial=0)
    padding_left = validated_property('padding_left', choices=PADDING_CHOICES, initial=0)
    padding = directional_property('padding%s')

    color = validated_property('color', choices=COLOR_CHOICES)
    background_color = validated_property('background_color', choices=BACKGROUND_COLOR_CHOICES)

    text_align = validated_property('text_align', choices=TEXT_ALIGN_CHOICES)
    text_direction = validated_property('text_direction', choices=TEXT_DIRECTION_CHOICES, initial=RTL)

    # font_family = list_property('font_family', choices=FONT_FAMILY_CHOICES)
    font_style = validated_property('font_style', choices=FONT_STYLE_CHOICES, initial=NORMAL)
    font_variant = validated_property('font_variant', choices=FONT_VARIANT_CHOICES, initial=NORMAL)
    font_weight = validated_property('font_weight', choices=FONT_WEIGHT_CHOICES, initial=NORMAL)
    font_size = validated_property('font_size', choices=FONT_SIZE_CHOICES)
    # font = composite_property([
    #     'font_family', 'font_style', 'font_variant', 'font_weight', 'font_size'
    #     FONT_CHOICES
    # ])

    _depth = -1

    def _debug(self, *args):
        # print('    ' * self.__class__._depth, *args)
        pass

    def layout(self, node, viewport):
        self._layout_node(node, viewport.width, viewport.height, viewport.dpi)
        node.layout.content_top = node.style.padding_top
        node.layout.content_bottom = node.style.padding_bottom

        node.layout.content_left = node.style.padding_left
        node.layout.content_right = node.style.padding_right

    def _layout_node(self, node, alloc_width, alloc_height, view_dpi):
        self.__class__._depth += 1
        self._debug("COMPUTE LAYOUT for", node, "available", alloc_width, alloc_height)

        if self.direction == COLUMN:
            self._debug("LAYOUT COLUMN...")
            self._layout_column(node, alloc_width, alloc_height, view_dpi)
        else:
            self._debug("LAYOUT ROW...")
            self._layout_row(node, alloc_width, alloc_height, view_dpi)

        self._debug("END LAYOUT", node, node.layout)
        self.__class__._depth -= 1

    def _layout_row(self, node, alloc_width, alloc_height, view_dpi):
        # Establish width
        if self.width:
            # If width is specified, use it
            available_width = self.width
            self._debug("SPECIFIED WIDTH", available_width)
        else:
            # If no width is specified, assume we're going to use all
            # the available width. If there is an intrinsic width,
            # use it to make user the width is at lea
            available_width = max(0, alloc_width - self.padding_left - self.padding_right)
            if node.intrinsic.width:
                self._debug("INTRINSIC WIDTH", node.intrinsic.width)
                try:
                    available_width = max(available_width, node.intrinsic.width.value)
                except AttributeError:
                    available_width = max(available_width, node.intrinsic.width)

                self._debug("ADJUSTED WIDTH", available_width)
            else:
                self._debug("USE ALL AVAILABLE WIDTH", available_width)

        if node.children:
            self._debug("LAYOUT CHILDREN", available_width)
            # Pass 1: Lay out all children with a hard-specified width, or an
            # intrinsic non-flexible width. While iterating, collect the flex
            # total of remaining elements.
            full_flex = 0
            width = 0
            for child in node.children:
                if child.style.width:
                    child_width = child.style.width + child.style.padding_left + child.style.padding_right
                    available_width -= child_width
                    self._debug("PASS 1 fixed width", child_width)
                    child.style._layout_node(child, child_width, alloc_height, view_dpi)
                    width += child_width
                elif child.intrinsic.width:
                    if hasattr(child.intrinsic.width, 'value'):
                        full_flex += child.style.flex
                        self._debug("PASS 1 intrinsic flex")
                    else:
                        child_width = child.intrinsic.width
                        child_width += child.style.padding_left + child.style.padding_right
                        available_width -= child_width
                        self._debug("PASS 1 intrinsic width", child_width)
                        child.style._layout_node(child, child_width, alloc_height, view_dpi)
                        width += child_width
                else:
                    self._debug("PASS 1 unspecified flex")
                    full_flex += child.style.flex

            available_width = max(0, available_width)
            if full_flex:
                self._debug("q =",available_width, full_flex, available_width / full_flex)
                quantum = available_width / full_flex
            else:
                quantum = None
            self._debug("QUANTUM", quantum)

            # Pass 2: Lay out children with an intrinsic flexible width,
            # or no width specification at all.
            left_position = 0
            for child in node.children:
                if child.style.width:
                    pass  # Already laid out
                elif child.intrinsic.width:
                    try:
                        child_width = child.intrinsic.width.value
                        if quantum:
                            child_width = max(quantum * child.style.flex, child_width)

                        self._debug("PASS 2 intrinsic width", child_width)

                        # child_width
                        available_width -= child_width
                        child.style._layout_node(child, child_width, alloc_height, view_dpi)
                        width += child.style.padding_left + child.layout.content_width + child.style.padding_right
                    except AttributeError:
                        pass  # Already laid out
                else:
                    if quantum:
                        child_width = quantum * child.style.flex
                    else:
                        child_width = 0

                    self._debug("PASS 2 unspecified width", child_width)
                    available_width -= child_width
                    child.style._layout_node(child, child_width, alloc_height, view_dpi)
                    width += child.style.padding_left + child.layout.content_width + child.style.padding_right

                # On this last pass, we can now set the horizontal position, too.
                left_position += child.style.padding_left
                child.layout.content_left = left_position
                left_position += child.layout.content_width + child.style.padding_right

            self._debug("USED WIDTH", width)
        else:
            self._debug("NO CHILDREN", available_width)
            width = available_width

        self._debug("FINAL WIDTH", width)
        node.layout.content_width = int(width)

        # Establish height, and position children vertically and horizontally.
        if self.height:
            height = self.height
            self._debug("SPECIFIED HEIGHT", height)
        else:
            available_height = max(0, alloc_height - self.padding_top - self.padding_bottom)
            if node.children:
                height = max(
                    child.layout.content_height + child.style.padding_top + child.style.padding_bottom
                    for child in node.children
                )
                self._debug("ROW HEIGHT", height)
            else:
                if node.intrinsic.height:
                    self._debug("INTRINSIC HEIGHT", node.intrinsic.height)
                    try:
                        height = node.intrinsic.height.value
                    except AttributeError:
                        height = node.intrinsic.height

                    self._debug("ADJUSTED HEIGHT", height)
                else:
                    height = available_height
                    self._debug("USE ALL AVAILABLE HEIGHT", available_height)

        node.layout.content_height = int(height)

        for child in node.children:
            extra = height - child.layout.content_height + child.style.padding_top + child.style.padding_bottom
            self._debug("row extra height", extra)
            if self.alignment is BOTTOM:
                child.layout.content_top = extra + child.style.padding_top
                self._debug("align to bottom", child.layout.content_top)
            elif self.alignment is CENTER:
                child.layout.content_top = int(extra / 2) + child.style.padding_top
                self._debug("align to center", child.layout.content_top)
            else:
                child.layout.content_top = child.style.padding_top
                self._debug("align to top", child.layout.content_top)

    def _layout_column(self, node, alloc_width, alloc_height, view_dpi):
        # Establish height
        if self.height:
            # If height is specified, use it
            available_height = self.height
            self._debug("SPECIFIED HEIGHT", available_height)
        else:
            # If no height is specified, assume we're going to use all
            # the available height. If there is an intrinsic height,
            # use it to make user the height is at lea
            available_height = max(0, alloc_height - self.padding_top - self.padding_bottom)
            if node.intrinsic.height:
                self._debug("INTRINSIC HEIGHT", node.intrinsic.height)
                try:
                    available_height = max(available_height, node.intrinsic.height.value)
                except AttributeError:
                    available_height = max(available_height, node.intrinsic.height)

                self._debug("ADJUSTED HEIGHT", available_height)
            else:
                self._debug("USE ALL AVAILABLE HEIGHT", available_height)

        if node.children:
            self._debug("LAYOUT CHILDREN", available_height)
            # Pass 1: Lay out all children with a hard-specified height, or an
            # intrinsic non-flexible height. While iterating, collect the flex
            # total of remaining elements.
            full_flex = 0
            height = 0
            for child in node.children:
                if child.style.height:
                    child_height = child.style.height + child.style.padding_top + child.style.padding_bottom
                    available_height -= child_height
                    self._debug("PASS 1 fixed height", child_height)
                    child.style._layout_node(child, alloc_width, child_height, view_dpi)
                    height += child_height
                elif child.intrinsic.height:
                    if hasattr(child.intrinsic.height, 'value'):
                        full_flex += child.style.flex
                        self._debug("PASS 1 intrinsic flex")
                    else:
                        child_height = child.intrinsic.height
                        child_height += child.style.padding_top + child.style.padding_bottom
                        available_height -= child_height
                        self._debug("PASS 1 intrinsic height", child_height)
                        child.style._layout_node(child, alloc_width, child_height, view_dpi)
                        height += child_height
                else:
                    self._debug("PASS 1 unspecified flex")
                    full_flex += child.style.flex

            available_height = max(0, available_height)
            if full_flex:
                self._debug("q =", available_height, full_flex, available_height / full_flex)
                quantum = available_height / full_flex
            else:
                quantum = None
            self._debug("QUANTUM", quantum)

            # Pass 2: Lay out children with an intrinsic flexible height,
            # or no height specification at all.
            top_position = 0
            for child in node.children:
                if child.style.height:
                    pass  # Already laid out
                elif child.intrinsic.height:
                    try:
                        child_height = child.intrinsic.height.value
                        height += child_height
                        if quantum:
                            child_height = max(quantum * child.style.flex, child_height)

                        self._debug("PASS 2 intrinsic height", child_height)

                        # child_height
                        available_height -= child_height
                        child.style._layout_node(child, alloc_width, child_height, view_dpi)
                        height += child.style.padding_top + child.layout.content_height + child.style.padding_bottom
                    except AttributeError:
                        pass  # Already laid out
                else:
                    if quantum:
                        child_height = quantum * child.style.flex
                    else:
                        child_height = 0

                    self._debug("PASS 2 unspecified height", child_height)
                    available_height -= child_height
                    child.style._layout_node(child, alloc_width, child_height, view_dpi)
                    height += child.style.padding_top + child.layout.content_height + child.style.padding_bottom

                # On this last pass, we can now set the horizontal position, too.
                top_position += child.style.padding_top
                child.layout.content_top = top_position
                top_position += child.layout.content_height + child.style.padding_bottom
        else:
            self._debug("NO CHILDREN", available_height)
            height = available_height

        self._debug("FINAL HEIGHT", height)
        node.layout.content_height = int(height)

        # Establish width, and position children vertically and horizontally.
        if self.width:
            width = self.width
        else:
            available_width = max(0, alloc_width - self.padding_left - self.padding_right)
            if node.children:
                width = max(
                    child.layout.content_width + child.style.padding_left + child.style.padding_right
                    for child in node.children
                )
            else:
                if node.intrinsic.width:
                    self._debug("INTRINSIC WIDTH", node.intrinsic.width)
                    try:
                        width = node.intrinsic.width.final(available_width)
                    except AttributeError:
                        width = node.intrinsic.width
                else:
                    width = available_width

        node.layout.content_width = int(width)

        for child in node.children:
            extra = width - child.layout.content_width + child.style.padding_left + child.style.padding_right
            if self.alignment is RIGHT:
                child.layout.content_left = extra + child.style.padding_left
            elif self.alignment is CENTER:
                child.layout.content_left = int(extra / 2) + child.style.padding_left
            else:
                child.layout.content_left = child.style.padding_left
