Multi-line text input
=====================

.. rst-class:: widget-support
.. csv-filter::
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(MultilineTextInput|Component)$)'}

.. |y| image:: /_static/yes.png
    :width: 16

The Multi-line text input is similar to the text input but designed for larger inputs, similar to the textarea field of HTML.

Usage
-----

.. code-block:: Python

    import toga

    textbox = toga.MultilineTextInput(id='view1')

Reference
---------

.. autoclass:: toga.widgets.multilinetextinput.MultilineTextInput
   :members:
   :undoc-members:
   :inherited-members:
