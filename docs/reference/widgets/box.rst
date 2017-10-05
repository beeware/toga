:orphan:

.. warnings about this file not being included in any toctree will be suppressed by :orphan:

Box
===

The box is a generic container for any widgets, boxes leverage the layout model from the BeeWare Colosseum_ package.

Usage
-----

A box can be instantiated with no children and then the children added later

.. code-block:: Python

    import toga

    box = toga.Box('box1')

    button = toga.Button('Hello world', on_press=button_handler)
    box.add(button)

To create boxes within boxes, use the children argument.

.. code-block:: Python

    import toga

    box_a = toga.Box('box_a')
    box_b = toga.Box('box_b)

    box = toga.Box('box', children=[box_a, box_b])

Box Styling
-----------

Styling of boxes through colosseum can be done pre instantiation or post,

.. code-block:: Python

    import toga

    box = toga.Box('box1')

    box.style.set(flex_direction='column', padding_top=10)

.. code-block:: Python

    import toga
    from colosseum import CSS

    style = CSS(padding_top=10)
    box = toga.Box('box', style=style)

Supported Platforms
-------------------

.. include:: ../supported_platforms/Box.rst

Reference
---------

.. autoclass:: toga.widgets.box.Box
   :members:
   :undoc-members:
   :inherited-members:

.. _Colosseum: http://pybee.org/project/projects/libraries/colosseum/