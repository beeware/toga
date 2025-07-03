==================
Debugging Your App
==================

Debugging is helpful tool in app development. Toga provides debugging options.

Debugging Widget Layout
=======================

The debug layout colors tool is designed to give all containers distinct colors, which enables you to better see what might be happening with the layout, and more easily debug problems with it.

Enabling the tool can be done two ways. You can enable it by setting the ``TOGA_DEBUG_LAYOUT`` environment variable equal to ``1``, which lets you use it even for code you can't or don't want to alter. Setting environment variables varies by operating system. Alternatively, you can enable it from within your code by including the following in your app file or your ``app.py``:

.. code-block:: python

    import os

    DEBUG_LAYOUT_ENABLED = os.environ.get("TOGA_DEBUG_LAYOUT") == "1"

Debug layout colors with the ``toga-demo``
-------------------------------------------

To use the debug layout with the ``toga-demo``, set the environment variable, and :doc:`install and run the demo <../tutorial/get-started>`.

You should see the following.

.. image:: ../images/toga-demo-debug-layout-enabled.png

If a box or other widget expands to fill its entire parent, you won't see the parent widget behind it. The ``toga-demo`` contains two hidden widgets, and so it only shows two colors.

Debug layout colors enabled in code
-----------------------------------

This example uses a series of nested boxes to show a variety of available colors. The tool is enabled here in the code. Save the following as a Python file on your computer.

.. code-block:: python

    import os

    import toga

    DEBUG_LAYOUT_ENABLED = os.environ.get("TOGA_DEBUG_LAYOUT") == "1"

    class DebugLayoutColors(toga.App):
        def startup(self):
            main_box = toga.Box()
            prev_box = main_box
            for _ in range(1, 12):
                new_box = toga.Box(margin=30)
                prev_box.add(new_box)
                prev_box = new_box

            self.main_window = toga.MainWindow(content=main_box)
            self.main_window.show()

    def main():
        return DebugLayoutColors("Debug Layout Colors Demo", "org.beeware.toga.debug.layout")

    if __name__ == "__main__":
    main().main_loop()

When you run the file, you should see the following.

.. image:: ../images/concentric-boxes-debug-layout-enabled.png
