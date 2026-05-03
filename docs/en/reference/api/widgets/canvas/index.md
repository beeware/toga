{{ component_header("Canvas", width=300) }}

/// admonition | Seeing deprecation warnings?
If you've updated Toga from 0.5.3 to 0.5.4 or newer and are seeing deprecation warnings from your existing code that uses Canvas, check the [migration guide](./migration.md) for info on how to update to the new API.
///

## Usage

Canvas is a 2D vector graphics drawing area, whose API broadly follows the [HTML5 Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API). Drawing methods are called directly on the Canvas. All positions and sizes are measured in [CSS pixels][css-units].

For example, the following code will draw an orange horizontal line:

```python
import toga

canvas = toga.Canvas()

canvas.stroke_style = "orange"
canvas.begin_path()
canvas.move_to(20, 20)
canvas.line_to(160, 20)
canvas.stroke()
```

Result:

![Usage example](./images/usage.png)

## Additional features

Toga adds some additional Pythonic conveniences to the base HTML5 API. First, a number of drawing methods that have a natural open/close life cycle ([`close_path()`][toga.Canvas.close_path], [`stroke()`][toga.Canvas.stroke], and [`fill()`][toga.Canvas.fill]) can additionally function as [context managers](https://docs.python.org/3/reference/datamodel.html#context-managers). Second, `fill` and `stroke` accept optional arguments to specify their parameters directly. Using both of these features, the previous example could be rewritten to:

```python
import toga

canvas = toga.Canvas()

with canvas.stroke(stroke_style="orange"):
    canvas.move_to(20, 20)
    canvas.line_to(160, 20)
```

Toga also provides one additional method, [`state()`][toga.Canvas.state], which is useful *only* as a context manager; it saves context upon entering, and restores it upon existing. That is, the two following snippets are functionally identical:

```python
canvas.fill_style = "blue"

canvas.save()
canvas.fill_style = "red"
canvas.restore()

# Fill style is now restored to blue.
```

```python
canvas.fill_style = "blue"

with canvas.state():
    canvas.fill_style = "red"

# Fill style is now restored to blue.
```

## Further reading

This page documents all of Canvas's drawing methods; for more detailed and illustrative tutorials, see the MDN documentation for the [HTML5 Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API). Other than the change in naming conventions for methods - the HTML5 API uses `lowerCamelCase`, whereas the Toga API uses `snake_case` - both APIs are very similar.

## Notes

- Toga does not guarantee pixel perfect rendering of Canvas content across all platforms. Most drawing instructions will appear identical across all platforms, and in the worst case, any given set of drawing instructions should result in a fundamentally similar image. However, text and other complex curve and line geometries (such as miters on tight corners) will result in minor discrepancies between platforms. Color rendition can also vary slightly between platforms depending on the color profiles of the device being used to render the canvas.

- The Canvas API allows the use of handlers to respond to mouse/pointer events. These event handlers differentiate between "primary" and "alternate" modes of activation. When a mouse is in use, alternate activation will usually be interpreted as a "right click"; however, platforms may not implement an alternate activation mode. To ensure cross-platform compatibility, applications should not use the alternate press handlers as the sole mechanism for accessing critical functionality.

## Advanced usage

It's also possible to reach beyond the HTML Canvas-based API documented here, and interact directly with the underlying structure that Canvas uses to store the series of drawing operations it's performed. This allows you to modify the rendered result nonlinearly, going "back in time" to change previous instructions. For more information, see [Advanced Canvas usage](./advanced.md).

## Reference

<!-- REMOVE WHEN RESOLVED -->
<!-- rumdl-disable MD013 MD022 MD023 -->
::: toga.Canvas
    options:
        inherited_members: True
        members:
            # Attributes; no way *not* to list them first
            - fill_style
            - stroke_style
            - line_width
            - line_dash
            - root_state
            - enabled
            - on_activate
            - on_alt_drag
            - on_alt_press
            - on_alt_release
            - on_drag
            - on_press
            - on_release
            - on_resize
            # Drawing methods
            - save
            - restore
            - state
            - begin_path
            - close_path
            - move_to
            - line_to
            - bezier_curve_to
            - quadratic_curve_to
            - arc
            - ellipse
            - rect
            - round_rect
            - fill
            - stroke
            - write_text
            - draw_image
            - rotate
            - scale
            - translate
            - reset_transform
            # Other methods
            - measure_text
            - as_image
            - focus
            - redraw

::: toga.widgets.canvas.OnTouchHandler

::: toga.widgets.canvas.OnResizeHandler
