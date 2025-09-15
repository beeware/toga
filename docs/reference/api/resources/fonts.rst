Font
====

A font for displaying text.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :include: {0: '^Font$'}

Usage
-----

For most widget styling, you do not need to create instances of the :class:`Font` class.
Fonts are applied to widgets using style properties::

   import toga
   from toga.style.pack import pack, SERIF, BOLD

   # Create a bold label in the system's serif font at default system size.
   my_label = toga.Label("Hello World", font_family=SERIF, font_weight=BOLD)

Toga provides a number of :ref:`built-in system fonts <pack-font-family>`. Font sizes
are specified in :ref:`CSS points <css-units>`; the default size depends on the platform
and the widget.

If you want to use a custom font, the font file must be provided as part of your app's
resources, and registered before first use::

   import toga

   # Register the user font with name "Roboto"
   toga.Font.register("Roboto", "resources/Roboto-Regular.ttf")

   # Create a label with the new font.
   my_label = toga.Label("Hello World", font_family="Roboto")

When registering a font, if an invalid value is provided for the style, variant or
weight, ``NORMAL`` will be used.

When a font includes multiple weights, styles or variants, each one must be registered
separately, even if they're stored in the same file::

   import toga
   from toga.style.pack import BOLD

   # Register a regular and bold font, contained in separate font files
   Font.register("Roboto", "resources/Roboto-Regular.ttf")
   Font.register("Roboto", "resources/Roboto-Bold.ttf", weight=BOLD)

   # Register a single font file that contains both a regular and bold weight
   Font.register("Bahnschrift", "resources/Bahnschrift.ttf")
   Font.register("Bahnschrift", "resources/Bahnschrift.ttf", weight=BOLD)

A small number of Toga APIs (e.g., :any:`Context.write_text`) *do* require the use of
:class:`Font` instance. In these cases, you can instantiate a Font using similar
properties to the ones used for widget styling::

   import toga
   from toga.style.pack import BOLD

   # Obtain a 14 point Serif bold font instance
   my_font = toga.Font(SERIF, 14, weight=BOLD)

   # Use the font to write on a canvas.
   canvas = toga.Canvas()
   canvas.context.write_text("Hello", font=my_font)

When constructing your own :class:`Font` instance, ensure that the font family you
provide is valid; otherwise an :any:`UnknownFontError` will be raised.

Notes
-----

* iOS and macOS do not support the use of variant font files (that is, fonts that
  contain the details of multiple weights/variants in a single file). Variant font
  files can be registered; however, only the "normal" variant will be used.

* Android and Windows do not support the oblique font style. If an oblique font is
  specified, Toga will attempt to use an italic style of the same font.

* Android and Windows do not support the small caps font variant. If a Small Caps font
  is specified, Toga will use the normal variant of the same font.

Reference
---------

.. autoclass:: toga.Font
.. autoexception:: toga.fonts.UnknownFontError
