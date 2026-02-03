{{ component_header("Canvas", width=300) }}

## Usage

Canvas is a 2D vector graphics drawing area, whose API broadly follows the [HTML5 Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API). Drawing methods are called directly on the Canvas. All positions and sizes are measured in [CSS pixels][css-units].

For example, the following code will draw an orange horizontal line:

```python
import toga
canvas = toga.Canvas()

canvas.begin_path()
canvas.move_to(20, 20)
canvas.line_to(160, 20)
canvas.stroke(color="orange")
```

Toga adds an additional layer of convenience to the base HTML5 API by providing context managers for operations that have a natural open/close life cycle. For example, the previous example could be replaced with:

```python
import toga
canvas = toga.Canvas()

with canvas.stroke(color="orange", 20, 20):
    canvas.line_to(160, 20)
```

Any argument provided to a drawing operation (including context managers) becomes a property of that object. Those properties can be modified after creation, after which you should invoke [`Canvas.redraw`][toga.Canvas.redraw] to request a redraw of the canvas.

A state stores a list of its associated drawing instructions as an attribute named [`drawing_actions`][toga.widgets.canvas.State.drawing_actions]. This can be modified like any other list (`append`, `insert`, `remove`, `clear`, etc.). As with modifying attributes, [`Canvas.redraw`][toga.Canvas.redraw] will need to be called to show the changes.

For example, if you were drawing a bar chart where the height of the bars changed over time, you don't need to completely reset the canvas and redraw all the objects; you can use the same objects, only modifying the height of existing bars, or adding and removing bars as required.

In this example, we create 2 filled drawing actions, then manipulate those objects, requesting a redraw after each set of changes.

```python
import toga

canvas = toga.Canvas()
with canvas.fill(color="red") as fill:
    circle = canvas.arc(x=50, y=50, radius=15)
    rect = canvas.rect(x=50, y=50, width=15, height=15)

# We can then change the properties of the drawing actions.
# Make the circle smaller, and move it closer to the origin.
circle.x = 25
circle.y = 25
circle.radius = 5

# Change the fill color to blue
fill.color = "blue"

# Remove the rectangle from the canvas
fill.drawing_actions.remove(rect)

# Display the changes
canvas.redraw()
```

For detailed tutorials on the use of Canvas drawing instructions, see the MDN documentation for the [HTML5 Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API). Other than the change in naming conventions for methods - the HTML5 API uses `lowerCamelCase`, whereas the Toga API uses `snake_case` - both APIs are very similar.

## Notes

- The Canvas API allows the use of handlers to respond to mouse/pointer events. These event handlers differentiate between "primary" and "alternate" modes of activation. When a mouse is in use, alternate activation will usually be interpreted as a "right click"; however, platforms may not implement an alternate activation mode. To ensure cross-platform compatibility, applications should not use the alternate press handlers as the sole mechanism for accessing critical functionality.

## Reference

::: toga.Canvas
    options:
        inherited_members: True
        members:
            # Attributes; no way *not* to list them first
            - enabled
            - on_activate
            - on_alt_drag
            - on_alt_press
            - on_alt_release
            - on_drag
            - on_press
            - on_release
            - on_resize
            - root_state
            # Drawing methods
            - begin_path
            - close_path
            - move_to
            - line_to
            - bezier_curve_to
            - quadratic_curve_to
            - arc
            - ellipse
            - rect
            - fill
            - stroke
            - write_text
            - draw_image
            - rotate
            - scale
            - translate
            - reset_transform
            - state
            # Other methods
            - redraw
            - measure_text
            - as_image
            - focus

::: toga.widgets.canvas.State

::: toga.widgets.canvas.DrawingAction

::: toga.widgets.canvas.ClosePath

::: toga.widgets.canvas.Fill

::: toga.widgets.canvas.Stroke

::: toga.widgets.canvas.OnTouchHandler

::: toga.widgets.canvas.OnResizeHandler
