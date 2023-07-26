Window
======

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(Window|Component))'}

A window for displaying components to the user

Usage
-----

The window class is used for desktop applications, where components need to be shown within a window-manager. Windows can be configured on
instantiation and support displaying multiple widgets, toolbars and resizing.

.. code-block:: python

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

.. autoclass:: toga.Window
   :members:
   :undoc-members:

.. autoprotocol:: toga.window.OnCloseHandler
.. autoprotocol:: toga.window.DialogResultHandler
