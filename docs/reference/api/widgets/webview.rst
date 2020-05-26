WebView
=======

.. rst-class:: widget-support
.. csv-filter::
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(WebView|Component)$)'}

.. |y| image:: /_static/yes.png
    :width: 16

The Web View widget is used for displaying an embedded browser window within an application

.. figure:: /reference/images/WebView.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga

    web = toga.WebView(url='https://google.com')

Reference
---------

.. autoclass:: toga.widgets.webview.WebView
   :members:
   :undoc-members:
   :inherited-members:
