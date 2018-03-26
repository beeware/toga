WebView
=======

======= ====== ========= ===== ========= ========
 macOS   GTK+   Windows   iOS   Android   Django
======= ====== ========= ===== ========= ========
 |y|     |y|    |y|       |y|             |y|
======= ====== ========= ===== ========= ========

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
