# Canvas migration guide

The Canvas widget's interface has changed quite a bit in Toga 0.5.4. We aim to maintain compatibility with user code that's been written for earlier versions. However, you'll likely see a lot of deprecation warnings, and since support for deprecated usage will eventually be removed, it's a good idea to update your code. This page explains how the interface has changed, and how to adapt existing code to it.

## Updated names

The names of several classes and methods have changed.

- Previously, in addition to the "one-shot" [`fill`][toga.Canvas.fill], [`stroke`][toga.Canvas.stroke], and [`close_path`][toga.Canvas.close_path] methods, there were analogous methods (`Fill`, `Stroke`, and `ClosedPath`) that functioned as context managers. These capitalized names (and the "close"/"closed" difference) are deprecated; the lower-case methods can now function as either standalone commands or as context managers.
- Previously, the current state of the drawing context was represented by a class named `Context`; all context managers inherited from it. The same idea is now represented by the [`State`][toga.widgets.canvas.State] class, and other context managers inherit from its abstract [`BaseState`][toga.widgets.canvas.BaseState] parent class.
- Accordingly, the canvas's top-level state object has been moved from `Canvas.context` to [`Canvas.root_state`][toga.Canvas.root_state], and the `Context()` method that saved and restores state has been renamed to [`state()`][toga.Canvas.state].
- `DrawingObject` has been renamed to [`DrawingAction`][toga.widgets.canvas.DrawingAction].

## Drawing methods have moved to Canvas

Previously, the drawing methods ([`line_to()`][toga.Canvas.fill], [`rect()`][toga.Canvas.rect], and so on) existed on the `Context` class (which is now named [`State`][toga.widgets.canvas.State]). In order to carry out drawing operations, these methods were called on either the canvas's [top-level context][toga.Canvas.root_state] or on a subcontext. All drawing methods should now be called directly on the canvas. For example, this code:

```python
import toga
canvas = toga.Canvas()
context = canvas.context

context.begin_path()
context.move_to(20, 20)
context.line_to(160, 20)
context.stroke()

with context.Context() as subcontext:
    subcontext.line_to(160, 20)

```

would now be written like this:

```python
import toga
canvas = toga.Canvas()

canvas.begin_path()
canvas.move_to(20, 20)
canvas.line_to(160, 20)
canvas.stroke()

with canvas.context.state():
    canvas.line_to(160, 20)

```

Context managers (like [`state`][toga.Canvas.state] in the above example) still [return the state object in case you need it][accessing-specific-drawingactions], but for most usage you don't have to pay attention to that. The canvas will automatically handling what to do when in or out of a context manager.

## Changes to method signatures

### Coordinates in context managers

The deprecated `Fill`, `Stroke`, and `ClosedPath` context managers took `x` and `y` parameters; supplying them moved to those coordinates when the context manager was entered. The [`fill`][toga.Canvas.fill], [`stroke`][toga.Canvas.stroke], and [`close_path`][toga.Canvas.close_path] context managers don't accept coordinates; call `move_to()` inside the context manager instead.

In other words, existing code like this:

```python
with canvas.context.Stroke(20, 20) as stroke:
    stroke.line_to(12, 50)
```

should be changed to:

```python
with canvas.stroke():
    canvas.move_to(20, 20)
    canvas.line_to(12, 50)
```

### Keyword-only extra parameters

Toga's [`fill`][toga.Canvas.fill] and [`stroke`][toga.Canvas.stroke] accept optional arguments that aren't part of the HTML spec, such as specifying [`line_width`][toga.Canvas.line_width] within the call to `stroke`. These parameters are now keyword-only; only parameters included in the equivalent HTML Canvas method can be provided positionally.

### `fill_style` and `stroke_style`

One optional parameter shared between [`fill`][toga.Canvas.fill] and [`stroke`][toga.Canvas.stroke] is `color`; in `fill`, it sets [`fill_style`][toga.Canvas.fill_style], while in `stroke`, it sets [`stroke_style`][toga.Canvas.stroke_style]. Each has now been renamed to its more "proper" name, but `color` has been maintained as an alias.

## No list-like methods or automatic redrawing

`Context` objects (now [`State`][toga.widgets.canvas.State] or other subclasses of [`BaseState`][toga.widgets.canvas.BaseState]) previously had list-like methods for [manipulating their stored lists of drawing actions][creating-and-adding-new-drawingactions]. These methods handled redrawing the canvas when changes were made. These methods are now deprecated; the standard approach is now to directly manipulate the state's [`drawing_actions`][toga.widgets.canvas.BaseState.drawing_actions] list directly. You'll need to manually call the canva's [`redraw()`][toga.Canvas.redraw] method afterward; this is now consistent with the behavior when moodifying attributes of a [`DrawingAction`][toga.widgets.canvas.DrawingAction].

Existing code might look something like this:

```python
import toga

canvas = toga.Canvas()

with canvas.context.Fill() as fill:
    canvas.move_to(0, 0)
    fill.arc(50, 50, radius=15)
    rect = fill.rect(50, 50, width=15, height=15)

# Remove the rectangle drawing action
fill.remove(rect)
```



```python
import toga

canvas = toga.Canvas()

with canvas.fill() as fill:
    canvas.move_to(0, 0)
    canvas.arc(50, 50, radius=15)
    rect = canvas.rect(x=50, y=50, width=15, height=15)

# Remove the rectangle drawing action
fill.drawing_actions.remove(rect)
canvas.redraw()
```
