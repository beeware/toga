Canvas
======

.. rst-class:: widget-support
.. csv-filter::
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(Divider|Component))'}

.. |y| image:: /_static/yes.png
    :width: 16

The divider is used to visually separate sections of a user layout with a line.

Usage
-----

Simple usage to separate two labels in a column:

.. code-block:: Python

    import toga
    from toga.style import Pack, COLUMN
    divider = toga.Divider()
    label0 = toga.Label("First section")
    label1 = toga.Label("Second section")
    box = toga.Box(
        children=[
            label0,
            divider,
            label1,
            ],
        style=Pack(direction=COLUMN)
    )

The direction (horizontal or vertical) can be given as an argument. If not specified, it
will default to ``Divider.AUTO``. In this case, it will be inferred from the divider's
parent (i.e., horizontal dividers in a column and vertical dividers in a row).

Reference
---------

.. autoclass:: toga.widgets.canvas.Divider
   :members:
   :undoc-members:
   :inherited-members:
