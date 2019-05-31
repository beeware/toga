Window
======

======= ====== ========= ===== ========= ========
 macOS   GTK+   Windows   iOS   Android   Django
======= ====== ========= ===== ========= ========
 |y|     |y|    |y|       |y|   |y|       |y|
======= ====== ========= ===== ========= ========

.. |y| image:: /_static/yes.png
    :width: 32

A window for displaying components to the user

Usage
-----

The window class is used for desktop applications, where components need to be shown within a window-manager. Windows can be configured on
instantiation and support displaying multiple widgets, toolbars and resizing.

.. code-block:: Python

    import toga


    class ExampleWindow(toga.App):
        def startup(self):
            self.label = toga.Label('Hello World')
            outer_box = toga.Box(
                children=[self.label]
            )
            self.window = toga.Window()
            self.window.content = outer_box

            self.window.show()


    def main():
        return ExampleWindow('Window', 'org.beeware.window')


    if __name__ == '__main__':
        app = main()
        app.main_loop()

Reference
---------

.. autoclass:: toga.window.Window
   :members:
   :undoc-members:
   :inherited-members:
