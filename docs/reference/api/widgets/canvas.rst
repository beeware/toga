Canvas
======

======= ====== ========= ===== ========= ========
 macOS   GTK+   Windows   iOS   Android   Django
======= ====== ========= ===== ========= ========
         |y|
======= ====== ========= ===== ========= ========

.. |y| image:: /_static/yes.png
    :width: 16

The canvas is used for creating a blank widget that you can draw on.

Usage
-----

Simple usage to draw an image on the screen:

.. code-block:: Python

    import toga
    canvas = toga.Canvas(style=Pack(flex=1))
    box = toga.Box(children=[canvas])
    with canvas.fill() as fill:
        fill.arc(50, 50, 15)

More advanced usage for something like a vector drawing app where you would want
to modify the parameters of the drawing objects:

.. code-block:: Python

    import toga
    canvas = toga.Canvas(style=Pack(flex=1))
    box = toga.Box(children=[canvas])
    with canvas.fill() as fill:
        arc1 = fill.arc(50, 50, 15)
        rect1 = fill.rect(50, 50, 15, 15)

    arc1.modify(25, 25, 5)
    rect1.x = 75
    fill.remove(rect1)

Use of drawing contexts, for example with a platformer game. Here you would want
to modify the x/y coordinate of a drawing context that draws each character on
the canvas:

.. code-block:: Python

    import toga
    canvas = toga.Canvas(style=Pack(flex=1))
    box = toga.Box(children=[canvas])
    with canvas.context() as hero:
        with hero.fill():
            hero.arc(50, 50, 15)
        with hero.stroke():
            hero.rect(50, 50, 15, 15)

    hero.translate(10, 0)


Reference
---------

Main Interface
^^^^^^^^^^^^^^

.. autoclass:: toga.widgets.canvas.Canvas
   :members:
   :undoc-members:
   :inherited-members:

Lower-Level Classes
^^^^^^^^^^^^^^^^^^^

.. autoclass:: toga.widgets.canvas.Context
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.Fill
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.Stroke
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.ClosedPath
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.MoveTo
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.LineTo
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.BezierCurveTo
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.QuadraticCurveTo
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.Ellipse
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.Arc
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.Arc
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.Rect
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.Rotate
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.Scale
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.Translate
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.WriteText
   :members:
   :inherited-members:

.. autoclass:: toga.widgets.canvas.NewPath
   :members:
   :inherited-members:

