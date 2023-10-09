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
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(Canvas|Component))'}

Usage
-----

Canvas is a 2D vector graphics drawing area, whose API broadly follows the `HTML5 Canvas
API <https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API>`__. The Canvas
provides a drawing Context; drawing instructions are then added to that context by
calling methods on the context. All positions and sizes are measured in :ref:`CSS pixels
<css-units>`.

For example, the following code will draw an orange horizontal line:

.. code-block:: python

    import toga
    canvas = toga.Canvas()
    context = canvas.context

    context.begin_path()
    context.move_to(20, 20)
    context.line_to(160, 20)
    context.stroke(color="orange")

Toga adds an additional layer of convenience to the base HTML5 API by providing context
managers for operations that have a natural open/close life cycle. For example, the
previous example could be replaced with:

.. code-block:: python

    import toga
    canvas = toga.Canvas()

    with canvas.context.Stroke(20, 20, color="orange") as stroke:
        stroke.line_to(160, 20)

Any argument provided to a drawing operation or context object becomes a property of
that object. Those properties can be modified after creation, after which you should
invoke :any:`Canvas.redraw` to request a redraw of the canvas.

Drawing operations can also be added to or removed from a context using the ``list``
operations ``append``, ``insert``,  ``remove`` and ``clear``. In this case,
:any:`Canvas.redraw` will be called automatically.

For example, if you were drawing a bar chart where the height of the bars changed over
time, you don't need to completely reset the canvas and redraw all the objects; you can
use the same objects, only modifying the height of existing bars, or adding and removing
bars as required.

In this example, we create 2 filled drawing objects, then manipulate those objects,
requesting a redraw after each set of changes.

.. code-block:: python

    import toga

    canvas = toga.Canvas()
    with canvas.context.Fill(color="red") as fill:
        circle = fill.arc(x=50, y=50, radius=15)
        rect = fill.rect(x=50, y=50, width=15, height=15)

    # We can then change the properties of the drawing objects.
    # Make the circle smaller, and move it closer to the origin.
    circle.x = 25
    circle.y = 25
    circle.radius = 5
    canvas.redraw()

    # Change the fill color to blue
    fill.color = "blue"
    canvas.redraw()

    # Remove the rectangle from the canvas
    fill.remove(rect)

For detailed tutorials on the use of Canvas drawing instructions, see the MDN
documentation for the `HTML5 Canvas API
<https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API>`__. Other than the change
in naming conventions for methods - the HTML5 API uses ``lowerCamelCase``, whereas the
Toga API uses ``snake_case`` - both APIs are very similar.

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

.. autoclass:: toga.Canvas
    :exclude-members: new_path, move_to, line_to, bezier_curve_to, quadratic_curve_to,
        arc, ellipse, rect, write_text, rotate, scale, translate, reset_transform,
        closed_path, fill, stroke

.. autoclass:: toga.widgets.canvas.Context
    :special-members: __getitem__, __len__

.. autoclass:: toga.widgets.canvas.DrawingObject

.. autoclass:: toga.widgets.canvas.ClosedPathContext
.. autoclass:: toga.widgets.canvas.FillContext
.. autoclass:: toga.widgets.canvas.StrokeContext

.. autoprotocol:: toga.widgets.canvas.OnTouchHandler
.. autoprotocol:: toga.widgets.canvas.OnResizeHandler
