Scroll Container
================

======= ====== ========= ===== ========= ========
 macOS   GTK+   Windows   iOS   Android   Django
======= ====== ========= ===== ========= ========
 |y|     |y|    |y|      |y|
======= ====== ========= ===== ========= ========

.. |y| image:: /_static/yes.png
    :width: 16

The Scroll Container is similar to the iframe or scrollable div element in HTML, it contains an object with
its own scrollable selection.

.. figure:: /reference/images/ScrollContainer.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga

    content = toga.WebView()

    container = toga.ScrollContainer(content=content)

Scroll settings
---------------

Horizontal or vertical scroll can be set via the initializer or using the property.

.. code-block:: Python

    import toga

    content = toga.WebView()

    container = toga.ScrollContainer(content=content, horizontal=False)

    container.vertical = False

Reference
---------

.. autoclass:: toga.widgets.scrollcontainer.ScrollContainer
   :members:
   :undoc-members:
   :inherited-members:
