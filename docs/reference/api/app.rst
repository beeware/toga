App
===

The top-level representation of an application.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(Application))', 1:'(?!(Core Component))'}


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
:meth:`~toga.App.startup()`. This implementation must assign a ``main_window`` for the
app.

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

Assigning a main window
-----------------------

An app *must* assign ``main_window`` as part of the startup process. However, the value
that is assigned as the main window will affect the behavior of the app.

Normal app
~~~~~~~~~~

The most common type of app will assign a :any:`toga.MainWindow` instance as the main
window. On platforms that have menu bars inside their windows, this will create a main
window with a menu bar, populated with the default app commands. The window assigned as
the main window will have its title set to the formal name of the app. A
:any:`toga.MainWindow` may also have a toolbar. When the main window is closed, the app
will exit.

This is the type of app that will be created if you use an instance of :any:`toga.App`
passing in a `startup` argument to the constructor.

Simple app
~~~~~~~~~~

To create an app that *doesn't* have these default menu items, you can assign an
instance of :any:`toga.Window` as the main window. A :any:`toga.Window` does not have a
menu bar; and as a result, neither will your app. As with a normal app, the window
assigned as the main window will have its title set to the formal name of the app; and
when the main window is closed, the app will exit.

.. _session-based-app:

Session-based app
~~~~~~~~~~~~~~~~~

A session-based app is an app that doesn't have a single "main" window. Instead, the app
will have a number of windows, with each window corresponding to a "session" of
interaction with the app. This session might be a editing a single document; or it could
be a particular view of data - web browsers or file browsers would be examples of
session-based apps, with each window representing a view of a URL, or a view of the
file system.

To define a session-based app, you assign a value of ``None`` as the main window. You can
then create new windows as required by your app.

The exact behavior of a session-based app is slightly different on each platform,
reflecting platform differences.

macOS
^^^^^

On macOS, there is only ever a single instance of an App running at any given time. That
instance can manage multiple documents. If you use the Finder to open a second document
of a type managed by the app, it will be opened in the existing app instance. Closing
all documents will not cause the app to exit; the app will keep executing until
explicitly exited.

If the app is started without an explicit file reference (e.g., by specifying a filename
at the command line, or dragging a file onto the app's icon), a file dialog will be
displayed prompting the user to select a file to open. If this dialog is dismissed, the
app will continue running. Selecting "Open" from the file menu will also display this
dialog. If a file is selected, a new document window will be opened.

Linux/Windows
^^^^^^^^^^^^^

On Linux and Windows, a single app instance app can also manage multiple open documents;
however when the last document being managed by an app instance is closed, the app
instance will exit. If the App is started without an explicit file reference, an empty
document of the default document type will be opened.

Background app
~~~~~~~~~~~~~~

To create an app without *any* main window, assign ``toga.BACKGROUND`` as the main
window. This will allow your app to persist even if it doesn't have any open windows. It
will also hide any app-level icon from your taskbar.

Document type handling
----------------------

.. TODO: Describe document types, open/save/save_as/save_all interface

Notes
-----

* On macOS, menus are tied to the app, not the window; and a menu is mandatory.
  Therefore, a minimal macOS app (i.e., an app using a :any:`toga.Window` as the main
  window) will still have a menu, but it will only have the bare minimum of menu items.

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
