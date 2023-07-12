Canvas
======

A drawing area for 2D vector graphics.

.. figure:: /reference/images/Canvas.png
    :align: center
    :width: 300

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(Canvas|Component))'}

Usage
-----

Canvas is a 2D vector graphics drawing area, whose API broadly follows the `HTML5 Canvas
API <https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API>`__. The Canvas
provides a drawing Context; drawing instructions are then added to that context by
calling methods on the context.

For example, the following code will draw an orange horizontal line:

.. code-block:: python

    import toga
    canvas = toga.Canvas()

    canvas.context.begin_path()
    canvas.context.move_to(20, 20)
    canvas.context.line_to(160, 20)
    canvas.context.stroke(color="orange")

Toga adds an additional layer of convenience to the base HTML5 API by providing context
managers for operations that have a natural open/close life cycle. For example, the
previous drawing example could be replace with:

.. code-block:: python

    import toga
    canvas = toga.Canvas()

    with canvas.context.Stroke(20, 20, color="orange") as stroke:
        stroke.line_to(160, 20)

Any argument provided to a primitive drawing objects or context object becomes a
property of that object. Those properties can be modified after creation; primitive
drawing operations can also be added or removed from the contexts where they have been
created using the ``list`` operations ``append``, ``insert`` and ``remove``.

For example, if you were drawing a bar chart where the height of the bars changed over
time, you don't need to completely reset the canvas and redraw all the objects; you can
use the same objects, only modifying the height of existing bars, or adding and removing
bars as required. After making changes to the properties of a drawing object, you can
invoke :meth:`~toga.Canvas.redraw()` to request a redraw of the canvas. A redraw will
be automatically invoked when the canvas resizes.

In this example, we create 2 filled drawing objects, then manipulate those objects,
requesting a redraw after each set of changes.

.. code-block:: python

    import toga

    canvas = toga.Canvas()
    with canvas.fill(color="red") as fill:
        arc1 = fill.arc(x=50, y=50, radius=15)
        rect1 = fill.rect(x=50, y=50, width=15, height=15)

    # We can then change the properties of the drawing objects.
    # Make the arc smaller, and move it closer to the origin.
    arc1.x = 25
    arc1.y = 25
    arc1.radius = 5
    canvas.redraw()

    # Change the fill color to Blue
    fill.color = "blue"
    canvas.redraw()

    # Remove the rectangle from the canvas
    fill.remove(rect1)
    canvas.redraw()

For detailed tutorials on the use of Canvas drawing instructions, see the MDN
documentation for the `HTML5 Canvas API
<https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API>`__. Other than the change
in naming conventions for methods - the HTML5 APIs uses ``lowerCamelCase``, whereas the
Toga API uses ``snake_case`` - the usage of any APIs provided by Toga's canvas should be
the same.

Notes
-----

* The Canvas API allows the use of handlers to respond to mouse/pointer events. These
  event handlers differentiate between "primary" and "alternate" modes of activation.
  When a mouse is in use, alternate activation will usually be interpreted as a "right
  click"; however, platforms may not implement an alternate activation mode. To ensure
  cross-platform compatibility, applications should not use the alternate press handlers
  as the sole mechanism for accessing critical functionality.

Reference
---------

Main Interface
^^^^^^^^^^^^^^

.. autoclass:: toga.Canvas
   :members:
   :undoc-members:
   :exclude-members:

.. autoclass:: toga.widgets.canvas.Context
   :members:
   :undoc-members:
   :exclude-members:

Simple Drawing objects
^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: toga.widgets.canvas
   :members:
   :undoc-members:
   :exclude-members: Canvas, Context, ClosedPathContext, FillContext, StrokeContext

Drawing Context Objects
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: toga.widgets.canvas.ClosedPathContext
   :members:
   :undoc-members:
   :exclude-members:

.. autoclass:: toga.widgets.canvas.FillContext
   :members:
   :undoc-members:
   :exclude-members:

.. autoclass:: toga.widgets.canvas.StrokeContext
   :members:
   :undoc-members:
   :exclude-members:
