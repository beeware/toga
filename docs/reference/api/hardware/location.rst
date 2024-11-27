Location services
=================

A sensor that can capture the geographical location of the device.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :include: {0: '^Location$'}

Usage
-----

The location services of a device can be accessed using the
:attr:`toga.App.location` attribute. This attribute exposes an API that allows you
to check if you have have permission to access location services; if permission
exists, you can capture the current location of the device, and/or set a handler to be
notified when position changes occur.

The Location API is *asynchronous*. This means the methods that have long-running
behavior (such as requesting permissions and requesting a location) must be
``await``-ed, rather than being invoked directly. This means they must be invoked from
inside an asynchronous handler:

.. code-block:: python

    import toga

    class MyApp(toga.App):
        ...
        async def determine_location(self, widget, **kwargs):
            location = await self.location.current_location()

All platforms require some form of permission to access the location service. To
confirm if you have permission to use the location service while the app is running,
you can call :any:`Location.has_permission`; you can request permission using
:any:`Location.request_permission()`.

If you wish to track the location of the user while the app is in the background, you
must make a separate request for background location permissions using
:any:`Location.request_background_permission()` . This request must be made *after*
foreground permissions have been requested and confirmed. To confirm if you have
permission to use location while the app is in the background, you can call
:any:`Location.has_background_permission`.

Toga will confirm whether the app has been granted permission to use Location
services before invoking any location API. If permission has not yet been granted, or
if permission has been denied by the user, a :any:`PermissionError` will be raised.

To continuously track location, add an ``on_change`` handler to the location service,
then call :any:`Location.start_tracking()`. The handler will be invoked whenever a new
location is obtained:

.. code-block:: python

    class MyApp(toga.App):
        ...
        async def location_update(self, location, altitude, **kwargs):
            print(f"You are now at {location}, with altitude {altitude} meters")

        def start_location(self):
            # Install a location handler
            self.location.on_change = self.location_update
            # Start location updates. This assumes permissions have already been
            # requested and granted.
            try:
                self.location.start_tracking()
            except PermissionError:
                print("User has not permitted location tracking.")

If you no longer wish to receive location updates, call :any:`Location.stop_tracking()`.

Notes
-----

* Apps that use location services must be configured to provide permissions to access
  those services. The permissions required are platform specific:

  * iOS: ``NSLocationWhenInUseUsageDescription`` must be defined in the app's
    ``Info.plist`` file. If you want to track location while the app is in the
    background, you must also define  ``NSLocationAlwaysAndWhenInUseUsageDescription``,
    and add the ``location`` and ``processing`` values to ``UIBackgroundModes``.
  * macOS: The ``com.apple.security.personal-information.location`` entitlement must be
    enabled, and ``NSLocationUsageDescription`` must be defined in the app's
    ``Info.plist`` file.
  * Android: At least one of the permissions ``android.permission.ACCESS_FINE_LOCATION``
    or ``android.permission.ACCESS_COARSE_LOCATION`` must be declared; if only one is
    declared, this will impact on the precision available in location results. If you
    want to track location while the app is in the background, you must also define the
    permission ``android.permission.ACCESS_BACKGROUND_LOCATION``.

* On macOS and GTK, there is no distinction between "background" permissions and "while-running"
  permissions for location tracking.

* There are no permission controls for non-sandboxed GTK applications and location requests
  are always allowed by the host. Sandboxed applications (e.g., Flatpak apps) request location
  information via the XDG Portal Location API, which has coarse grained permissions.

* On iOS, if the user has provided "allow once" permission for foreground location
  tracking, requests for background location permission will be rejected.

* On Android prior to API 34, altitude is reported as the distance above the WGS84
  ellipsoid datum, rather than Mean Sea Level altitude.

Reference
---------

.. autoclass:: toga.hardware.location.Location

.. autoprotocol:: toga.hardware.location.OnLocationChangeHandler
