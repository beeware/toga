Geolocation
===========

A sensor that can capture the geographical location of the device.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(Geolocation|Hardware))'}

Usage
-----

The Geolocation services of a device can be accessed using the
:attr:`~toga.App.geolocation` attribute. This attribute exposes an API that allows you to
check if you have have permission to access geolocation services; and if permission exists,
capture the current location of the device, and set a handler to be notified when position
changes occur.

The Camera API is *asynchronous*. This means the methods that have long-running behavior
(such as requesting permissions and requesting a position) must be ``await``-ed, rather
than being invoked directly. This means they must be invoked from inside an asynchronous
handler:

.. code-block:: python

    import toga

    class MyApp(toga.App):
        ...
        async def determine_location(self, widget, **kwargs):
            location = await self.geolocation.current_location

Most platforms will require some form of device permission to access the geolocation
service. To confirm if you have permission to use the geolocation service, you can call
:any:`Geolocation.has_permission`; you can request to permission using
:any:`Geolocation.request_permission()`.

The calls to request permissions *can* be invoked from a synchronous context (i.e., a
non ``async`` method); however, they are non-blocking when used in this way. Invoking a
method like :any:`Geolocation.request_permission()` will start the process of requesting
permission, but will return *immediately*, without waiting for the user's response. This
allows an app to *request* permissions as part of the startup process, prior to using
the geolocation APIs, without blocking the rest of app startup.

Toga will confirm whether the app has been granted permission to use geolocation
services before invoking any geolocation API. If permission has not yet been granted,
the platform *may* request access at the time of the first geolocation request; however,
this is not guaranteed to be the behavior on all platforms.

Notes
-----

* Apps that use a camera must be configured to provide permission to the camera device.
  The permissions required are platform specific:

  * iOS: ``NSLocationWhenInUseUsageDescription`` must be defined in the app's
    ``Info.plist`` file. If you want to track location while the app is in the
    background, you must also define  ``NSLocationAlwaysAndWhenInUseUsageDescription``.
  * macOS: The ``com.apple.security.personal-information.location`` entitlement must be
    enabled, and ``NSLocationUsageDescription`` must be defined in the app's
    ``Info.plist`` file.
  * Android: At least one of the permissions ``android.permission.ACCESS_FINE_LOCATION``
    or ``android.permission.ACCESS_COARSE_LOCATION`` must be declared; if only one is
    declared, this will impact on the precision available in geolocation results. If you
    want to track location while the app is in the background, you must also define the
    permission ``android.permission.ACCESS_BACKGROUND_LOCATION``.

Reference
---------

.. autoclass:: toga.hardware.geolocation.Geolocation
