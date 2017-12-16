=====================
The Flow Style Engine
=====================

Toga's default style engine, **Flow**, is a layout algorithm based around the
idea of stacking boxes inside boxes. Each box specifies a direction for it's
children, and each child specifies how it will consume the available space -
either as a specific width, or as a proportion of the available width. Other
properties exist to control color, text alignment and so on.

It is simliar to the CSS Flexbox algorithm; but dramatically simplified, as
there is no allowance for overflowing boxes.

Flow style properties
~~~~~~~~~~~~~~~~~~~~~

``display``
-----------

**Values:** ``flow`` | ``none``

**Initial value:** ``flow``

Used to define the how to display the element. A value of ``flow`` will apply the flow layout algorithm to this node and it's descendents. A value of ``none`` removes the element from the layout entirely. Space will be allocated for the element as if it were there, but the element itself will not be visible.

``visibility``
--------------

**Values:** ``visible`` | ``none``

**Initial value:** ``visible``

Used to define whether the element should be drawn. A value of ``visible`` means the element will be displayed. A value of ``none`` removes the element, but still allocates space for the element as if it were in the element tree.

``direction``
-------------

**Values:** ``row`` | ``column``

**Initial value:** ``row``

``alignment``
-------------

**Values:** ``top`` | ``bottom`` | ``left`` | ``right`` | ``center``

**Initial value:** ``top`` if direction is ``row``; ``left`` if direction is ``column``

``width``
---------

**Values:** ``<integer>`` | ``none``

**Initial value:** ``none``

``height``
----------

**Values:** ``<integer>`` | ``none``

**Initial value:** ``none``

``flex``
--------

**Values:** ``<number>``

**Initial value:** 0

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

``padding``
-----------

**Values:** ``` | ````

**Initial value:** see

``color``
---------

**Values:** ``<color>``

**Initial value:** ``black``

    color = validated_property('color', choices=COLOR_CHOICES)

``background_color``
--------------------

**Values:** ``<color>`` | ``transparent``

**Initial value:** The platform default background color

``text_align``
--------------

**Values:** ``left`` | ``right`` | ``center`` | ``justify``

**Initial value:** ``left`` if ``text_direction`` is ``ltr``; ``right`` if ``text_direction`` is ``rtl``

``text_direction``
------------------

**Values:** ``rtl`` | ``ltr``

**Initial value:** ``rtl``

The Flow algorithm
~~~~~~~~~~~~~~~~~~

The flow algorithm is applied to the root of a layout tree, with a box
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
