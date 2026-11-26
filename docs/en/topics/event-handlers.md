# Passing arguments to event handlers

Toga event handlers receive information about the event that triggered them. For example, a button's `on_press` handler receives the button as its first argument and may receive additional keyword arguments.

```python
def button_handler(widget, **kwargs):
    print(f"{widget.text} was pressed")
```

Sometimes an event handler also needs additional information that is not provided by the event itself. Python provides several ways to pass this information to a handler.

## Using a closure

A closure is a function that remembers variables from the scope in which it was created. It can be used to create an event handler with access to additional information.

```python
import toga


def create_handler(message):
    def handler(widget, **kwargs):
        print(message)
        print(f"{widget.text} was pressed")

    return handler


button = toga.Button(
    "Click me",
    on_press=create_handler("Hello from the handler!"),
)
```

In this example, `create_handler()` creates and returns a handler that remembers the supplied `message`. When the button is pressed, Toga invokes the returned handler with the button as its `widget` argument.

## Using functools.partial

Python's `functools.partial` provides another way to bind arguments to a function before it is called.

```python
import toga
from functools import partial


def button_handler(message, widget, **kwargs):
    print(message)
    print(f"{widget.text} was pressed")


button = toga.Button(
    "Click me",
    on_press=partial(button_handler, "Hello from the handler!"),
)
```

Here, `partial()` binds the `message` argument in advance. Toga supplies the remaining `widget` and event keyword arguments when the button is pressed.

Both closures and `functools.partial` are useful for passing additional information to event handlers. Choose the approach that makes the handler easiest to understand.

## Asynchronous event handlers

An event handler can also be an asynchronous function when it needs to perform asynchronous work.

```python
import asyncio


async def button_handler(widget, **kwargs):
    await asyncio.sleep(1)
    print(f"{widget.text} was pressed")
```

For more information about asynchronous operations and scheduling tasks, see the [dialog documentation](../reference/api/application/dialogs.md).

**Note:** Generator-based event handlers are deprecated. Use an `async def` handler and `await` asynchronous operations instead.
