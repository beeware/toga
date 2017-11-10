=====================================
Let's draw on a canvas! (Gtk+ only for now, help needed!)
=====================================

One of the main capabilities needed to create many types of GUI applications is
the ability to draw and manipulate lines, shapes, and other graphics. To do this
in Toga, we use the Canvas Widget.

Utilizing the Canvas is easy as determining the drawing operations you want to
perform, placing them in a function, and then creating a new Canvas while
passing the function to the on_draw parameter.

1. We first define the drawing operations we want to perform in a new function::

    def draw_steps(self):
        self.canvas.stroke_style('rbga(0, 0, 0, 1)')

2. Next we create a new Canvas, and pass in the draw_steps method::

    self.canvas = toga.Canvas(on_draw=self.draw_steps)

That's all there is to! In this example we also add our canvas to the MainWindow
through use of the Box Widget::

        box = toga.Box(children=[self.canvas])
        self.main_window.content = box

You'll also notice in the full example below that some of the drawing operations
use the "with" keyword to utilize two context managers called closed_path and
fill. This reduces the repetition of commands while utilizing these basic
drawing capabilities.

.. image:: screenshots/tutorial-4.png

Here's the source code

.. literalinclude:: /tutorial/source/tutorial-4.py
   :language: python


In this example, we see a new Toga widget - :class:`.Canvas`.
