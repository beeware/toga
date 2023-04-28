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

.. code-block:: python

    import toga

    input = toga.TextInput(placeholder='enter name here')

Reference
---------

.. autoclass:: toga.widgets.textinput.TextInput
   :members:
   :undoc-members:
