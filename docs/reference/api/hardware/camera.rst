Camera
======

A sensor that can capture photos and/or video.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(Camera|Hardware))'}

Usage
-----

Cameras attached to a device running an app can be accessed using the
:attr:`~toga.App.camera` attribute. This attribute exposes an API that allows you to
check if you have have permission to access the camera device; and if permission exists,
capture photographs.

The Camera API is *asynchronous*. This means the methods that have long-running behavior
(such as requesting permissions and taking photographs) must be ``await``-ed, rather
than being invoked directly. This means they must be invoked from inside an asynchronous
handler:

.. code-block:: python

    import toga

    class MyApp(toga.App):
        ...
        async def time_for_a_selfie(self, widget, **kwargs):
            photo = await self.camera.take_photo()

Most platforms will require some form of device permission to access the camera. The
permission APIs are paired with the specific actions performed on those APIs - that is,
to take a photo, you require :any:`Camera.has_permission`, which you can request using
:any:`Camera.request_permission()`.

The calls to request permissions *can* be invoked from a synchronous context (i.e., a
non ``async`` method); however, they are non-blocking when used in this way. Invoking a
method like :any:`Camera.request_permission()` will start the process of requesting
permission, but will return *immediately*, without waiting for the user's response. This
allows an app to *request* permissions as part of the startup process, prior to using
the camera APIs, without blocking the rest of app startup.

Toga will confirm whether the app has been granted permission to use the camera before
invoking any camera API. If permission has not yet been granted, the platform *may*
request access at the time of first camera access; however, this is not guaranteed to be
the behavior on all platforms.

Notes
-----

* Apps that use a camera must be configured to provide permission to the camera device.
  The permissions required are platform specific:

  * iOS: ``NSCameraUsageDescription`` must be defined in the app's ``Info.plist`` file.
  * macOS: The ``com.apple.security.device.camera`` entitlement must be enabled.
  * Android: The ``android.permission.CAMERA`` permission must be declared.

* The iOS simulator implements the iOS Camera APIs, but is not able to take photographs.
  To test your app's Camera usage, you must use a physical iOS device.

Reference
---------

.. autoclass:: toga.hardware.camera.Camera

.. autoclass:: toga.hardware.camera.CameraDevice
