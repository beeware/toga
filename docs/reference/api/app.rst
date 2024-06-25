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
singleton object - any given process can only have a single App. That application may
manage multiple windows, but it will generally have at least one window (called the
:attr:`~toga.App.main_window`).

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
:meth:`~toga.App.startup()`. This implementation *must* assign a value to
:attr:`~toga.App.main_window` for the app. The value that is assigned controls the type
of app that is created. The possible values that can be assigned to
:attr:`~toga.App.main_window` is :ref:`discussed below <assigning-main-window>`; the
most common type of app will assign an instance of :any:`toga.MainWindow`:

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
commands are automatically installed *before* :meth:`~toga.App.startup()` is invoked. If
you wish to customize the menu items exposed by your app, you can add or remove commands
in your :meth:`~toga.App.startup()` implementation.

.. _assigning-main-window:

Assigning a main window
-----------------------

An app *must* assign ``main_window`` as part of the startup process. However, the value
that is assigned as the main window will affect the behavior of the app.

:class:`~toga.Window`
~~~~~~~~~~~~~~~~~~~~~

Most apps will assign an instance of :class:`toga.Window` (or a subclass,
such as :class:`toga.MainWindow`) as the main window. This window will control
the life cycle of the app. When the window assigned as the main window is closed, the
app will exit.

If you create an ``App`` by passing a ``startup`` argument to the constructor, a
:class:`~toga.MainWindow` will be automatically created and assigned to ``main_window``.

``None``
~~~~~~~~

If your app doesn't have a single "main" window, but instead has multiple windows that
are equally important (e.g., a document editor, or a web browser), you can assign a
value of ``None`` to :attr:`~toga.App.main_window`. The resulting behavior is slightly
different on each platform, reflecting platform differences.

On macOS, the app is allowed to continue running without having any open windows. The
app can open and close windows as required; the app will keep running until explicitly
exited.

On Linux and Windows, when an app closes the last window it is managing, the app will
automatically exit. Attempting to closing the last window will trigger any app-level
:meth:`~toga.App.on_exit` handling in addition to any window-specific
:meth:`~toga.Window.on_close` handling.

Mobile, web and console platforms *must* define a main window.

:attr:`~toga.App.BACKGROUND`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assigning a value of :attr:`toga.App.BACKGROUND` as the main window will allow your app
to persist even if it doesn't have any open windows. It will also hide any app-level
icon from your taskbar.

Background apps are not supported on mobile, web and console platforms.

Notes
-----

* On macOS, menus are tied to the app, not the window; and a menu is mandatory.
  Therefore, a macOS app will *always* have a menu with the default menu items,
  regardless of the window being used as the main window.

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
