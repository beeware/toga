=====================
The Pack Style Engine
=====================

Toga's default style engine, **Pack**, is a layout algorithm based around the idea of
packing boxes inside boxes. Each box specifies a direction for its children, and each
child specifies how it will consume the available space - either as a specific width,
or as a proportion of the available width. Other properties exist to control color,
text alignment and so on.

It is similar in some ways to the CSS Flexbox algorithm; but dramatically simplified, as
there is no allowance for overflowing boxes.


The string values defined here are the string literals that the Pack algorithm accepts.
These values are also pre-defined as Python constants in the ``toga.style.pack`` module
with the same name; however, following Python style, the constants use upper case and
dashes are underscores. For example, the Python constant ``toga.style.pack.SANS_SERIF``
evaluates as the string literal ``"sans-serif"``. (The constant ``NONE``, or
``"none"``, is distinct from Python's ``None``.)


Some properties, despite always storing their value in a consistent form, are more
liberal in what they accept, and will convert as necessary when assigned alternate
forms. Where relevant, these are listed under **Accepts**.

Toga has a :ref:`layout debug mode <debug-layout>` to aid in visually debugging
or exploring Pack layouts.

Pack style properties
~~~~~~~~~~~~~~~~~~~~~

``display``
-----------

**Value:** ``"pack"`` or ``"none"``

**Initial value:** ``"pack"``

Used to define how to display the widget. A value of ``"pack"`` will apply the pack
layout algorithm to this node and its descendants. A value of ``"none"`` removes the
widget from the layout entirely. Space will be allocated for the widget as if it were
there, but the widget itself will not be visible.

``visibility``
--------------

**Value:** ``"hidden"`` or ``"visible"``

**Initial value:** ``"visible"``

Used to define whether the widget should be drawn. A value of ``"visible"`` means the
widget will be displayed. A value of ``"hidden"`` removes the widget from view, but
allocates space for the widget as if it were still in the layout.

Any children of a hidden widget are implicitly removed from view.

If a previously hidden widget is made visible, any children of the widget with a
visibility of ``"hidden"`` will remain hidden. Any descendants of the hidden child will
also remain hidden, regardless of their visibility.

.. _pack-direction:

``direction``
-------------

**Value:** ``"row"`` or ``"column"``

**Initial value:** ``"row"``

The packing direction for children of the box. A value of ``"column"`` indicates
children will be stacked vertically, from top to bottom. A value of ``"row"`` indicates
children will be packed horizontally; left-to-right if ``text_direction`` is ``"ltr"``,
or right-to-left if ``text_direction`` is ``"rtl"``.

``align_items``
---------------

**Value:** ``"start"``, ``"center"``, or ``"end"``

**Initial value:** ``"start"``

**Aliases:** ``vertical_align_items`` in a row, ``horizontal_align_items`` in a column

The alignment of this box's children along the cross axis. A row's cross axis is
vertical, so ``"start"`` aligns children to the top, while ``"end"`` aligns them to the
bottom. For columns, ``"start"`` is on the left if ``text_direction`` is ``"ltr"``, and
the right if ``rtl``.

``justify_content``
-------------------

**Value:** ``"start"``, ``"center"``, or ``"end"``

**Initial value:** ``"start"``

**Aliases:** ``horizontal_align_content`` in a row, ``vertical_align_content`` in a
column

The alignment of this box's children along the main axis. A column's main axis is
vertical, so ``"start"`` aligns children to the top, while ``"end"`` aligns them to the
bottom. For rows, ``"start"`` is on the left if ``text_direction`` is ``"ltr"``, and
the right if ``"rtl"``.

This property only has an effect if there is some free space in the main axis. For
example, if any children have a non-zero ``flex`` value, then they will consume all the
available space, and ``justify_content`` will make no difference to the layout.

``gap``
-------

**Value:** an integer

**Initial value:** ``0``

The amount of space to allocate between adjacent children, in :ref:`CSS pixels
<css-units>`.

``width``
---------

**Value:** an integer or ``"none"``

**Initial value:** ``"none"``

Specify a fixed width for the box, in :ref:`CSS pixels <css-units>`.

The final width for the box may be larger, if the children of the box cannot
fit inside the specified space.

``height``
----------

**Value:** an integer or ``"none"``

**Initial value:** ``"none"``

Specify a fixed height for the box, in :ref:`CSS pixels <css-units>`.

The final height for the box may be larger, if the children of the box cannot
fit inside the specified space.

``flex``
--------

**Value:** a floating-point number

**Initial value:** ``0.0``

A weighting that is used to compare this box with its siblings when
allocating remaining space in a box.

Once fixed space allocations have been performed, this box will assume ``flex
/ (sum of all flex for all siblings)`` of all remaining available space in the
direction of the parent's layout.

``margin_top``
---------------

``margin_right``
-----------------

``margin_bottom``
------------------

``margin_left``
----------------

**Value:** an integer

**Initial value:** ``0``

The amount of space to allocate outside the edge of the box, in :ref:`CSS pixels
<css-units>`.

``margin``
-----------

**Value:** a tuple consisting of ``(margin_top, margin_right, margin_bottom,
margin_left)``

**Initial value:** ``(0, 0, 0, 0)``

**Accepts:** an integer or a sequence of 1–4 integers

A shorthand for setting the top, right, bottom and left margin with a single
declaration.

If 1 integer is provided, that value will be used as the margin for all sides.

If 2 integers are provided, the first value will be used as the margin for the top and
bottom; the second will be used as the value for the left and right.

If 3 integers are provided, the first value will be used as the top margin, the second
for the left and right margin, and the third for the bottom margin.

If 4 integers are provided, they will be used as the top, right, bottom and left margin,
respectively.

``color``
---------

**Value:** a color or ``None``

**Initial value:** ``None``; will use the system default

Set the foreground color for the object being rendered.

Some objects may not use the value.

``background_color``
--------------------

**Value:** a color, ``"transparent"``, or ``None``

**Initial value:** ``None``; will use the system default

Set the background color for the object being rendered.

Some objects may not use the value.

``text_align``
--------------

**Value:** ``"left"``, ``"right"``, ``"center"``, or ``"justify"``

**Initial value:** ``"left"`` if ``text_direction`` is ``"ltr"``; ``"right"`` if
``text_direction`` is ``"rtl"``

Defines the alignment of text in the object being rendered.

``text_direction``
------------------

**Value:** ``"rtl"`` or ``"ltr"``

**Initial value:** ``"rtl"``

Defines the natural direction of horizontal content.

.. _pack-font-family:

``font_family``
---------------

**Value**: a list of strings

**Initial value:** ``["system"]``

**Accepts:** a string or a sequence of strings

A list defining possible font families, in order of preference: the first item that maps
to a valid font will be used. If none can be resolved, the system font will be used.
Setting to a single string value is the same as setting to a list containing that
string as the only item.

A value of ``"system"`` indicates that whatever is a system-appropriate font
should be used.

A value of ``"serif"``, ``"sans-serif"``, ``"cursive"``, ``"fantasy"``, or
``"monospace"`` will use a system-defined font that matches the description (e.g. Times
New Roman for ``"serif"``, Courier New for ``"monospace"``).

Any other value will be checked against the family names previously registered with
:any:`Font.register`.

On supported platforms (currently Windows and Linux), if Toga doesn't recognize the
family as one of its predefined builtins or as a font you've registered, it will
attempt to load the requested font from your system before falling back to the default
system font.

.. _pack-font-style:

``font_style``
----------------

**Value:** ``"normal"``, ``"italic"``, or ``"oblique"``

**Initial value:** ``"normal"``

The style of the font to be used.

**Note:** Windows and Android do not support the oblique font style. A request for an
``"oblique"`` font will be interpreted as ``"italic"``.

.. _pack-font-variant:

``font_variant``
----------------

**Value:** ``"normal"`` or ``"small_caps"``

**Initial value:** ``"normal"``

The variant of the font to be used.

**Note:** Windows and Android do not support the small caps variant. A request for a
``"small_caps"`` font will be interpreted as ``"normal"``.

.. _pack-font-weight:

``font_weight``
---------------

**Value:** ``"normal"`` or ``"bold"``

**Initial value:** ``"normal"``

The weight of the font to be used.

.. _pack-font-size:

``font_size``
-------------

**Value:** an integer

**Initial value:** ``-1``; will use the system default size. This is also stored as a
constant named ``SYSTEM_DEFAULT_FONT_SIZE``.

The size of the font to be used, in :ref:`CSS points <css-units>`.

The relationship between Pack and CSS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pack aims to be a functional subset of CSS. Any Pack layout can be converted
into an equivalent CSS layout. After applying this conversion, the CSS layout
should be considered a "reference implementation". Any disagreement between the
rendering of a converted Pack layout in a browser, and the layout produced by
the Toga implementation of Pack should be considered to be either a bug in Toga,
or a bug in the mapping.

The mapping that can be used to establish the reference implementation is:

* The reference HTML layout document is rendered in `no-quirks mode
  <https://developer.mozilla.org/en-US/docs/Web/HTML/Quirks_Mode_and_Standards_Mode>`__,
  with a default CSS stylesheet:

  .. code-block:: html

      <!DOCTYPE html>
      <html>
         <head>
            <meta charset="UTF-8" />
            <title>Pack layout testbed</title>
            <style>
               html, body {
                  height: 100%;
               }
               body {
                  overflow: hidden;
                  display: flex;
                  margin: 0;
                  white-space: pre;
               }
               div {
                  display: flex;
                  white-space: pre;
               }
            </style>
         </head>
         <body></body>
      </html>

* The root widget of the Pack layout can be mapped to the ``<body>`` element of
  the HTML reference document. The rendering area of the browser window becomes
  the view area that Pack will fill.

* ImageViews map to ``<img>`` elements. The ``<img>`` element has an additional style of
  ``object-fit: contain`` unless *both* ``height`` and ``width`` are defined.

* All other widgets are mapped to ``<div>`` elements.

* The following Pack declarations can be mapped to equivalent CSS declarations:

   ============================= ===================================================
   Pack property                 CSS property
   ============================= ===================================================
   ``direction: <str>``          ``flex-direction: <str>``
   ``display: pack``             ``display: flex``
   ``flex: <int>``               If ``direction == "row"`` and ``width`` is set,
                                 or ``direction == "column"`` and ``height`` is set,
                                 ignore. Otherwise, ``flex: <int> 0 auto``.
   ``font_size: <int>``          ``font-size: <int>pt``
   ``height: <value>``           ``height: <value>px`` if value is an integer;
                                 ``height: auto`` if value is ``"none"``.
   ``margin_top: <int>``         ``margin-top: <int>px``
   ``margin_bottom: <int>``      ``margin-bottom: <int>px``
   ``margin_left: <int>``        ``margin-left: <int>px``
   ``margin_right: <int>``       ``margin-right: <int>px``
   ``text_direction: <str>``     ``direction: <str>``
   ``width: <value>``            ``width: <value>px`` if value is an integer;
                                 ``width: auto`` if value is ``"none"``.
   ============================= ===================================================

* All other Pack declarations should be used as-is as CSS declarations, with
  underscores being converted to dashes (e.g., ``background_color`` becomes
  ``background-color``).
