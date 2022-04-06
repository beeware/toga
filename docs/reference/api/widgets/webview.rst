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

The Web View widget is used for displaying an embedded browser window within an application.

Both sites served by a web server and local content can be displayed. Due to security
restrictions in the macOS backend WKWebView, local content on macOS can only be loaded
from a single directory, relative to the base URL, and not from an absolute "file://" URL.
As a workaround, it is possible to use a lightweight webserver instead.

.. figure:: /reference/images/WebView.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga

    web = toga.WebView(url='https://google.com')

Debugging
---------

If you need to debug the HTML, JavaScript or CSS content of a view, you may want
to use the "inspect element" feature of the WebView. This is not be turned on by
default on some platforms. To enable WebView debugging:

* macOS

    Run the following at the terminal::

        $ defaults write com.example.appname WebKitDeveloperExtras -bool true

    substituting `com.example.appname` with the bundle ID for your app.


Reference
---------

.. autoclass:: toga.widgets.webview.WebView
   :members:
   :undoc-members:
   :inherited-members:
