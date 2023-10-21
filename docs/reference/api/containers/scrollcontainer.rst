ScrollContainer
===============

A container that can display a layout larger than the area of the container, with
overflow controlled by scroll bars.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/scrollcontainer-macOS.png
       :align: center
       :width: 450px

  .. group-tab:: Linux

    .. figure:: /reference/images/scrollcontainer-gtk.png
       :align: center
       :width: 450px

  .. group-tab:: Windows

    .. figure:: /reference/images/scrollcontainer-winforms.png
       :align: center
       :width: 450px

  .. group-tab:: Android

    .. figure:: /reference/images/scrollcontainer-android.png
       :align: center
       :width: 450px

  .. group-tab:: iOS

    .. figure:: /reference/images/scrollcontainer-iOS.png
       :align: center
       :width: 450px


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
