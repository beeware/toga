Text Input
==========

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(TextInput|Component)$)'}

The text input widget is a simple input field for user entry of text data.

.. figure:: /reference/images/TextInput.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga

    input = toga.TextInput(placeholder='enter name here')

Reference
---------

.. autoclass:: toga.widgets.textinput.TextInput
   :members:
   :undoc-members:

Valid Pack style properties
----------------------------

``font_family``: The font family to use for the text input.

``font_size``: The font size to use for the text input.

``color``: The color of the text in the input box.

``background_color``: The background color of the input box.

``border_color``: The color of the input box border.

``border_width``: The width of the input box border.

``border_radius``: The radius of the input box corners.

``padding``: The padding within the input box.

``margin``: The margin around the input box.
