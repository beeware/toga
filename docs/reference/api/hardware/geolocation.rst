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
:attr:`~toga.App.geolocation` attribute. This attribute exposes an API that allows you
to check if you have have permission to access geolocation services; if permission
exists, you can capture the current location of the device, and/or set a handler to be
notified when position changes occur.

The Geolocation API is *asynchronous*. This means the methods that have long-running
behavior (such as requesting permissions and requesting a location) must be
``await``-ed, rather than being invoked directly. This means they must be invoked from
inside an asynchronous handler:

.. code-block:: python

    import toga

    class MyApp(toga.App):
        ...
        async def determine_location(self, widget, **kwargs):
            location = await self.geolocation.current_location()

All platforms require some form of permission to access the geolocation service. To
confirm if you have permission to use the geolocation service while the app is running,
you can call :any:`Geolocation.has_permission`; you can request to permission using
:any:`Geolocation.request_permission()`. To confirm if you have permission to use
geolocation while the app is in the background, you can call
:any:`Geolocation.has_background_permission`; you can request to permission using
:any:`Geolocation.request_background_permission()`

The calls to request permissions *can* be invoked from a synchronous context (i.e., a
non ``async`` method); however, they are non-blocking when used in this way. Invoking a
method like :any:`Geolocation.request_permission()` will start the process of requesting
permission, but will return *immediately*, without waiting for the user's response. This
allows an app to *request* permissions as part of the startup process, prior to using
the geolocation APIs, without blocking the rest of app startup.

Toga will confirm whether the app has been granted permission to use geolocation
services before invoking any geolocation API. If permission has not yet been granted, or
if permission has been denied by the user, a :any:`PermissionError` will be raised.

To continuously track location, add an ``on_change`` handler to the geolocation service,
then call :any:`Geolocation.start()`. The handler will be invoked whenever a new
geolocation position is obtained:

.. code-block:: python

    class MyApp(toga.App):
        ...
        async def location_update(self, location, altitude, **kwargs):
            print(f"You are now at {location}, with altitude {altitude} meters")

        def start_geolocation(self):
            # Install a geolocation handler
            self.geolocation.on_change = self.location_update
            # Start location updates. This assumes permissions have already been
            # requested and granted.
            try:
                self.geolocation.start()
            except PermissionError:
                print("User has not permitted geolocation.")

If you no longer wish to receive geolocation updates, call :any:`Geolocation.stop()`.

Notes
-----

* Apps that use a camera must be configured to provide permission to the camera device.
  The permissions required are platform specific:

  * iOS: ``NSLocationWhenInUseUsageDescription`` must be defined in the app's
    ``Info.plist`` file. If you want to track location while the app is in the
    background, you must also define  ``NSLocationAlwaysAndWhenInUseUsageDescription``,
    and add the ``location`` and ``processing`` values to ``UIBackgroundModes``.
  * macOS: The ``com.apple.security.personal-information.location`` entitlement must be
    enabled, and ``NSLocationUsageDescription`` must be defined in the app's
    ``Info.plist`` file.
  * Android: At least one of the permissions ``android.permission.ACCESS_FINE_LOCATION``
    or ``android.permission.ACCESS_COARSE_LOCATION`` must be declared; if only one is
    declared, this will impact on the precision available in geolocation results. If you
    want to track location while the app is in the background, you must also define the
    permission ``android.permission.ACCESS_BACKGROUND_LOCATION``.

* On macOS, there is no distinction between "background" permissions and "while-running"
  permissions.

* On iOS, requesting permission to track location in the background will always require
  2 interactions from the user - an initial request to use geolocation while the app is
  running, then a second request to use location in the background. If you call
  :meth:`~toga.hardware.Geolocation.request_background_permission()` before *any*
  permissions have been confirmed, the user will be asked immediately for geolocation
  permissions while the app is running; the request for background tracking will be
  deferred until the first attempt to use location in the background, or a second call
  to :meth:`~toga.hardware.Geolocation.request_background_permission()`. Background
  location tracking will not be permitted unless the user allows geolocation "always"
  while the app is running. If they only allow "once off" permission while the app is
  running, requests for background processing will be ignored.

Reference
---------

.. autoclass:: toga.hardware.geolocation.Geolocation
