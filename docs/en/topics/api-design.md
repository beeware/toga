# API design

Toga's API is structured around the following principles:

## Coding style

The public API follows a "Pythonic" style, using Python language idioms (e.g., context managers and iterators) and naming conventions (e.g., `snake_case`, not `CamelCase`), even if the underlying platforms don't lean that way.

Names are spelled according to US English.

## Properties

Wherever possible, Toga exposes an object's state using property notation (e.g. `widget.property`) rather than getter or setter methods.

Properties follow [Postel's Law](https://en.wikipedia.org/wiki/Robustness_principle) – for example, a widget's `text` property will accept any object when set, but will always return a string when retrieved.

## Constructors

Any of a class's writable properties can be initialized in its constructor by passing keyword arguments with the same names. The constructor may also accept read-only properties such as [`Widget.id`][toga.Widget.id], which cannot be changed later.

If a constructor has a single required argument, such as the text of a [`Label`][toga.Label], it may be passed as a positional argument.

## Events

Events are used to notify your app of user actions. To make your app handle an event, you can assign either a regular or async callable to an event handler property. These can be identified by their names, which always begin with `on_`.

Events are named for the general purpose of the interaction, not the specific mechanism. For example, a [`Button`][toga.Button]'s event is called `on_press`, not `on_click`, because "click" implies a mouse is used.

When the event occurs, your handler will be passed the widget as a positional argument, and other event-specific information as keyword arguments. For forward compatibility with arguments added in the future, handlers should always declare a `**kwargs` argument.

If an event is triggered by a change in a property:

- The new value of the property will be visible within the event handler.
- Setting the property programmatically will also generate an event, unless the property is set to its existing value, in which case whether it generates an event is undefined.

## Common names

When a widget allows the user to control a simple value (e.g. the `str` of a [`TextInput`][toga.TextInput], or the `bool` of a [`Switch`][toga.Switch]), then its property is called `value`, and the corresponding event is called `on_change`.

When a widget has a non-editable caption, (e.g. a [`Button`][toga.Button] or [`Switch`][toga.Switch]), then its property is called `text`.

Ranges of numbers are expressed as separate `min` and `max` properties.
