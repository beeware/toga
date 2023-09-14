ScrollContainer
===============

A container that can display a layout larger than the area of the container, with
overflow controlled by scroll bars.

.. figure:: /reference/images/ScrollContainer.png
   :align: center
   :width: 300px

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(ScrollContainer|Component))'}

Usage
-----

.. code-block:: python

    import toga

    content = toga.Box(children=[...])

    container = toga.ScrollContainer(content=content)

Reference
---------

.. autoclass:: toga.ScrollContainer
   :exclude-members: window, app
