===================
Your first Toga app
===================

In this example, we're going to build a desktop app with a single
button, that prints to the console when you press the button.

Here's a complete code listing for our "Hello world" app::

    from __future__ import print_function, unicode_literals, absolute_import

    import toga


    def button_handler(widget):
        print("hello")


    def build(app):
        container = toga.Container()

        button = toga.Button('Hello world', on_press=button_handler)

        button.style.set(margin=50)

        container.add(button)

        return container


    if __name__ == '__main__':
        app = toga.App('First App', 'org.pybee.helloworld', startup=build)

        app.main_loop()


Lets walk through this one line at a time.

The code starts with imports. First, we have some ``__future__`` imports.
These to make Python 2 behave a bit more like Python 3. If you're using Python
3, you can omit this line::

    from __future__ import print_function, unicode_literals, absolute_import

Next, we import toga::

    import toga

Then, we set up a handler - a wrapper around behavior that we want to activate
when the button is pressed. A handler is just a function. The function takes
the widget that was activated as the first argument; depending on the type of
event that is being handled, other arguments may also be provided. In the case
of a simple button press, however, there are no extra arguments::

    def button_handler(widget):
        print("hello")

By creating an app, we're declaring that we want to have a main window, with a
main menu. However, Toga doesn't know what content we want in that
main window. The next step is to define a method that describes the UI that we
want our app to have. This method is a callable that accepts an app instance::

    def build(app):

We want to put a button in the window. However, unless we want the button to
fill the entire app window, we can't just put the button into the app window.
Instead, we need create a container, and put the button in the container.

A container is an object that can be used to hold multiple widgets, and to
define padding around widgets. So, we define a container::

        container = toga.Container()

We can then define a button. When we create the button, we can set the button
text, and we also set the behavior that we want to invoke when the button is
pressed, referencing the handler that we defined earlier::

        button = toga.Button('Hello world', on_press=button_handler)

Now we have to define how the button will appear in the window. Toga uses a
CSS-based layout scheme, so we can apply CSS styles to each widget::

        button.style.set(margin=50)

Each widget is a "block" in CSS terms, what we've done here is say that the
button with have a margin of 50 pixels on each side. If we wanted to define a
margin of 20 pixels on top of the button, we could have defined ``margin_top=20``,
or we could have specified the ``margin=(20,50,50,50)``.

The next step is to add the button to the container::

        container.add(button)

The button will, by default, stretch to the size of the container it is placed
in. The outer container is also a block, which will stretch to the size of
container it is placed in - which, in our case, is the window itself. The
button has a default height, defined by the way that the underlying platform
draws buttons). As a result, this means we'll see a single button in the app
window that stretches to the width of the screen, but has a 50 pixel margin
surrounding it.

Now we've set up the container, we return the outer container that holds all
the UI content. This container will be the content of the app's main window::

        return container

Lastly, we get into the main body of the program, where we create the app
itself. The app is a high level container representing the executable. The app
has a name, and a unique identifier. The identifier is used when registering
any app-specific system resources. By convention, the identifier is a
"reversed domain name". The app also accepts our callable defining the main
window contents::

    if __name__ == '__main__':

        app = toga.App('First App', 'org.pybee.helloworld', startup=build)

Having created the app, we can start the main app loop. This is a blocking
call; it won't return until you quit the main app::

        app.main_loop()

And that's it! Save this script as ``helloworld.py``, and you're ready to go.

Running the app
---------------

Before you run the app, you'll need to install toga. Although you *can* install
toga by just running::

    $ pip install toga

We strongly suggest that you **don't** do this. We'd suggest creating a `virtual
environment`_ first, and installing toga in that virtual environment.

.. _virtual environment: http://docs.python-guide.org/en/latest/dev/virtualenvs/

.. note:: Minimum versions

    Toga has some minimum requirements:

    * If you're on OS X, you need to be on 10.7 (Lion) or newer.

    * If you're on Linux, you need to have GTK+ 3.4 or later. This is the
      version that ships starting with Ubuntu 12.04 and Fedora 17.

    * If you want to use the WebView widget, you'll also need to
      have WebKit, plus the GI bindings to WebKit installed.
      
        * For Ubuntu that's provided by the libwebkitgtk-3.0-0 and
          gir1.2-webkit-3.0 packages.

        * For Fedora it's all provided in the webkitgtk3 package.

    If these requirements aren't met, Toga either won't work at all, or won't
    have full functionality.

.. note:: Problems with source installs

    Internally, Toga is comprised of a number of subpackages - one for each
    platform it supports. If you install using wheels, the install process will
    correctly identify the required packages and install them. However, if you
    install from source using pip, there is a `known bug in pip`_ that causes
    dependencies to not be installed. It may be necessary to manually install
    the following pre-requisites:

    * OS X: ``pip install toga-cocoa``
    * Linux: ``pip install toga-gtk toga-cassowary cassowary``
    * Win32: ``pip install toga-win32 toga-cassowary cassowary``

.. _known bug in pip: https://github.com/pypa/pip/issues/1951

.. note:: Problems under Linux

    Unfortunately, GTK+3 doesn't provide a pip-installable version of it's Python
    bindings, so if you're using a virtual environment with --no-site-packages
    installed (which is the default), GTK+ won't be in your ``PYTHONPATH`` inside
    a virtual environment.

    To make the system GTK+ bindings available to your virtualenv,
    symlink the `gi` module from the system dist-packages directory into your
    virtualenv's site-packages.
    
        For a Ubuntu 32bit system::

            $ cd $VIRTUAL_ENV/lib/python2.7/site-packages
            $ ln -si /usr/lib/python2.7/dist-packages/gi

        For a Fedora 64bit system::

            $ cd $VIRTUAL_ENV/lib/python2.7/site-packages
            $ ln -si /usr/lib64/python2.7/site-packages/gi/

Once you've got toga installed, you can run your script::

    $ python helloworld.py

This should pop up a window with a button:

.. image:: screenshots/tutorial-0.png

If you click on the button, you should see messages appear in the console.
Even though we didn't define anything about menus, the app will have default
menu entries to quit the app, and an About page. The keyboard bindings to quit
the app, plus the "close" button on the window will also work as expected. The
app will have a default Toga icon (a picture of Tiberius the yak).
