Scroll Container
================

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(ScrollContainer|Component))'}

The Scroll Container is similar to the ``iframe`` or scrollable ``div`` element in HTML, it contains an object with
its own scrollable selection.

.. figure:: /reference/images/ScrollContainer.jpeg
    :align: center

Usage
-----

.. code-block:: python

    import toga

    content = toga.WebView()

    container = toga.ScrollContainer(content=content)

Scroll settings
---------------

Horizontal or vertical scroll can be set via the initializer or using the property.

.. code-block:: python

    import toga

    content = toga.WebView()

    container = toga.ScrollContainer(content=content, horizontal=False)

    container.vertical = False

Reference
---------

.. autoclass:: toga.ScrollContainer
   :members:
   :undoc-members:
