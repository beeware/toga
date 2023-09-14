TextInput
=========

A widget for the display and editing of a single line of text.

.. figure:: /reference/images/TextInput.png
   :align: center
   :width: 300

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!^(TextInput|Component)$)'}

Usage
-----

.. code-block:: python

    import toga

    text_input = toga.TextInput()
    text_input.value = "Jane Developer"

The input can be provided a placeholder value - this is a value that will be
displayed to the user as a prompt for appropriate content for the widget. This
placeholder will only be displayed if the widget has no content; as soon as
a value is provided (either by the user, or programmatically), the placeholder
content will be hidden.

The input can also be provided a list of :ref:`validators <validators>`. A
validator is a function that will be invoked whenever the content of the input
changes. The function should return ``None`` if the current value of the input
is valid; if the current value is invalid, it should return an error message.

Notes
-----

* Although an error message is provided when validation fails, Toga does not
  guarantee that this error message will be displayed to the user.

* Winforms does not support the use of partially or fully transparent colors for
  the TextInput background. If a color with an alpha value is provided
  (including ``TRANSPARENT``), the alpha channel will be ignored. A
  ``TRANSPARENT`` background will be rendered as white.

* On Winforms, if a TextInput is given an explicit height, the rendered widget
  will not expand to fill that space. The widget will have the fixed height
  determined by the font used on the widget. In general, you should avoid
  setting a ``height`` style property on TextInput widgets.

Reference
---------

.. autoclass:: toga.TextInput
