Canvas
======

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(Canvas|Component))'}

The canvas is used for creating a blank widget that you can draw on.

Usage
-----

Simple usage to draw a black circle on the screen using the arc drawing object:

.. code-block:: python

    import toga
    canvas = toga.Canvas(style=Pack(flex=1))
    box = toga.Box(children=[canvas])
    with canvas.fill() as fill:
        fill.arc(50, 50, 15)

More advanced usage for something like a vector drawing app where you would
want to modify the parameters of the drawing objects. Here we draw a black
circle and black rectangle. We then change the size of the circle, move the
rectangle, and finally delete the rectangle.

.. code-block:: python

    import toga
    canvas = toga.Canvas(style=Pack(flex=1))
    box = toga.Box(children=[canvas])
    with canvas.fill() as fill:
        arc1 = fill.arc(x=50, y=50, radius=15)
        rect1 = fill.rect(x=50, y=50, width=15, height=15)

    arc1.x, arc1.y, arc1.radius = (25, 25, 5)
    rect1.x = 75
    fill.remove(rect1)

Use of drawing contexts, for example with a platformer game. Here you would
want to modify the x/y coordinate of a drawing context that draws each
character on the canvas. First, we create a hero context. Next, we create a
black circle and a black outlined rectangle for the hero's body. Finally, we
move the hero by 10 on the x-axis.

.. code-block:: python

    import toga
    canvas = toga.Canvas(style=Pack(flex=1))
    box = toga.Box(children=[canvas])
    with canvas.context() as hero:
        with hero.fill() as body:
            body.arc(50, 50, 15)
        with hero.stroke() as outline:
            outline.rect(50, 50, 15, 15)

    hero.translate(10, 0)


Reference
---------

Main Interface
^^^^^^^^^^^^^^

.. autoclass:: toga.Canvas
   :members:
   :undoc-members:
   :exclude-members: canvas, add_draw_obj

Lower-Level Classes
^^^^^^^^^^^^^^^^^^^

.. automodule:: toga.widgets.canvas
   :members:
   :undoc-members:
   :exclude-members: Canvas, add_draw_obj
