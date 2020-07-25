Divider
=======

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

    box = toga.Box(
        children=[
            toga.Label("First section"),
            toga.Divider(),
            toga.Label("Second section"),
        ],
        style=Pack(direction=COLUMN, flex=1, padding=10)
    )

The direction (horizontal or vertical) can be given as an argument. If not specified, it
will default to horizontal.

Reference
---------

.. autoclass:: toga.widgets.divider.Divider
   :members:
   :undoc-members:
   :inherited-members:
