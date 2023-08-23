PasswordInput
=============

A widget to allow the entry of a password. Any value typed by the user will be
obscured, allowing the user to see the number of characters they have typed, but
not the actual characters.

.. figure:: /reference/images/PasswordInput.png
   :align: center
   :width: 300

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!^(PasswordInput|Component)$)'}


Usage
-----

The ``PasswordInput`` is functionally identical to a :class:`~toga.TextInput`, except
for how the text is displayed. All features supported by :class:`~toga.TextInput` are
also supported by PasswordInput.

.. code-block:: python

    import toga

    password = toga.PasswordInput()

Notes
-----

* Winforms does not support the use of partially or fully transparent colors for
  the PasswordInput background. If a color with an alpha value is provided
  (including ``TRANSPARENT``), the alpha channel will be ignored. A
  ``TRANSPARENT`` background will be rendered as white.

* On Winforms, if a PasswordInput is given an explicit height, the rendered
  widget will not expand to fill that space. The widget will have the fixed
  height determined by the font used on the widget. In general, you should avoid
  setting a ``height`` style property on PasswordInput widgets.

Reference
---------

.. autoclass:: toga.PasswordInput
