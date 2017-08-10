:orphan:

.. warnings about this file not being included in any toctree will be suppressed by :orphan:

Web View
========

The Web View widget is used for displaying an embedded browser window within an application

.. figure:: /reference/images/WebView.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga

    web = toga.WebView(url='https://google.com')

Supported Platforms
-------------------

.. include:: ../supported_platforms/WebView.rst

Reference
---------

.. autoclass:: toga.widgets.webview.WebView
   :members:
   :undoc-members:
   :inherited-members: