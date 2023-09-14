Divider
=======

A separator used to visually distinguish two sections of content in a layout.

.. figure:: /reference/images/Divider.jpeg
    :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(Divider|Component))'}

Usage
-----

To separate two labels stacked vertically with a horizontal line:

.. code-block:: python

    import toga
    from toga.style.pack import Pack, COLUMN

    box = toga.Box(
        children=[
            toga.Label("First section"),
            toga.Divider(),
            toga.Label("Second section"),
        ],
        style=Pack(direction=COLUMN, flex=1, padding=10)
    )

The direction (horizontal or vertical) can be given as an argument. If not
specified, it will default to horizontal.

Reference
---------

.. autoclass:: toga.Divider
