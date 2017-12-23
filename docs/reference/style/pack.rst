=====================
The Pack Style Engine
=====================

Toga's default style engine, **Pack**, is a layout algorithm based around the
idea of packing boxes inside boxes. Each box specifies a direction for it's
children, and each child specifies how it will consume the available space -
either as a specific width, or as a proportion of the available width. Other
properties exist to control color, text alignment and so on.

It is simliar in some ways to the CSS Flexbox algorithm; but dramatically
simplified, as there is no allowance for overflowing boxes.

Pack style properties
~~~~~~~~~~~~~~~~~~~~~

``display``
-----------

**Values:** ``pack`` | ``none``

**Initial value:** ``pack``

Used to define the how to display the element. A value of ``pack`` will apply
the pack layout algorithm to this node and it's descendents. A value of
``none`` removes the element from the layout entirely. Space will be allocated
for the element as if it were there, but the element itself will not be
visible.

``visibility``
--------------

**Values:** ``visible`` | ``none``

**Initial value:** ``visible``

Used to define whether the element should be drawn. A value of ``visible``
means the element will be displayed. A value of ``none`` removes the element,
but still allocates space for the element as if it were in the element tree.

``direction``
-------------

**Values:** ``row`` | ``column``

**Initial value:** ``row``

The packing direction for children of the box. A value of ``column`` indicates
children will be stacked vertically, from top to bottom. A value of ``row``
indicates children will be packed horizontally; left-to-right if
``text_direction`` is ``ltr``, or right-to-left if ``text_direction`` is ``rtl``.

``alignment``
-------------

**Values:** ``top`` | ``bottom`` | ``left`` | ``right`` | ``center``

**Initial value:** ``top`` if direction is ``row``; ``left`` if direction is ``column``

The alignment of children relative to the outside of the packed box.

If the box is a ``column`` box, only the values ``left``, ``right`` and
``center`` are honored.

If the box is a ``row`` box, only the values ``top``, ``bottom and ``center``
are honored.

If a value value is provided, but the value isn't honored, the alignment
reverts to the default for the direction.


``width``
---------

**Values:** ``<integer>`` | ``none``

**Initial value:** ``none``

Specify a fixed width for the box.

The final width for the box may be larger, if the children of the box cannot
fit inside the specified space.

``height``
----------

**Values:** ``<integer>`` | ``none``

**Initial value:** ``none``

Specify a fixed height for the box.

The final height for the box may be larger, if the children of the box cannot
fit inside the specified space.

``flex``
--------

**Values:** ``<number>``

**Initial value:** 0

A weighting that is used to compare this box with it's siblings when
allocating remaining space in a box.

Once fixed space allocations have been performed, this box will assume ``flex
/ (sum of all flex for all siblings)`` of all remaining available space in the
direction of the parent's layout.

``padding_top``
---------------

``padding_right``
-----------------

``padding_bottom``
------------------

``padding_left``
----------------

**Values:** ``<integer>``

**Initial value:** ``0``

The amount of space to allocate between the edge of the box, and the edge of content in the box, on the top, right, bottom and left sides, respectively.

``padding``
-----------

**Values:** ``<integer>`` {1,4}

A shorthand for setting the top, right, bottom and left padding with a single declaration.

If 1 integer is provided, that value will be used as the padding for all sides.

If 2 integers are provided, the first value will be used as the padding for the top and bottom; the second will be used as the value for the left and right.

If 3 integers are provided, the first value will be used as the top padding, the second for the left and right padding, and the third for the bottom padding.

If 4 integers are provided, they will be used as the top, right, bottom and left padding, respectively.

``color``
---------

**Values:** ``<color>``

**Initial value:** System default

Set the foreground color for the object being rendered.

Some objects may not use the value.

``background_color``
--------------------

**Values:** ``<color>`` | ``transparent``

**Initial value:** The platform default background color

Set the background color for the object being rendered.

Some objects may not use the value.

``text_align``
--------------

**Values:** ``left`` | ``right`` | ``center`` | ``justify``

**Initial value:** ``left`` if ``text_direction`` is ``ltr``; ``right`` if ``text_direction`` is ``rtl``

Defines the alignment of text in the object being rendered.

``text_direction``
------------------

**Values:** ``rtl`` | ``ltr``

**Initial value:** ``rtl``

Defines the natural direction of horizontal content.

``font_family``
---------------

**Values:** ``system`` | ``serif``| ``sans-serif`` | ``cursive`` | ``fantasy`` | ``monospace`` | ``<string>``

**Initial value:** ``system``

The font family to be used.

A value of ``system`` indicates that whatever is a system-appropriate font
should be used.

A value of ``serif``, ``sans-serif``, ``cursive``, ``fantasy``, or ``monospace`` will use a system defined font that matches the description (e.g.,"Times New Roman" for ``serif``, "Courier New" for ``monospace``).

Otherwise, any font name can be specified. If the font name cannot be resolved, the system font will be used.

``font_variant``
----------------

**Values:** ``normal`` | ``small_caps``

**Initial value:** ``normal``

The variant of the font to be used.

``font_weight``
---------------

**Values:** ``normal`` | ``bold``

**Initial value:** ``normal``

The weight of the font to be used.

``font_size``
-------------

**Values:** ``<integer>``

**Initial value:** System default

``font``
--------

A shorthand value


The Pack algorithm
~~~~~~~~~~~~~~~~~~

The pack algorithm is applied to the root of a layout tree, with a box
specifying the allocated width and allocated height.

1. **Establish the available width**

   If the element has a ``width`` specified, the available width is set to
   that width.

   Otherwise, the adjusted view width is set to the view width, less the
   amount of ``padding_left`` and ``padding_right``. If this results in a
   value less than 0, the adjusted view width is set to 0.

   If the element has a fixed intrinsic width, the available width is set to
   the minimum of the adjusted view width and the intrinsic width.

   If the element has a minimum intrinsic width, the available width is fixed
   to the maximum of the adjusted view width and the intrinsic minimum width.

   If the element does not have an intrinsic width, the available width is set
   to the adjusted view width.

2. **Establish the available height**

   If the element has a ``height`` specified, the available height is set to
   that height.

   Otherwise, the adjusted view height is set to the view height, less the
   amount of ``padding_top`` and ``padding_bottom``. If this results in a
   value less than 0, the adjusted view height is set to 0.

   If the element has a fixed intrinsic height, the available height is set to
   the minimum of the adjusted view height and the intrinsic height.

   If the element has a minimum intrinsic height, the available height is
   fixed to the maximum of the adjusted view height and the intrinsic minimum
   height.

   If the element does not have an intrinsic height, the available height is
   set to the adjusted view height.

