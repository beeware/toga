===================
Your first Toga app
===================

In this example, we're going to build a desktop app with a single
button, that prints to the console when you press the button.

Set up your development environment
===================================

If you haven't got Python 3 installed, you can do so via `the official installer
<https://www.python.org/downloads>`_, or using your operating system's package manager.

The recommended way of setting up your development environment for Toga is to install a
virtual environment, install the required dependencies and start coding. To set up a
virtual environment, open a fresh terminal session, and run:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      $ mkdir toga-tutorial
      $ cd toga-tutorial
      $ python3 -m venv venv
      $ source venv/bin/activate

  .. group-tab:: Linux

    .. code-block:: console

      $ mkdir toga-tutorial
      $ cd toga-tutorial
      $ python3 -m venv venv
      $ source venv/bin/activate

  .. group-tab:: Windows

    .. code-block:: doscon

      C:\...>mkdir toga-tutorial
      C:\...>cd toga-tutorial
      C:\...>py -m venv venv
      C:\...>venv\Scripts\activate

Your prompt should now have a ``(venv)`` prefix in front of it.

Next, install Toga into your virtual environment:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ python -m pip install toga

  .. group-tab:: Linux

    Before you install Toga, you'll need to install some system packages.

    .. include:: /reference/platforms/unix-prerequisites.rst

    Then, install Toga:

    .. code-block:: console

      (venv) $ python -m pip install toga

    If you get an error when installing Toga, please ensure that you have fully installed
    all the platform prerequisites.

  .. group-tab:: Windows

    Confirm that your system meets the :ref:`Windows prerequisites
    <windows-prerequisites>`; then run:

    .. code-block:: doscon

      (venv) C:\...>python -m pip install toga

After a successful installation of Toga you are ready to get coding.

Write the app
=============

Create a new file called ``helloworld.py`` and add the following code for the
"Hello world" app:

.. literalinclude:: /../examples/tutorial0/tutorial/app.py
   :language: python


Let's walk through this one line at a time.

The code starts with imports. First, we import toga::

    import toga

Then we set up a handler, which is a wrapper around behavior that we want to activate
when the button is pressed. A handler is just a function. The function takes
the widget that was activated as the first argument; depending on the type of
event that is being handled, other arguments may also be provided. In the case
of a simple button press, however, there are no extra arguments::

    def button_handler(widget):
        print("hello")

When the app gets instantiated (in ``main()``, discussed below), Toga will create
a window with a menu. We need to provide a method that tells Toga what content
to display in the window. The method can be named anything, it just needs to
accept an app instance::

    def build(app):

We want to put a button in the window. However, unless we want the button to
fill the entire app window, we can't just put the button into the app window.
Instead, we need create a box, and put the button in the box.

A box is an object that can be used to hold multiple widgets, and to
define padding around widgets. So, we define a box::

        box = toga.Box()

We can then define a button. When we create the button, we can set the button
text, and we also set the behavior that we want to invoke when the button is
pressed, referencing the handler that we defined earlier::

        button = toga.Button('Hello world', on_press=button_handler)

Now we have to define how the button will appear in the window. By default,
Toga uses a style algorithm called ``Pack``, which is a bit like "CSS-lite".
We can set style properties of the button::

        button.style.padding = 50

What we've done here is say that the button will have a padding of 50 pixels
on all sides. If we wanted to define padding of 20 pixels on top of the
button, we could have defined ``padding_top = 20``, or we could have specified
the ``padding = (20, 50, 50, 50)``.

Now we will make the button take up all the available width::

       button.style.flex = 1

The ``flex`` attribute specifies how an element is sized with respect to other
elements along its direction. The default direction is row (horizontal) and
since the button is the only element here, it will take up the whole width.
Check out `style docs
<https://toga.readthedocs.io/en/latest/reference/style/pack.html#flex>`_ for
more information on how to use the ``flex`` attribute.

The next step is to add the button to the box::

        box.add(button)

The button has a default height, defined by the way that the underlying platform
draws buttons. As a result, this means we'll see a single button in the app
window that stretches to the width of the screen, but has a 50 pixel space
surrounding it.

Now we've set up the box, we return the outer box that holds all the UI content.
This box will be the content of the app's main window::

        return box

Lastly, we instantiate the app itself. The app is a high level container
representing the executable. The app has a name and a unique identifier. The
identifier is used when registering any app-specific system resources. By
convention, the identifier is a "reversed domain name". The app also accepts our
method defining the main window contents. We wrap this creation process into a
method called ``main()``, which returns a new instance of our application::

    def main():
        return toga.App('First App', 'org.beeware.helloworld', startup=build)

The entry point for the project then needs to instantiate this entry point
and start the main app loop. The call to ``main_loop()`` is a blocking call;
it won't return until you quit the main app::

    if __name__ == '__main__':
        main().main_loop()

And that's it! Save this script as ``helloworld.py``, and you're ready to go.

Running the app
---------------

The app acts as a Python module, which means you need to run it in a different
manner than running a regular Python script: You need to specify the :code:`-m`
flag and *not* include the :code:`.py` extension for the script name.

Here is the command to run for your platform from your working directory:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ python -m helloworld

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ python -m helloworld

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>python -m helloworld

This should pop up a window with a button:

.. image:: screenshots/tutorial-0.png

If you click on the button, you should see messages appear in the console.
Even though we didn't define anything about menus, the app will have default
menu entries to quit the app, and an About page. The keyboard bindings to quit
the app, plus the "close" button on the window will also work as expected. The
app will have a default Toga icon (a picture of Tiberius the yak).

Troubleshooting issues
----------------------

Occasionally you might run into issues running Toga on your computer.

Before you run the app, you'll need to install toga. Although you *can* install
toga by just running:

.. code-block:: console

    $ python -m pip install toga

We strongly suggest that you **don't** do this. We'd suggest creating a `virtual
environment`_ first, and installing toga in that virtual environment as directed
at the top of this guide.

.. _virtual environment: https://docs.python-guide.org/dev/virtualenvs/

Once you've got Toga installed, you can run your script:

.. code-block:: console

    (venv) $ python -m helloworld
