App
===

The top-level representation of an application.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(Application|Component))'}


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

Reference
---------

.. autoclass:: toga.App
    :exclude-members: app

.. autoprotocol:: toga.app.AppStartupMethod
.. autoprotocol:: toga.app.BackgroundTask
.. autoprotocol:: toga.app.OnExitHandler
