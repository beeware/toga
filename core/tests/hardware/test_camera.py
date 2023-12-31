import pytest

import toga
from toga.constants import FlashMode
from toga_dummy import factory
from toga_dummy.hardware.camera import Camera as DummyCamera
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)


@pytest.fixture
def photo(app):
    return toga.Image("resources/photo.png")


def test_no_camera(monkeypatch, app):
    """If there's no camera, and no factory implementation, accessing camera raises an exception"""
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
def test_request_photo_permission(app, initial, should_request, has_permission):
    """An app can request permission to take photos"""
    # The camera instance round-trips the app instance
    assert app.camera.app == app

    # Set initial permission
    app.camera._impl._has_photo_permission = initial

    assert (
        app.loop.run_until_complete(app.camera.request_photo_permission())
        == has_permission
    )

    if should_request:
        assert_action_performed(app.camera, "request photo permission")
    else:
        assert_action_not_performed(app.camera, "request photo permission")

    # As a result of requesting, photo permission is as expected
    assert app.camera.has_photo_permission == has_permission


def test_request_photo_permission_sync(app):
    """An app can synchronously request permission to take photos"""
    # Set initial permission
    app.camera._impl._has_photo_permission = -1

    result = app.camera.request_photo_permission()

    # This will cause a permission request to occur...
    assert_action_performed(app.camera, "request photo permission")

    # ... but the result won't be directly comparable
    with pytest.raises(RuntimeError):
        # == True isn't good python, but it's going to raise an exception anyway.
        result == True  # noqa: E712


def test_device_properties(app):
    """Device properties can be checked"""

    assert [
        {
            "device": device,
            "__str__": str(device),
            "name": device.name,
            "id": device.id,
            "has_flash": app.camera.has_flash(device),
        }
        for device in app.camera.devices
    ] == [
        {
            "device": DummyCamera.CAMERA_1,
            "__str__": "Camera 1",
            "name": "Camera 1",
            "id": "camera-1",
            "has_flash": True,
        },
        {
            "device": DummyCamera.CAMERA_2,
            "__str__": "Camera 2",
            "name": "Camera 2",
            "id": "camera-2",
            "has_flash": False,
        },
    ]


@pytest.mark.parametrize(
    "device",
    [None, DummyCamera.CAMERA_1, DummyCamera.CAMERA_2],
)
@pytest.mark.parametrize(
    "flash",
    [FlashMode.AUTO, FlashMode.ON, FlashMode.OFF],
)
def test_take_photo_with_permission(app, device, flash, photo):
    """If permission has not been previously requested, it is requested before a photo is taken."""
    # Set permission to potentially allowed
    app.camera._impl._has_photo_permission = -1

    app.camera._impl.simulate_photo(photo)

    result = app.loop.run_until_complete(
        app.camera.take_photo(device=device, flash=flash)
    )

    # Photo was returned
    assert result == photo

    assert_action_performed(app.camera, "has photo permission")
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
    app.camera._impl._has_photo_permission = 1

    # Simulate the camera response
    app.camera._impl.simulate_photo(photo)

    result = app.loop.run_until_complete(app.camera.take_photo())

    # Photo was returned
    assert result == photo

    assert_action_performed(app.camera, "has photo permission")
    assert_action_performed_with(
        app.camera,
        "take photo",
        permission_requested=False,
        device=None,
        flash=FlashMode.AUTO,
    )


def test_take_photo_no_permission(app, photo):
    """If permission has been denied, an exception is raised"""
    # Deny permission
    app.camera._impl._has_photo_permission = 0

    with pytest.raises(
        PermissionError,
        match=r"App does not have permission to take photos",
    ):
        app.loop.run_until_complete(app.camera.take_photo())

    assert_action_performed(app.camera, "has photo permission")
    assert_action_not_performed(app.camera, "take photo")
