=====================================
You put the box inside another box...
=====================================

.. include:: /tutorial/tutorial-issues-note.rst

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

In order to render the icons, you will need to have the icon files inside a
``icons`` folder in the same directory as your app file.

Here are the :download:`Icons <./resources/icons.zip>`

The ``rebase_path`` function handles two cases: when your application is
launched as a single file module, Toga needs an absolute file path; but when
launched as a package module, or through briefcase, it should be a relative
file path. On a real world scenario, you would be using only relative paths.

In this example, we see a couple of new Toga widgets - :class:`.Table`,
:class:`.SplitContainer`, and :class:`.ScrollContainer`. You can also see that
CSS styles can be added in the widget constructor. Lastly, you can
see that windows can have toolbars.
