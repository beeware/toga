import pytest

import toga
from toga.constants import FlashMode
from toga.hardware.camera import CameraDevice
from toga_dummy import factory
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
    try:
        monkeypatch.delattr(app, "_camera")
    except AttributeError:
        pass
    monkeypatch.delattr(factory, "Camera")

    # Accessing the camera object should raise NotImplementedError
    with pytest.raises(NotImplementedError):
        app.camera


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

    # ... but the result won't be directly comparable
    with pytest.raises(RuntimeError):
        # == True isn't good python, but it's going to raise an exception anyway.
        result == True  # noqa: E712


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
