App
===

The top-level representation of an application.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(Application|Component))'}


Usage
-----

The App class is the top level representation of all application activity. It is a
singleton object - any given process can only have a single Application. That
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

When creating an app, you must provide a formal name (a human readable name for the
app), and an App ID (a machine-readable identifier - usually a reversed domain name).
You can provide these details as explicit arguments; however, you can also provide these
details as PEP621 packaging metadata using the ``Formal-Name`` and ``App-ID`` keys. If
you deploy your app with `Briefcase <https://briefcase.readthedocs.io/en/stable>`__,
this metadata will be populated as part of the deployment process.

A Toga app also has an app name; this is a `PEP508
<https://peps.python.org/pep-0508/#names>`__ module identifier for the app. The app name
can be provided explicitly; however, if it isn't provided explicitly, Toga uses the
following strategy to determine an app name:

1. If an app name has been explicitly provided, it will be used as-is.
2. If no app name has been explicitly provided, Toga will look for the name of the
   parent of the ``__main__`` module for the app.
3. If there is no ``__main__`` module, but an App ID has been explicitly provided, the
   last name part of the App ID will be used. For example, an explicit App ID of
   ``com.example.my-app`` would yield an app name of ``my-app``.
4. As a last resort, Toga will use the name ``toga`` as an app name.

Toga will attempt to load an :class:`~toga.Icon` for the app. If an icon is not
specified when the App instance is created, Toga will attempt to use ``resources/<app
name>`` as the name of the icon (for whatever app name has been provided or derived). If
no resource matching this name can be found, a warning will be printed, and the app will
fall back to a default icon.

Reference
---------

.. autoclass:: toga.App
   :members:
   :undoc-members:

.. autoclass:: toga.app.WindowSet
   :members:
   :undoc-members:

.. autoprotocol:: toga.app.AppStartupMethod
.. autoprotocol:: toga.app.BackgroundTask
.. autoprotocol:: toga.app.OnExitHandler
