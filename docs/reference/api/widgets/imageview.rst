Image View
==========

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(ImageView|Component)$)'}

The Image View is a container for an image to be rendered on the display

Usage
-----

.. code-block:: Python

    import toga

    view = toga.ImageView(id='view1', image=my_image)

Reference
---------

.. autoclass:: toga.widgets.imageview.ImageView
   :members:
   :undoc-members:
