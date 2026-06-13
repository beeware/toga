import pytest

import toga
from toga.constants import BarcodeFormat, FlashMode
from toga.hardware.camera import CameraDevice
from toga.platform import get_factory
from toga_dummy.hardware.camera import (
    Camera as DummyCamera,
    CameraDevice as DummyCameraDevice,
)
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)


@pytest.fixture
def photo(app):
    return toga.Image("resources/photo.png")


def test_no_camera(monkeypatch, app):
    """If there's no camera, and no factory implementation, accessing camera raises an
    exception."""
    factory = get_factory()
    try:
        monkeypatch.delattr(app, "_camera")
    except AttributeError:
        pass
    monkeypatch.delitem(factory._entrypoints, "Camera")

    # Accessing the camera object should raise NotImplementedError
    with pytest.raises(NotImplementedError):
        _ = app.camera


@pytest.mark.parametrize(
    "initial, should_request, has_permission",
    [
        (-1, True, True),
        (0, True, False),
        (1, False, True),
    ],
)
def test_request_permission(app, initial, should_request, has_permission):
    """An app can request permission to use the camera."""
    # The camera instance round-trips the app instance
    assert app.camera.app == app

    # Set initial permission
    app.camera._impl._has_permission = initial

    assert (
        app.loop.run_until_complete(app.camera.request_permission()) == has_permission
    )

    if should_request:
        assert_action_performed(app.camera, "request permission")
    else:
        assert_action_not_performed(app.camera, "request permission")

    # As a result of requesting, photo permission is as expected
    assert app.camera.has_permission == has_permission


def test_request_permission_sync(app):
    """An app can synchronously request permission to use the camera."""
    # Set initial permission
    app.camera._impl._has_permission = -1

    result = app.camera.request_permission()

    # This will cause a permission request to occur...
    assert_action_performed(app.camera, "request permission")

    # ... but the result won't be directly comparable (to anything)
    with pytest.raises(RuntimeError):
        _ = result == 1


def test_device_properties(app):
    """Device properties can be checked."""

    assert [
        {
            "device": device,
            "__repr__": repr(device),
            "__str__": str(device),
            "name": device.name,
            "id": device.id,
            "has_flash": device.has_flash,
        }
        for device in app.camera.devices
    ] == [
        {
            "device": CameraDevice(DummyCamera.CAMERA_1),
            "__repr__": "<CameraDevice id=camera-1 'Camera 1'>",
            "__str__": "Camera 1",
            "name": "Camera 1",
            "id": "camera-1",
            "has_flash": True,
        },
        {
            "device": CameraDevice(DummyCamera.CAMERA_2),
            "__repr__": "<CameraDevice id=camera-2 'Camera 2'>",
            "__str__": "Camera 2",
            "name": "Camera 2",
            "id": "camera-2",
            "has_flash": False,
        },
    ]

    # Identity check
    assert CameraDevice(DummyCamera.CAMERA_1) == CameraDevice(DummyCamera.CAMERA_1)
    # A different instance with the same ID is equal
    duplicate = CameraDevice(
        DummyCameraDevice(id="camera-1", name="Duplicate Camera 1", has_flash=True)
    )
    assert CameraDevice(DummyCamera.CAMERA_1) == duplicate
    # Different cameras aren't equal
    assert CameraDevice(DummyCamera.CAMERA_1) != CameraDevice(DummyCamera.CAMERA_2)


@pytest.mark.parametrize(
    "device",
    [None, CameraDevice(DummyCamera.CAMERA_1), CameraDevice(DummyCamera.CAMERA_2)],
)
@pytest.mark.parametrize(
    "flash",
    [FlashMode.AUTO, FlashMode.ON, FlashMode.OFF],
)
def test_take_photo_with_permission(app, device, flash, photo):
    """If permission has not been previously requested, it is requested before a photo
    is taken."""
    # Set permission to potentially allowed
    app.camera._impl._has_permission = -1

    app.camera._impl.simulate_photo(photo)

    result = app.loop.run_until_complete(
        app.camera.take_photo(device=device, flash=flash)
    )

    # Photo was returned
    assert result == photo

    assert_action_performed(app.camera, "has permission")
    assert_action_performed_with(
        app.camera,
        "take photo",
        permission_requested=True,
        device=device,
        flash=flash,
    )


def test_take_photo_prior_permission(app, photo):
    """If permission has been previously requested, a photo can be taken."""
    # Set permission
    app.camera._impl._has_permission = 1

    # Simulate the camera response
    app.camera._impl.simulate_photo(photo)

    result = app.loop.run_until_complete(app.camera.take_photo())

    # Photo was returned
    assert result == photo

    assert_action_performed(app.camera, "has permission")
    assert_action_performed_with(
        app.camera,
        "take photo",
        permission_requested=False,
        device=None,
        flash=FlashMode.AUTO,
    )


def test_take_photo_no_permission(app, photo):
    """If permission has been denied, an exception is raised."""
    # Deny permission
    app.camera._impl._has_permission = 0

    with pytest.raises(
        PermissionError,
        match=r"App does not have permission to take photos",
    ):
        app.loop.run_until_complete(app.camera.take_photo())

    assert_action_performed(app.camera, "has permission")
    assert_action_not_performed(app.camera, "take photo")


##########################################################################
# Scanning API
##########################################################################


def test_is_scanning_initial(app):
    """is_scanning is False before any scan starts."""
    assert app.camera.is_scanning is False
    assert_action_performed(app.camera, "is scanning")


