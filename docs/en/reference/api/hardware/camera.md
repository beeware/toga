{{ component_header("Camera") }}

## Usage

Cameras attached to a device running an app can be accessed using the [`camera`][toga.App.camera] attribute. This attribute exposes an API that allows you to check if you have have permission to access the camera device; and if permission exists, capture photographs.

The Camera API is *asynchronous*. This means the methods that have long-running behavior (such as requesting permissions and taking photographs) must be `await`-ed, rather than being invoked directly. This means they must be invoked from inside an asynchronous handler:

```python
import toga

class MyApp(toga.App):
    ...
    async def time_for_a_selfie(self, widget, **kwargs):
        photo = await self.camera.take_photo()
```

Most platforms will require some form of device permission to access the camera. The permission APIs are paired with the specific actions performed on those APIs - that is, to take a photo, you require [`Camera.has_permission`][toga.hardware.camera.Camera.has_permission], which you can request using [`Camera.request_permission()`][toga.hardware.camera.Camera.request_permission].

Toga will confirm whether the app has been granted permission to use the camera before invoking any camera API. If permission has not yet been granted, the platform *may* request access at the time of first camera access; however, this is not guaranteed to be the behavior on all platforms.

## Notes

- Apps that use a camera must be configured to provide permission to the camera device. The permissions required are platform specific:
    - iOS: `NSCameraUsageDescription` must be defined in the app's `Info.plist` file.
    - macOS: The `com.apple.security.device.camera` entitlement must be enabled, and `NSCameraUsageDescription` must be defined in the app's `Info.plist` file.
    - Android: The `android.permission.CAMERA` permission must be declared.
- The iOS simulator implements the iOS Camera APIs, but is not able to take photographs. To test your app's Camera usage, you must use a physical iOS device.

## Reference

::: toga.hardware.camera.Camera

::: toga.hardware.camera.CameraDevice
