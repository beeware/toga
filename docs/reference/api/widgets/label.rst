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

  .. group-tab:: Web |beta|

    .. figure:: /reference/images/label-macOS.png
       :align: center
       :width: 300px

  .. group-tab:: Textual |beta|

    .. figure:: /reference/images/label-textual.png
       :align: center
       :width: 300px

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
