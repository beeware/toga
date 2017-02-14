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

Reference
---------

.. autoclass:: toga.interface.app.App
   :members:
   :undoc-members:
   :inherited-members: