Label
=====

A text label for annotating forms or interfaces.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/label-macOS.png
       :align: center
       :width: 300px

  .. group-tab:: Linux

    .. figure:: /reference/images/label-gtk.png
       :align: center
       :width: 300px

  .. group-tab:: Windows

    .. figure:: /reference/images/label-winforms.png
       :align: center
       :width: 300px

  .. group-tab:: Android

    .. figure:: /reference/images/label-android.png
       :align: center
       :width: 300px

  .. group-tab:: iOS

    .. figure:: /reference/images/label-ios.png
       :align: center
       :width: 300px

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!^(Label|Component)$)'}

Usage
-----

.. code-block:: python

    import toga

    label = toga.Label("Hello world")

Notes
-----

* Winforms does not support an alignment value of ``JUSTIFIED``. If this
  alignment value is used, the label will default to left alignment.

Reference
---------

.. autoclass:: toga.Label