3. **Layout children**

   If the element has no children, the final width of the element is set to
   the available width, and the final height of the element is set to the
   available height.

   Otherwise, the element is a parent element, the final width is set to 0,
   and the children are laid out.

   If the parent element has a ``display`` value of ``row``, it is a **row
   box**, and child layout occurs as follows:

   1. **Allocated fixed width elements**

      This step is performed on every child, in definition order.

      If the child has:

      * an explicitly specified ``width``; or
      * a fixed intrinsic width; or
      * a ``flex`` value of 0

      then the child is then laid out using a recursive call to this
      algorithm, using the current available width and available height.

      The child's full width is then evaluated as the content width allocated
      by the recursive layout call, plus the ``padding_left`` and
      ``padding_right`` of the child. The final width of the parent element
      is increased by the child's full width; the available width of the
      parent element is decreased by the child's full width.

   2. **Evaluate flex quantum value**

      The flex total is set to the sum of the ``flex`` value for every element
      that *wasnt'* laid out in substep 1.

      If the available width is less than 0, or the flex total is 0, the flex
      quantum is set to 0. Otherwise, the flex quantum is set to the available
      width divided by the flex total.

   3. **Evaluate the flexible width elements**

      This step is performed on every child, in definition order.

      If the child was laid out in step 1, no layout is required, and this
      step can be skipped.

      Otherwise, the child's flex allocation is the product of the flex quantum
      and the child's ``flex`` value.

      If the child has a minimum intrinsic width, the child's allocated width
      is set to the maximum of the flex allocation and the minimum intrinsic width.

      Otherwise, the child's allocated width is set to the flex allocation.

      The child is then laid out using a recursive call to this algorithm,
      using the child's allocated width and the available height.

      The child's full width is then evaluated as the content width allocated by
      the recursive layout call, plus the ``padding_left`` and
      ``padding_right`` of the child. The overall width of the parent element
      is increased by the child's full width.

   4. **Evaluate row height, and set the horizontal position of each element**.

      The current horizontal offset is set to 0, and then this step is
      performed on every child, in definition order.

      If the ``text_direction`` of parent element is ``ltr``, the left
      position of the child element is set to the current horizontal offset
      plus the child's ``padding_left``. The current horizontal offset is then
      increased by the child's content width plus the child's ``padding_right``.

      If the ``text_direction`` of the parent element is ``rtl``, the right
      position of the child element is set to the parent's final width, less
      the offset, less the child's ``padding_right``. The current horizontal
      offset is then increased by the child's content width plus the
      child's ``padding_left``.

   5. **Set the vertical position of each child inside the row**

      This step is performed on every child, in definition order.

      The extra height for a child is defined as the difference between the
      parent elements final height and the child's full height.

      If the parent element has a ``alignment`` value of ``top``, the
      vertical position of the child is set to 0, relative to the parent.

      If the parent element has a ``alignment`` value of ``bottom``, the
      vertical position of the child is set to the extra height, relative to
      the parent.

      If the parent element has a ``alignment`` value of ``center``, the
      vertical position of the child is set to 1/2 of the extra height,
      relative to the parent.

   If the parent element has a ``display`` value of ``column``, it is a
   **column box**, and child layout occurs as follows:

   1. **Allocated fixed height elements**

      This step is performed on every child, in definition order.

      If the child has:

      * an explicitly specified ``height``; or
      * a fixed intrinsic height; or
      * a ``flex`` value of 0

      then the child is then laid out using a recursive call to this
      algorithm, using the current available width and available height.

      The child's full height is then evaluated as the content height allocated
      by the recursive layout call, plus the ``padding_top`` and
      ``padding_bottom`` of the child. The final height of the parent element
      is increased by the child's full height; the available height of the
      parent element is decreased by the child's full height.

   2. **Evaluate flex quantum value**

      The flex total is set to the sum of the ``flex`` value for every element
      that *wasn't* laid out in substep 1.

      If the available height is less than 0, or the flex total is 0, the flex
      quantum is set to 0. Otherwise, the flex quantum is set to the available
      height divided by the flex total.

   3. **Evaluate the flexible height elements**

      This step is performed on every child, in definition order.

      If the child was laid out in step 1, no layout is required, and this
      step can be skipped.

      Otherwise, the child's flex allocation is the product of the flex quantum
      and the child's ``flex`` value.

      If the child has a minimum intrinsic height, the child's allocated height
      is set to the maximum of the flex allocation and the minimum intrinsic height.

      Otherwise, the child's allocated height is set to the flex allocation.

      The child is then laid out using a recursive call to this algorithm,
      using the child's allocated height and the available width.

      The child's full height is then evaluated as the content height allocated by
      the recursive layout call, plus the ``padding_top`` and
      ``padding_bottom`` of the child. The overall height of the parent element
      is increased by the child's full height.

   4. **Evaluate column width, and set the vertical position of each element**.

      The current vertical offset is set to 0, and then this step is
      performed on every child, in definition order.

      The top position of the child element is set to the current vertical
      offset plus the child's ``padding_top``. The current vertical offset is
      then increased by the child's content height plus the child's
      ``padding_bottom``.

   5. **Set the horizontal position of each child inside the column**

      This step is performed on every child, in definition order.

      The extra width for a child is defined as the difference between the
      parent element's final width and the child's full width.

      If the parent element has a ``alignment`` value of ``left``, the
      horizontal position of the child is set to 0, relative to the parent.

      If the parent element has a ``alignment`` value of ``right``, the
      horizontal position of the child is set to the extra width, relative to
      the parent.

      If the parent element has a ``text_align`` value of ``center``, the
      horizontal position of the child is set to 1/2 of the extra width,
      relative to the parent.