def test_on_detection_default_none(app):
    """on_detection is a no-op by default."""
    assert app.camera.on_detection._raw is None


def test_on_detection_set_and_get(app):
    """on_detection can be set and retrieved."""

    def handler(camera, **kwargs):
        pass

    app.camera.on_detection = handler
    assert app.camera.on_detection._raw is handler


def test_start_scanning_with_permission(app):
    """Start scanning with default mode (auto-stop on first detection)."""
    app.camera._impl._has_permission = -1
    app.camera._impl.simulate_scan("QR_CODE_CONTENT")

    result = app.loop.run_until_complete(app.camera.start_scanning())

    assert result == "QR_CODE_CONTENT"
    assert_action_performed(app.camera, "has permission")
    assert_action_performed_with(
        app.camera,
        "start scanning",
        permission_requested=True,
        device=None,
        code_types=list(BarcodeFormat),
        continuous=False,
    )


def test_start_scanning_with_device(app):
    """Start scanning with a specific device."""
    app.camera._impl._has_permission = 1
    app.camera._impl.simulate_scan("content")

    device = CameraDevice(DummyCamera.CAMERA_2)
    result = app.loop.run_until_complete(app.camera.start_scanning(device=device))

    assert result == "content"
    assert_action_performed_with(
        app.camera,
        "start scanning",
        device=device,
    )


def test_start_scanning_with_code_types(app):
    """Start scanning with specific code types."""

    app.camera._impl._has_permission = 1
    app.camera._impl.simulate_scan("content")

    result = app.loop.run_until_complete(
        app.camera.start_scanning(code_types=[BarcodeFormat.QR])
    )

    assert result == "content"
    assert_action_performed_with(
        app.camera,
        "start scanning",
        code_types=[BarcodeFormat.QR],
    )


def test_start_scanning_all_code_types(app):
    """All declared BarcodeFormat values can be used for scanning."""
    app.camera._impl._has_permission = 1
    app.camera._impl.simulate_scan("all_types")

    all_types = list(BarcodeFormat)
    result = app.loop.run_until_complete(
        app.camera.start_scanning(code_types=all_types)
    )

    assert result == "all_types"
    assert_action_performed_with(
        app.camera,
        "start scanning",
        code_types=all_types,
    )


def test_start_scanning_prior_permission(app):
    """If permission was already granted, scan starts without requesting."""
    app.camera._impl._has_permission = 1
    app.camera._impl.simulate_scan("scanned data")

    result = app.loop.run_until_complete(app.camera.start_scanning())

    assert result == "scanned data"
    assert_action_performed_with(
        app.camera,
        "start scanning",
        permission_requested=False,
    )


def test_start_scanning_no_permission(app):
    """If permission has been denied, start_scanning raises PermissionError."""
    app.camera._impl._has_permission = 0

    with pytest.raises(
        PermissionError,
        match=r"App does not have permission to take photos",
    ):
        app.loop.run_until_complete(app.camera.start_scanning())

    assert_action_performed(app.camera, "has permission")
    assert_action_not_performed(app.camera, "start scanning")


def test_start_scanning_continuous(app):
    """In continuous mode, scanning continues until stop_scanning is called."""
    app.camera._impl._has_permission = 1

    detected = []

    def on_detected(camera, content, **kwargs):
        detected.append(content)

    app.camera._impl.simulate_scan("first")
    result = app.camera.start_scanning(continuous=True, on_detection=on_detected)
    assert_action_performed_with(
        app.camera,
        "start scanning",
        continuous=True,
    )

    assert detected == ["first"]

    app.camera._impl.simulate_scan("second")
    assert detected == ["first", "second"]

    app.camera.stop_scanning()
    assert_action_performed(app.camera, "stop scanning")

    assert app.loop.run_until_complete(result) is None


def test_stop_scanning(app):
    """stop_scanning ends scanning and resolves the scan result with None."""
    app.camera._impl._has_permission = 1

    result = app.camera.start_scanning()

    app.camera.stop_scanning()
    assert_action_performed(app.camera, "stop scanning")

    assert app.loop.run_until_complete(result) is None


def test_is_scanning_during_scan(app):
    """is_scanning reflects the active scanning state."""
    app.camera._impl._has_permission = 1

    _ = app.camera.start_scanning()

    assert app.camera.is_scanning is True
    assert_action_performed(app.camera, "is scanning")

    app.camera.stop_scanning()

    assert app.camera.is_scanning is False
    assert_action_performed(app.camera, "is scanning")


def test_on_detection_callback_invoked(app):
    """The on_detection callback is invoked when a barcode is detected."""
    app.camera._impl._has_permission = 1

    detected = []

    def handler(camera, content, **kwargs):
        detected.append((camera, content))

    app.camera._impl.simulate_scan("callback_content")
    app.loop.run_until_complete(app.camera.start_scanning(on_detection=handler))

    assert len(detected) == 1
    assert detected[0][0] is app.camera
    assert detected[0][1] == "callback_content"


def test_scan_result_direct_comparison_error(app):
    """ScanResult raises RuntimeError if compared directly."""
    result = app.camera.start_scanning()
    with pytest.raises(RuntimeError):
        _ = result == "anything"


def test_scan_result_repr(app):
    """ScanResult repr is meaningful."""
    result = app.camera.start_scanning()
    assert "scan" in repr(result).lower()
