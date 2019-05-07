from travertino.constants import (
    NORMAL, SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE, ITALIC, OBLIQUE, SMALL_CAPS, BOLD,
    LEFT, RIGHT, TOP, BOTTOM, CENTER, JUSTIFY, RTL, LTR, TRANSPARENT, SYSTEM
)
from travertino.declaration import BaseStyle, Choices
from travertino.layout import BaseBox
from travertino.size import BaseIntrinsicSize

from toga.fonts import Font


######################################################################
# Display
######################################################################

PACK = 'pack'

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


DISPLAY_CHOICES = Choices(PACK, NONE)
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

FONT_FAMILY_CHOICES = Choices(SYSTEM, SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE, string=True)
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

    def _debug(self, *args):
        print('    ' * self.__class__._depth, *args)

    def apply(self, prop, value):
        if self._applicator:
            if prop == 'text_align':
                if value is None:
                    if self.text_direction is RTL:
                        value = RIGHT
                    else:
                        value = LEFT
                self._applicator.set_text_alignment(value)
            elif prop == 'color':
                self._applicator.set_color(value)
            elif prop == 'background_color':
                self._applicator.set_background_color(value)
            elif prop == 'visibility':
                hidden = False
                if value == HIDDEN:
                    hidden = True
                self._applicator.set_hidden(hidden)
            elif prop in ('font_family', 'font_size', 'font_style', 'font_variant', 'font_weight'):
                self._applicator.set_font(
                    Font(
                        self.font_family,
                        self.font_size,
                        style=self.font_style,
                        variant=self.font_variant,
                        weight=self.font_weight
                    )
                )

    def layout(self, node, viewport):
        self._layout_node(node, viewport.width, viewport.height, viewport.dpi)
        node.layout.content_top = node.style.padding_top
        node.layout.content_bottom = node.style.padding_bottom

        node.layout.content_left = node.style.padding_left
        node.layout.content_right = node.style.padding_right

    def _layout_node(self, node, alloc_width, alloc_height, view_dpi):
        self.__class__._depth += 1
        # self._debug("COMPUTE LAYOUT for", node, "available", alloc_width, alloc_height)

        # Establish available width
        if self.width:
            # If width is specified, use it
            available_width = self.width
            # self._debug("SPECIFIED WIDTH", available_width)
        else:
            # If no width is specified, assume we're going to use all
            # the available width. If there is an intrinsic width,
            # use it to make sure the width is at least the amount specified.
            available_width = max(0, alloc_width - self.padding_left - self.padding_right)
            # self._debug("INITIAL AVAILABLE WIDTH", available_width)
            if node.intrinsic.width:
                # self._debug("INTRINSIC WIDTH", node.intrinsic.width)
                try:
                    available_width = max(available_width, node.intrinsic.width.value)
                except AttributeError:
                    available_width = min(available_width, node.intrinsic.width)

                # self._debug("ADJUSTED WIDTH", available_width)
            else:
                # self._debug("USE ALL AVAILABLE WIDTH", available_width)
                pass

        # Establish available height
        if self.height:
            # If height is specified, use it.
            available_height = self.height
            # self._debug("SPECIFIED HEIGHT", available_height)
        else:
            available_height = max(0, alloc_height - self.padding_top - self.padding_bottom)
            # self._debug("INITIAL AVAILABLE HEIGHT", available_height)
            if node.intrinsic.height:
                # self._debug("INTRINSIC HEIGHT", node.intrinsic.height)
                try:
                    available_height = max(available_height, node.intrinsic.height.value)
                except AttributeError:
                    available_height = node.intrinsic.height

                # self._debug("ADJUSTED HEIGHT", available_height)
            else:
                # self._debug("USE ALL AVAILABLE HEIGHT", available_height)
                pass

        if node.children:
            if self.direction == COLUMN:
                width, height = self._layout_column_children(node, available_width, available_height, view_dpi)
            else:
                width, height = self._layout_row_children(node, available_width, available_height, view_dpi)

        else:
            # self._debug("NO CHILDREN", available_width)
            width = available_width
            height = available_height

        # self._debug("FINAL SIZE", width, height)
        node.layout.content_width = int(width)
        node.layout.content_height = int(height)

        # self._debug("END LAYOUT", node, node.layout)
        self.__class__._depth -= 1

    def _layout_row_children(self, node, available_width, available_height, view_dpi):
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
                child.style._layout_node(child, available_width, available_height, view_dpi)
                child_width = child.style.padding_left + child.layout.content_width + child.style.padding_right
                width += child_width
                available_width -= child_width
            elif child.intrinsic.width:
                if hasattr(child.intrinsic.width, 'value'):
                    if child.style.flex:
                        full_flex += child.style.flex
                        # self._debug("PASS 1 intrinsic flex width", child.intrinsic.width)
                    else:
                        # self._debug("PASS 1 intrinsic non-flex width", child.intrinsic.width)
                        child.style._layout_node(child, 0, available_height, view_dpi)
                        child_width = child.style.padding_left + child.layout.content_width + child.style.padding_right
                        width += child_width
                        available_width -= child_width
                else:
                    # self._debug("PASS 1 intrinsic width", child.intrinsic.width)
                    child.style._layout_node(child, available_width, available_height, view_dpi)
                    child_width = child.style.padding_left + child.layout.content_width + child.style.padding_right
                    width += child_width
                    available_width -= child_width
            else:
                if child.style.flex:
                    # self._debug("PASS 1 unspecified flex width")
                    full_flex += child.style.flex
                else:
                    # self._debug("PASS 1 unspecified non-flex width")
                    child.style._layout_node(child, available_width, available_height, view_dpi)
                    child_width = child.style.padding_left + child.layout.content_width + child.style.padding_right
                    width += child_width
                    available_width -= child_width

        available_width = max(0, available_width)
        if full_flex:
            # self._debug("q =",available_width, full_flex, available_width / full_flex)
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
                        child_alloc_width = max(quantum * child.style.flex, child.intrinsic.width.value)
                        # self._debug("PASS 2 intrinsic flex width", child_alloc_width)

                        child.style._layout_node(child, child_alloc_width, available_height, view_dpi)
                        width += child.style.padding_left + child.layout.content_width + child.style.padding_right
                    except AttributeError:
                        pass  # Already laid out
                else:
                    if quantum:
                        child_width = quantum * child.style.flex
                    else:
                        child_width = 0

                    # self._debug("PASS 2 unspecified flex width", child_width)
                    available_width -= child_width
                    child.style._layout_node(child, child_width, available_height, view_dpi)
                    width += child.style.padding_left + child.layout.content_width + child.style.padding_right

        # self._debug("USED WIDTH", width)

        # Pass 3: Set the horizontal position of each child, and establish row height
        offset = 0
        if node.style.text_direction is RTL:
            for child in node.children:
                # self._debug("START CHILD AT RTL HORIZONTAL OFFSET", child, offset)
                offset += child.layout.content_width + child.style.padding_right
                child.layout.content_left = width - offset
                offset += child.style.padding_left
                child_height = child.layout.content_height + child.style.padding_top + child.style.padding_bottom
                height = max(height, child_height)
        else:
            for child in node.children:
                # self._debug("START CHILD AT LTR HORIZONTAL OFFSET", child, offset)
                offset += child.style.padding_left
                child.layout.content_left = offset
                offset += child.layout.content_width + child.style.padding_right
                child_height = child.layout.content_height + child.style.padding_top + child.style.padding_bottom
                height = max(height, child_height)

        # Pass 4: set vertical position of each child.
        for child in node.children:
            extra = height - child.layout.content_height + child.style.padding_top + child.style.padding_bottom
            # self._debug("row extra height", extra)
            if self.alignment is BOTTOM:
                child.layout.content_top = extra + child.style.padding_top
                # self._debug("align to bottom", child, child.layout.content_top)
            elif self.alignment is CENTER:
                child.layout.content_top = int(extra / 2) + child.style.padding_top
                # self._debug("align to center", child, child.layout.content_top)
            else:
                child.layout.content_top = child.style.padding_top
                # self._debug("align to top", child, child.layout.content_top)

        return width, height

    def _layout_column_children(self, node, available_width, available_height, view_dpi):
        # self._debug("LAYOUT COLUMN CHILDREN", available_height)
        # Pass 1: Lay out all children with a hard-specified height, or an
        # intrinsic non-flexible height. While iterating, collect the flex
        # total of remaining elements.
        full_flex = 0
        height = 0
        for child in node.children:
            if child.style.height:
                # self._debug("PASS 1 fixed height", child.style.height)
                child.style._layout_node(child, available_width, available_height, view_dpi)
                child_height = child.style.padding_top + child.layout.content_height + child.style.padding_bottom
                height += child_height
                available_height -= child_height
            elif child.intrinsic.height:
                if hasattr(child.intrinsic.height, 'value'):
                    if child.style.flex:
                        full_flex += child.style.flex
                        # self._debug("PASS 1 intrinsic flex height", child.intrinsic.height)
                    else:
                        # self._debug("PASS 1 intrinsic non-flex height", child.intrinsic.height)
                        child.style._layout_node(child, available_width, 0, view_dpi)
                        child_height = child.style.padding_top + child.layout.content_height + child.style.padding_bottom
                        height += child_height
                        available_height -= child_height
                else:
                    # self._debug("PASS 1 intrinsic height", child.intrinsic.height)
                    child.style._layout_node(child, available_width, available_height, view_dpi)
                    child_height = child.style.padding_top + child.layout.content_height + child.style.padding_bottom
                    height += child_height
                    available_height -= child_height
            else:
                if child.style.flex:
                    # self._debug("PASS 1 unspecified flex height")
                    full_flex += child.style.flex
                else:
                    # self._debug("PASS 1 unspecified non-flex height")
                    child.style._layout_node(child, available_width, available_height, view_dpi)
                    child_height = child.style.padding_top + child.layout.content_height + child.style.padding_bottom
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
                        child_alloc_height = max(quantum * child.style.flex, child.intrinsic.height.value)
                        # self._debug("PASS 2 intrinsic height", child_alloc_height)

                        child.style._layout_node(child, available_width, child_alloc_height, view_dpi)
                        height += child.style.padding_top + child.layout.content_height + child.style.padding_bottom
                    except AttributeError:
                        pass  # Already laid out
                else:
                    if quantum:
                        child_height = quantum * child.style.flex
                    else:
                        child_height = 0

                    # self._debug("PASS 2 unspecified height", child_height)
                    available_height -= child_height
                    child.style._layout_node(child, available_width, child_height, view_dpi)
                    height += child.style.padding_top + child.layout.content_height + child.style.padding_bottom

        # self._debug("USED HEIGHT", height)

        # Pass 3: Set the vertical position of each element, and establish column width
        offset = 0
        width = 0
        for child in node.children:
            # self._debug("START CHILD AT VERTICAL OFFSET", offset)
            offset += child.style.padding_top
            child.layout.content_top = offset
            offset += child.layout.content_height + child.style.padding_bottom
            child_width = child.layout.content_width + child.style.padding_left + child.style.padding_right
            width = max(width, child_width)

        # Pass 4: set horizontal position of each child.
        for child in node.children:
            extra = width - child.layout.content_width + child.style.padding_left + child.style.padding_right
            # self._debug("row extra width", extra)
            if self.alignment is LEFT:
                child.layout.content_left = extra + child.style.padding_left
                # self._debug("align to right", child, child.layout.content_left)
            elif self.alignment is CENTER:
                child.layout.content_left = int(extra / 2) + child.style.padding_left
                # self._debug("align to center", child, child.layout.content_left)
            else:
                child.layout.content_left = child.style.padding_left
                # self._debug("align to left", child, child.layout.content_left)

        return width, height


