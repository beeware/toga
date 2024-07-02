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
:attr:`~toga.App.main_window` for the app. The possible values are :ref:`discussed
below <assigning-main-window>`; most apps will assign an instance of
:any:`toga.MainWindow`:

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
automatically exit. Attempting to close the last window will trigger any app-level
:meth:`~toga.App.on_exit` handling in addition to any window-specific
:meth:`~toga.Window.on_close` handling.

Mobile, web and console platforms *must* define a main window.

:attr:`~toga.App.BACKGROUND`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assigning a value of :attr:`toga.App.BACKGROUND` as the main window will allow your app
to persist even if it doesn't have any open windows. It will also hide any app-level
icon from your taskbar.

Background apps are not supported on mobile, web and console platforms.

Life cycle of an app
--------------------

Regardless of what an application does, every application goes through the same
life cycle of starting, running, and shutting down.

Application startup is handled by the :meth:`~toga.App.startup` method described above.
:meth:`~toga.App.startup` *cannot* be an asynchronous method, as it runs *before* the
App's event loop is started.

All other events in the life cycle of the app can be managed with event handlers.
:class:`toga.App` defines the following event handlers:

* :meth:`~toga.App.on_running` occurs as soon as the app's event loop has started.

* :meth:`~toga.App.on_exit` occurs when the user tries to exit. The handler for this
  event must return a Boolean value: ``True`` if the app is allowed to exit; ``False``
  otherwise. This allows an app to abort the exit process (for example, to prevent exit
  if there are unsaved changes).

Event handlers can be defined by subclassing :class:`toga.App` and overriding the event
handler method, by assigning a value to the event handler when the app instance is
constructed, or by assigning the event handler attribute on an existing app instance.
When the event handler is set by assigning a value to the event handler, the handler
method must accept an ``app`` argument. This argument is not required when subclassing,
as the app instance can be implied. Regardless of how they are defined, event handlers
*can* be defined as ``async`` methods.

Managing documents
------------------

When you create an App instance, you can declare the type of documents that your app is
able to manage by providing a value for ``document_types``. When an app declares that it
can manage document types, the app will automatically create file management menu items
(such as New, Open and Save), and the app will process command line arguments, creating
a :class:`toga.Document` instance for each argument matching a registered document type.

For details on how to define and register document types, refer to :doc:`the
documentation on document handling <./resources/document>`.

System-installed commands
-------------------------

Every app install a collection of default :ref:`commands`, reflecting basic app
operations like quitting the app, displaying an About dialog, and so on. These commands
are all backed by default implementations on :class:`toga.App`. You can alter the default
Toga behavior by overriding these methods.

The commands installed by default is dependent on platform requirements. For example,
mobile apps won't install an :attr:`~toga.Command.EXIT` command because mobile apps
don't usually provide an in-app way to quit the app.

If your app :ref:`registers at least one document type <registering-document-types>`,
the system-installed commands will include all file management commands (New, Open,
Save, etc). These commands use the :class:`toga.Document` API to save the content
managed by your app.

The system-installed commands are also affected by the methods defined by your app. For
example, the preferences menu item will only be installed if your app overrides
:meth:`~toga.App.preferences`. The file management commands can also be installed by
overriding the corresponding methods in your app; overriding the :meth:`~toga.App.save`
method will enable the Save menu item; overriding the :meth:`~toga.App.open` method will
enable the Open menu item, and so on.

The system-installed commands will all be installed *before* your app's
:meth:`~toga.App.startup` method is invoked. If you wish to remove a menu item that has
been installed by default, you delete the command from your app's
:attr:`~toga.App.commands` set, using the :attr:`~toga.Command.id` attribute of the
command. For example, to remove the About menu item that is installed by default you
would add the following to your app's startup method:

.. code-block:: python

    def startup(self):
        del self.commands[toga.Command.ABOUT]

        # Other startup logic
        ...

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
.. autoprotocol:: toga.app.OnRunningHandler
.. autoprotocol:: toga.app.OnExitHandler
