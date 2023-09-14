WebView
=======

An embedded web browser.

.. figure:: /reference/images/WebView.jpeg
    :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!^(WebView|Component)$)'}

Usage
-----

.. code-block:: python

    import toga

    webview = toga.WebView()

    # Request a URL be loaded in the webview.
    webview.url = "https://beeware.org"

    # Load a URL, and wait (non-blocking) for the page to complete loading
    await webview.load_url("https://beeware.org")

    # Load static HTML content into the wevbiew.
    webview.set_content("https://example.com", "<html>...</html>")

Notes
-----

* Due to app security restrictions, WebView can only display ``http://`` and
  ``https://`` URLs, not ``file://`` URLs. To serve local file content, run a
  web server on ``localhost`` using a background thread.

* Using WebView on Windows 10 requires that your users have installed the `Edge
  WebView2 Evergreen Runtime
  <https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download-section>`__.
  This is installed by default on Windows 11.

* Using WebView on Linux requires that the user has installed the system packages
  for WebKit2, plus the GObject Introspection bindings for WebKit2.

* On macOS 13.3 (Ventura) and later, the content inspector for your app can be opened by
  running Safari, `enabling the developer tools
  <https://support.apple.com/en-au/guide/safari/sfri20948/mac>`__, and selecting your
  app's window from the "Develop" menu.

  On macOS versions prior to Ventura, the content inspector is not enabled by default,
  and is only available when your code is packaged as a full macOS app (e.g., with
  Briefcase). To enable debugging, run:

    .. code-block:: console

        $ defaults write com.example.appname WebKitDeveloperExtras -bool true

    Substituting ``com.example.appname`` with the bundle ID for your packaged app.

Reference
---------

.. autoclass:: toga.WebView