Pack.validated_property('display', choices=DISPLAY_CHOICES, initial=PACK)
Pack.validated_property('visibility', choices=VISIBILITY_CHOICES, initial=VISIBLE)
Pack.validated_property('direction', choices=DIRECTION_CHOICES, initial=ROW)
Pack.validated_property('alignment', choices=ALIGNMENT_CHOICES)

Pack.validated_property('width', choices=SIZE_CHOICES, initial=0)
Pack.validated_property('height', choices=SIZE_CHOICES, initial=0)
Pack.validated_property('flex', choices=FLEX_CHOICES, initial=0)

Pack.validated_property('padding_top', choices=PADDING_CHOICES, initial=0)
Pack.validated_property('padding_right', choices=PADDING_CHOICES, initial=0)
Pack.validated_property('padding_bottom', choices=PADDING_CHOICES, initial=0)
Pack.validated_property('padding_left', choices=PADDING_CHOICES, initial=0)
Pack.directional_property('padding%s')

Pack.validated_property('color', choices=COLOR_CHOICES)
Pack.validated_property('background_color', choices=BACKGROUND_COLOR_CHOICES)

Pack.validated_property('text_align', choices=TEXT_ALIGN_CHOICES)
Pack.validated_property('text_direction', choices=TEXT_DIRECTION_CHOICES, initial=LTR)

Pack.validated_property('font_family', choices=FONT_FAMILY_CHOICES, initial=SYSTEM)
# Pack.list_property('font_family', choices=FONT_FAMILY_CHOICES)
Pack.validated_property('font_style', choices=FONT_STYLE_CHOICES, initial=NORMAL)
Pack.validated_property('font_variant', choices=FONT_VARIANT_CHOICES, initial=NORMAL)
Pack.validated_property('font_weight', choices=FONT_WEIGHT_CHOICES, initial=NORMAL)
Pack.validated_property('font_size', choices=FONT_SIZE_CHOICES, initial=12)
# Pack.composite_property([
#     'font_family', 'font_style', 'font_variant', 'font_weight', 'font_size'
#     FONT_CHOICES
# ])
