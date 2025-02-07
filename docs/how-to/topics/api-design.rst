==========
API design
==========

Toga's API is structured around the following principles:

Properties
==========

Toga prefers to expose an object's state using property notation (e.g.
``widget.property``) rather than getter or setter methods.

Constructors
============

Any of a class's writable properties can be initialized in its constructor by passing
keyword arguments with the same names. The constructor may also accept read-only
properties such as :any:`Widget.id`, which cannot be changed later.

If a constructor has a single required argument, such as the text of a :any:`Label`, it
may be passed as a positional argument.

Events
======

Events are used to notify your app of user actions. To make your app handle an event,
you can assign either a regular or async callable to an event handler property. These
can be identified by their names, which always begin with ``on_``.

When the event occurs, your handler will be passed the widget as a positional argument,
and other event-specific information as keyword arguments. For forward compatibility
with arguments added in the future, handlers should always declare a ``**kwargs``
argument.

If an event is triggered by a change in a property:

* The new value of the property will be visible within the event handler.
* Setting the property programmatically will also generate an event, unless the property
  is set to its existing value, in which case whether it generates an event is
  undefined.

Common names
============

When a widget allows the user to control a simple value (e.g. the ``str`` of a
:any:`TextInput`, or the ``bool`` of a :any:`Switch`), then its property is called
``value``, and the corresponding event is called ``on_change``.

When a widget has a non-editable caption, (e.g. a :any:`Button` or :any:`Switch`), then
its property is called ``text``.
