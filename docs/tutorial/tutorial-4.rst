=======================
Let's draw on a canvas!
=======================

.. note:: This tutorial only works on GTK for now!

    Want to help out? Maybe you could port the Canvas widget to other platforms?

One of the main capabilities needed to create many types of GUI applications is
the ability to draw and manipulate lines, shapes, text, and other graphics. To
do this in Toga, we use the Canvas Widget.

Utilizing the Canvas is as easy as determining the drawing operations you want to
perform and then creating a new Canvas. All drawing objects that are created
with one of the drawing operations are returned so that they can be modified or
removed.

1. We first define the drawing operations we want to perform in a new function::

     def draw_tiberius(self):
        tiberius_context = self.canvas.create_context()
        with self.canvas.context(tiberius_context):
           self.fill_head()

Notice that we also created and used a new context called tiberius_context. This
is optional and the default root context will be used if no context is created.

2. Next we create a new Canvas::

    self.canvas = toga.Canvas(style=Pack(flex=1))

That's all there is to! In this example we also add our canvas to the MainWindow
through use of the Box Widget::

        box = toga.Box(children=[self.canvas])
        self.main_window.content = box

You'll also notice in the full example below that some of the drawing operations
use the "with" keyword to utilize context managers including context,
closed_path, fill, and stroke. This reduces the repetition of commands while
utilizing these basic drawing capabilities.

.. image:: screenshots/tutorial-4.png

Here's the source code

.. literalinclude:: /../examples/tutorial4/tutorial/app.py
   :language: python

In this example, we see a new Toga widget - :class:`.Canvas`.
