Box
===

.. rst-class:: widget-support
.. csv-filter::
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(Box|Component))'}

.. |y| image:: /_static/yes.png
    :width: 16

The box is a generic container for widgets, allowing you to construct layouts.

Usage
-----

A box can be instantiated with no children and the children added later:

.. code-block:: Python

    import toga

    box = toga.Box('box1')

    button = toga.Button('Hello world', on_press=button_handler)
    box.add(button)

To create boxes within boxes, use the children argument:

.. code-block:: Python

    import toga

    box_a = toga.Box('box_a')
    box_b = toga.Box('box_b)

    box = toga.Box('box', children=[box_a, box_b])

Box Styling
-----------

Styling of boxes can be done during instantiation of the Box:

.. code-block:: Python

    import toga
    from toga.style import Pack
    from toga.style.pack import COLUMN

    box = toga.Box(id='box', style=Pack(direction=COLUMN, padding_top=10))

Styles can be also be updated on an existing instance:

.. code-block:: Python

    import toga
    from toga.style import Pack
    from toga.style.pack import COLUMN

    box = toga.Box(id='box', style=Pack(direction=COLUMN))

    box.style.update(padding_top=10)

Reference
---------

.. autoclass:: toga.widgets.box.Box
   :members:
   :undoc-members:
   :inherited-members:
