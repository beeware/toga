{{ component_header("Camera") }}

## Usage

Cameras attached to a device running an app can be accessed using the [`camera`][toga.App.camera] attribute. This attribute exposes an API that allows you to check if you have have permission to access the camera device; and if permission exists, capture photographs or scan barcodes.

The Camera API is *asynchronous*. This means the methods that have long-running behavior (such as requesting permissions, taking photographs, and scanning) must be `await`-ed, rather than being invoked directly. This means they must be invoked from inside an asynchronous handler:

```python
import toga

class MyApp(toga.App):
    ...
    async def time_for_a_selfie(self, widget, **kwargs):
        photo = await self.camera.take_photo()

    async def scan_qr_code(self, widget, **kwargs):
        content = await self.camera.start_scanning()
        self.label.text = f"Scanned: {content}"
```

Most platforms will require some form of device permission to access the camera. The permission APIs are paired with the specific actions performed on those APIs - that is, to take a photo or scan a barcode, you require [`Camera.has_permission`][toga.hardware.camera.Camera.has_permission], which you can request using [`Camera.request_permission()`][toga.hardware.camera.Camera.request_permission].

Toga will confirm whether the app has been granted permission to use the camera before invoking any camera API. If permission has not yet been granted, the platform *may* request access at the time of first camera access; however, this is not guaranteed to be the behavior on all platforms.

## Scanning for Barcodes

The camera can be used to scan QR codes and other barcode types in real-time. Scanning is supported on iOS, macOS, and in the Dummy (test) backend.

To scan a barcode, call [`Camera.start_scanning()`][toga.hardware.camera.Camera.start_scanning]. By default, scanning stops automatically when the first barcode is detected, and the result resolves to the content string:

```python
async def scan_once(self, widget, **kwargs):
    content = await self.camera.start_scanning()
    self.label.text = f"Found: {content}"
```

For continuous scanning (e.g., scanning multiple codes), pass `continuous=True` and provide an `on_detection` callback:

```python
async def start_continuous_scan(self, widget, **kwargs):
    self.camera.on_detection = self.on_barcode
    await self.camera.start_scanning(continuous=True)

def on_barcode(self, camera, content, **kwargs):
    self.log(f"Detected: {content}")

def stop_scan(self, widget, **kwargs):
    self.camera.stop_scanning()
```

You can specify which barcode formats to scan for using the `code_types` parameter. It accepts a single [`BarcodeFormat`][toga.constants.BarcodeFormat] value or a list:

```python
# Scan for QR codes only
content = await self.camera.start_scanning(code_types=BarcodeFormat.QR)

# Scan for multiple formats
content = await self.camera.start_scanning(
    code_types=[BarcodeFormat.QR, BarcodeFormat.CODE128],
)
```

## Notes

- Apps that use a camera must be configured to provide permission to the camera device. The permissions required are platform specific:
    - iOS: `NSCameraUsageDescription` must be defined in the app's `Info.plist` file.
    - macOS: The `com.apple.security.device.camera` entitlement must be enabled, and `NSCameraUsageDescription` must be defined in the app's `Info.plist` file.
    - Android: The `android.permission.CAMERA` permission must be declared.
- The iOS simulator implements the iOS Camera APIs, but is not able to take photographs or scan barcodes. To test your app's Camera usage, you must use a physical iOS device.
- Barcode scanning is currently available on iOS, macOS, and in the Dummy (test) backend. Other backends will raise `NotImplementedError`.

## Reference

::: toga.hardware.camera.Camera

::: toga.hardware.camera.CameraDevice

::: toga.hardware.camera.ScanResult

::: toga.constants.BarcodeFormat
