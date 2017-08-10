:orphan:

.. warnings about this file not being included in any toctree will be suppressed by :orphan:

Application
===========

The app is the main entry point and container for the Toga GUI.

Usage
-----

The app class is used by instantiating with a name, namespace and callback to a startup delegate which takes 1 argument of the app instance.

To start a UI loop, call `app.main_loop()`

.. code-block:: Python

    import toga


    def build(app):
        # build UI
        pass


    if __name__ == '__main__':
        app = toga.App('First App', 'org.pybee.helloworld', startup=build)
        app.main_loop()

Alternatively, you can subclass App and implement the startup method

.. code-block:: Python

    import toga


    class MyApp(toga.App):
        def startup(self):
            # build UI
            pass


    if __name__ == '__main__':
        app = MyApp('First App', 'org.pybee.helloworld', startup=build)
        app.main_loop()


Supported Platforms
-------------------

.. include:: ../supported_platforms/App.rst

Reference
---------

.. autoclass:: toga.app.App
   :members:
   :undoc-members:
   :inherited-members: