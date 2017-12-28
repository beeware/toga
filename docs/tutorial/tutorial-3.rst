======================
Let's build a browser!
======================

Although it's possible to build complex GUI layouts, you can get a lot
of functionality with very little code, utilizing the rich components that
are native on modern platforms.

So - let's build a tool that lets our pet yak graze the web - a primitive
web browser, in less than 40 lines of code!

.. image:: screenshots/tutorial-3.png

Here's the source code:

.. literalinclude:: /../examples/tutorial3/tutorial/app.py
   :language: python

In this example, you can see an application being developed as a class, rather
than as a build method. You can also see boxes defined in a declarative
manner - if you don't need to retain a reference to a particular widget, you
can define a widget inline, and pass it as an argument to a box, and it
will become a child of that box.
