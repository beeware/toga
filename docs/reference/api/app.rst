Application
===========

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(Application|Component))'}

The app is the main entry point and container for the Toga GUI.

Usage
-----

The app class is used by instantiating with a name, namespace and callback to a startup delegate which takes 1 argument of the app instance.

To start a UI loop, call ``app.main_loop()``

.. code-block:: python

    import toga


    def build(app):
        # build UI
        pass


    if __name__ == '__main__':
        app = toga.App('First App', 'org.beeware.helloworld', startup=build)
        app.main_loop()

Alternatively, you can subclass App and implement the startup method

.. code-block:: python

    import toga


    class MyApp(toga.App):
        def startup(self):
            # build UI
            pass


    if __name__ == '__main__':
        app = MyApp('First App', 'org.beeware.helloworld')
        app.main_loop()

All App instances must have assigned their :attr:`~toga.App.main_window` before the
conclusion of their :meth:`~toga.App.startup` method.

Reference
---------

.. autoclass:: toga.App

.. autoprotocol:: toga.app.AppStartupMethod
.. autoprotocol:: toga.app.BackgroundTask
.. autoprotocol:: toga.app.OnExitHandler
