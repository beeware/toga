{{ component_header("Canvas", width=300) }}

## Usage

Canvas is a 2D vector graphics drawing area, whose API broadly follows the [HTML5 Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API). The Canvas provides a drawing `State`; drawing instructions are then added to that state by calling methods on the state. All positions and sizes are measured in [CSS pixels][css-units].

For example, the following code will draw an orange horizontal line:

```python
import toga
canvas = toga.Canvas()
state = canvas.root_state

state.begin_path()
state.move_to(20, 20)
state.line_to(160, 20)
state.stroke(color="orange")
```

Toga adds an additional layer of convenience to the base HTML5 API by providing context managers for operations that have a natural open/close life cycle. For example, the previous example could be replaced with:

```python
import toga
canvas = toga.Canvas()

with canvas.state.Stroke(20, 20, color="orange") as stroke:
    stroke.line_to(160, 20)
```

Any argument provided to a drawing operation or state object becomes a property of that object. Those properties can be modified after creation, after which you should invoke [`Canvas.redraw`][toga.Canvas.redraw] to request a redraw of the canvas.

Drawing operations can also be added to or removed from a state using the `list` operations `append`, `insert`, `remove` and `clear`. In this case, [`Canvas.redraw`][toga.Canvas.redraw] will be called automatically.

For example, if you were drawing a bar chart where the height of the bars changed over time, you don't need to completely reset the canvas and redraw all the objects; you can use the same objects, only modifying the height of existing bars, or adding and removing bars as required.

In this example, we create 2 filled drawing objects, then manipulate those objects, requesting a redraw after each set of changes.

```python
import toga

canvas = toga.Canvas()
with canvas.root_state.Fill(color="red") as fill:
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
```

For detailed tutorials on the use of Canvas drawing instructions, see the MDN documentation for the [HTML5 Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API). Other than the change in naming conventions for methods - the HTML5 API uses `lowerCamelCase`, whereas the Toga API uses `snake_case` - both APIs are very similar.

## Notes

- Toga does not guarantee pixel perfect rendering of Canvas content across all platforms. Most drawing instructions will appear identical across all platforms, and in the worst case, any given set of drawing instructions should result in a fundamentally similar image. However, text and other complex curve and line geometries (such as miters on tight corners) will result in minor discrepancies between platforms. Color rendition can also vary slightly between platforms depending on the color profiles of the device being used to render the canvas.

- The Canvas API allows the use of handlers to respond to mouse/pointer events. These event handlers differentiate between "primary" and "alternate" modes of activation. When a mouse is in use, alternate activation will usually be interpreted as a "right click"; however, platforms may not implement an alternate activation mode. To ensure cross-platform compatibility, applications should not use the alternate press handlers as the sole mechanism for accessing critical functionality.

## Reference

::: toga.Canvas
    options:
        members:
            - ClosedPath
            - State
            - Fill
            - Stroke
            - as_image
            - root_state
            - enabled
            - focus
            - measure_text
            - on_activate
            - on_alt_drag
            - on_alt_press
            - on_alt_release
            - on_drag
            - on_press
            - on_release
            - on_resize
            - redraw

::: toga.widgets.canvas.State
    options:
        inherited_members: True

::: toga.widgets.canvas.DrawingAction

::: toga.widgets.canvas.ClosedPathContext

::: toga.widgets.canvas.FillContext

::: toga.widgets.canvas.StrokeContext

::: toga.widgets.canvas.OnTouchHandler

::: toga.widgets.canvas.OnResizeHandler
