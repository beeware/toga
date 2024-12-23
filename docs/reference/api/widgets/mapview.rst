MapView
=======

A zoomable map that can be annotated with location pins.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/mapview-cocoa.png
       :align: center
       :width: 450px

  .. group-tab:: Linux

    .. figure:: /reference/images/mapview-gtk.png
       :align: center
       :width: 450px

  .. group-tab:: Windows

    .. figure:: /reference/images/mapview-winforms.png
       :align: center
       :width: 450px

  .. group-tab:: Android

    .. figure:: /reference/images/mapview-android.png
       :align: center
       :width: 450px

  .. group-tab:: iOS

    .. figure:: /reference/images/mapview-iOS.png
       :align: center
       :width: 450px

  .. group-tab:: Web |no|

    Not supported

  .. group-tab:: Textual |no|

    Not supported

Usage
-----

A MapView is a scrollable area that can show a map at varying levels of detail, from
nation-level to street level. The map can be centered at a given coordinate, and zoomed
to the required level of detail using an integer from 0 (for global detail) to 20
(for building level detail):

.. code-block:: python

    import toga

    # Create a map centered in London, UK.
    mapview = toga.MapView(location=(51.507222, -0.1275))

    # Center the map in Perth, Australia
    mapview.location = (-31.9559, 115.8606)

    # Zoom to show the map to show street level detail
    mapview.zoom = 15

A map can also display pins. A map pin must have a title, and can optionally have a
subtitle. Pins can be added at time of map construction, or can be dynamically added,
updated and removed at runtime:

.. code-block:: python

    import toga

    mapview = toga.MapView(
        pins=[
            toga.MapPin((-31.95064, 115.85889), title="Yagan Square"),
        ]
    )

    # Create a new pin, and add it to the map
    brutus = toga.MapPin((41.50375, -81.69475), title="Brutus was here")
    mapview.pins.add(brutus)

    # Update the pin label and position
    brutus.location = (40.440831, -79.991162)
    brutus.title = "Brutus will be here"

    # Remove the Brutus pin
    mapview.pins.remove(brutus)

    # Remove all pins
    mapview.pins.clear()

Pins can respond to being pressed. When a pin is pressed, the map generates an
``on_select`` event, which receives the pin as an argument.

.. _mapview-system-requires:

System requirements
-------------------

* Using MapView on Windows 10 requires that your users have installed the `Edge
  WebView2 Evergreen Runtime
  <https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download>`__.
  This is installed by default on Windows 11.

* Using MapView on Linux requires that the user has installed the system packages
  for WebKit2, plus the GObject Introspection bindings for WebKit2. The name of
  the system package required is distribution dependent:

  - Ubuntu 20.04; Debian 11: ``gir1.2-webkit2-4.0``
  - Ubuntu 22.04+; Debian 12+: ``gir1.2-webkit2-4.1``
  - Fedora: ``webkit2gtk4.1``
  - Arch/Manjaro: ``webkit2gtk-4.1``
  - OpenSUSE Tumbleweed: ``libwebkit2gtk3 typelib(WebKit2)``
  - FreeBSD: ``webkit2-gtk3``

* Using MapView on Android requires the OSMDroid package in your project's Gradle
  dependencies. Ensure your app declares a dependency on
  ``org\.osmdroid:osmdroid-android:6.1.20`` or later.

Notes
-----

* The Android, GTK and Winforms implementations of MapView use `OpenStreetMap
  <https://www.openstreetmap.org/about>`__ as a source of map tiles. OpenStreetMap is an
  open data project with its own `copyright, license terms, and acceptable use policies
  <https://www.openstreetmap.org/copyright>`__. If you make use of MapView in your
  application, it is your responsibility to ensure that your app complies with these
  terms. In addition, we strongly encourage you to financially support the
  `OpenStreetMap Foundation <https://osmfoundation.org>`__, as their work is what allows
  Toga to provide map content on these platforms.

* On macOS and iOS, MapView will not repeat map tiles if the viewable area at the given
  zoom level is bigger than the entire world. A zoom to a very low level will be clipped
  to the lowest level that allows displaying the map without repeating tiles.

Reference
---------

.. autoclass:: toga.MapView

.. autoclass:: toga.MapPin

.. autoclass:: toga.widgets.mapview.MapPinSet

.. autoprotocol:: toga.widgets.mapview.OnSelectHandler
