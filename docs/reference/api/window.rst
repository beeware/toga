Window
======

.. rst-class:: widget-support
.. csv-filter::
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(Window|Component))'}

.. |y| image:: /_static/yes.png
    :width: 16

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
