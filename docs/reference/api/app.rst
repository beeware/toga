App
===

The top-level representation of an application.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :include: {0: '^Application$'}


Usage
-----

The App class is the top level representation of all application activity. It is a
singleton object - any given process can only have a single App. That
application may manage multiple windows, but it is guaranteed to have at least one
window (called the :attr:`~toga.App.main_window`); when the App's
:attr:`~toga.App.main_window` is closed, the application will exit.

The application is started by calling :meth:`~toga.App.main_loop()`. This will invoke
the :meth:`~toga.App.startup()` method of the app.

.. code-block:: python

    import toga

    app = toga.App("Simplest App", "com.example.simplest")
    app.main_loop()

You can populate an app's main window by passing a callable as the ``startup`` argument
to the :class:`toga.App` constructor. This ``startup`` method must return the content
that will be added to the main window of the app.

.. code-block:: python

    import toga

    def create_content(app):
        return toga.Box(children=[toga.Label("Hello!")])

    app = toga.App("Simple App", "com.example.simple", startup=create_content)
    app.main_loop()

This approach to app construction is most useful with simple apps. For most complex
apps, you should subclass :class:`toga.App`, and provide an implementation of
:meth:`~toga.App.startup()`. This implementation *must* create and assign a
``main_window`` for the app.

.. code-block:: python

    import toga

    class MyApp(toga.App):
        def startup(self):
            self.main_window = toga.MainWindow()
            self.main_window.content = toga.Box(children=[toga.Label("Hello!")])
            self.main_window.show()

    if __name__ == '__main__':
        app = MyApp("Realistic App", "org.beeware.realistic")
        app.main_loop()

Every app must have a formal name (a human readable name), and an app ID (a
machine-readable identifier - usually a reversed domain name). In the examples above,
these are provided as constructor arguments. However, you can also provide these
details, along with many of the other constructor arguments, as packaging metadata in a
format compatible with :any:`importlib.metadata`. If you deploy your app with `Briefcase
<https://briefcase.readthedocs.io/en/stable>`__, this will be done automatically.

A Toga app will install a number of default commands to reflect core application
functionality (such as the Quit/Exit menu item, and the About menu item). The IDs for
these commands are defined as constants on the :class:`~toga.Command` class. These
commands are installed by the :meth:`~toga.App.create_app_commands()` method; this
method is invoked *after* :meth:`~toga.App.startup()`, but *before* menus are populated
for the first time. If you wish to customize the menu items exposed by your app, you should
override the :meth:`~toga.App.create_app_commands()` method.

Assigning a main window
-----------------------

An app *must* assign ``main_window`` as part of the startup process. However, the value
that is assigned as the main window will affect the behavior of the app.

Standard app
~~~~~~~~~~~~

The most common type of app will assign a :any:`toga.MainWindow` instance as the main
window. On platforms that have menu bars inside their windows, this will create a main
window with a menu bar, populated with the default app commands. The window assigned as
the main window will have its title set to the formal name of the app. A
:any:`toga.MainWindow` may also have a toolbar. When the main window is closed, the app
will exit.

This is the type of app that will be created if you use an instance of :any:`toga.App`
passing in a ``startup`` argument to the constructor.

Simple app
~~~~~~~~~~

To create an app that *doesn't* have these default menu items, or you can assign an
instance of :any:`toga.Window` as the main window. A :any:`toga.Window` does not have a
menu bar; and as a result, neither will your app. As with a normal app, the window
assigned as the main window will have its title set to the formal name of the app; and
when the main window is closed, the app will exit. The :any:`toga.Window` instance used
used as the main window *must* be closable (i.e., you can't specify `closable=False`) -
otherwise, you wouldn't be able to exit the app.

Notes
-----

* Apps executed under Wayland on Linux environment may not show the app's formal name
  correctly. Wayland considers many aspects of app operation to be the domain of the
  windowing environment, not the app; as a result, some API requests will be ignored
  under a Wayland environment. Correctly displaying the app's formal name requires the
  use of a desktop metadata that Wayland can read. Packaging your app with `Briefcase
  <https://briefcase.readthedocs.io/en/stable>`__ is one way to produce this metadata.

Reference
---------

.. autoclass:: toga.App

.. autoprotocol:: toga.app.AppStartupMethod
.. autoprotocol:: toga.app.BackgroundTask
.. autoprotocol:: toga.app.OnExitHandler
