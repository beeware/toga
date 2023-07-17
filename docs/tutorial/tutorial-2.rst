=====================================
You put the box inside another box...
=====================================

If you've done any GUI programming before, you will know that one of the
biggest problems that any widget toolkit solves is how to put widgets on the
screen in the right place. Different widget toolkits use different approaches
- constraints, packing models, and grid-based models are all common. Toga's
Pack style engine borrows heavily from an approach that is new for widget
toolkits, but well proven in computing: Cascading Style Sheets (CSS).

If you've done any design for the web, you will have come across CSS before as
the mechanism that you use to lay out HTML on a web page. Although this is the
reason CSS was developed, CSS itself is a general set of rules for laying out
any "boxes" that are structured in a tree-like hierarchy. GUI widgets are an
example of one such structure.

To see how this works in practice, lets look at a more complex example,
involving layouts, scrollers, and containers inside other containers:

.. image:: screenshots/tutorial-2.png

Here's the source code:

.. literalinclude:: /../examples/tutorial2/tutorial/app.py
   :language: python

In order to render the icons, you will need to move the icons folder into the
same directory as your app file.

Here are the :download:`Icons <./resources/icons.zip>`

In this example, we see a couple of new Toga widgets - :class:`.Table`,
:class:`.SplitContainer`, and :class:`.ScrollContainer`. You can also see that
CSS styles can be added in the widget constructor. Lastly, you can
see that windows can have toolbars.

You'll also see that we're not creating a :class:`toga.App` directly. Instead, we're
declaring a subclass of `toga.App`, and instantiating that class. This also changes the
startup sequence of the app - instead of a function called ``build()``, the app invokes
a method on the app class named ``startup()``. This method behaves slightly differently
to our ``build()`` method - whereas previously the ``build()`` method returned the content
that we wanted to put into our main window, the ``startup()`` method is responsible for
creating and showing the main window of the app.
