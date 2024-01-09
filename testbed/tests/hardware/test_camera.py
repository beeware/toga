import pytest

from toga.constants import FlashMode

from ..conftest import skip_on_platforms
from .probe import get_probe


@pytest.fixture
async def camera_probe(monkeypatch, app_probe):
    skip_on_platforms("android", "linux", "windows")
    return get_probe(monkeypatch, app_probe, "Camera")


async def test_camera_properties(app, camera_probe):
    assert {
        device.id: app.camera.has_flash(device) for device in app.camera.devices
    } == camera_probe.known_cameras()


async def test_grant_photo_permission(app, camera_probe):
    """A user can grant permission to use the camera"""
    # Reset camera permissions
    camera_probe.reset_photo_permission()

    # Initiate the permission request. Since there hasn't been an explicit
    # allow or deny, this will allow access.
    assert await app.camera.request_photo_permission()

    # Permission now exists
    assert app.camera.has_photo_permission

    # A second request to grant permissions is a no-op
    assert await app.camera.request_photo_permission()

    # Permission still exists
    assert app.camera.has_photo_permission


async def test_take_photo(app, camera_probe):
    """A user can take a photo with the all the available cameras"""

    # Ensure the camera has permissions
    camera_probe.allow_photo_permission()

    for camera in [None] + app.camera.devices:
        # Trigger taking a photo
        photo = app.camera.take_photo(device=camera)
        await camera_probe.wait_for_camera()

        # Simulate pressing the shutter on the camera
        image, device_used, _ = await camera_probe.press_shutter_button(photo)

        # The image exists, and has the expected size, using the requested camera
        assert image.size == (512, 512)
        assert camera_probe.same_device(camera, device_used)


async def test_flash_mode(app, camera_probe):
    """A user can take a photo with all the flash modes"""

    # Ensure the camera has permissions
    camera_probe.allow_photo_permission()

    for flash_mode in [FlashMode.AUTO, FlashMode.ON, FlashMode.OFF]:
        # Trigger taking a photo with the default device
        photo = app.camera.take_photo(flash=flash_mode)
        await camera_probe.wait_for_camera()

        # Simulate pressing the shutter on the camera
        image, _, flash_mode_used = await camera_probe.press_shutter_button(photo)

        # The image exists, and has the expected size.
        assert image.size == (512, 512)
        assert camera_probe.same_flash_mode(flash_mode, flash_mode_used)


async def test_take_photo_unknown_permission(app, camera_probe):
    """If a user hasn't explicitly granted permissions, they can take a photo with the camera"""
    # Don't pre-grant permission; use default grant.

    # Trigger taking a photo
    photo = app.camera.take_photo()
    await camera_probe.wait_for_camera()

    # Simulate pressing the shutter on the camera
    image, _, _ = await camera_probe.press_shutter_button(photo)

    # The image exists, and has the expected size.
    assert image.size == (512, 512)


async def test_cancel_photo(app, camera_probe):
    """A user can cancel taking a photo"""

    # Ensure the camera has permissions
    camera_probe.allow_photo_permission()

    # Trigger taking a photo
    photo = app.camera.take_photo()
    await camera_probe.wait_for_camera()

    # Simulate pressing the shutter on the camer
    image = await camera_probe.cancel_photo(photo)

    # No image was returned
    assert image is None


async def test_take_photo_no_permission(app, camera_probe):
    """If the user doesn't have camera permission, an error is raised"""
    # Revoke camera permission
    camera_probe.reject_photo_permission()

    with pytest.raises(PermissionError):
        await app.camera.take_photo()


async def test_change_camera(app, camera_probe):
    """The currently selected camera can be changed"""

    # Ensure the camera has permissions
    camera_probe.allow_photo_permission()

    # Trigger taking a photo
    photo = app.camera.take_photo()
    await camera_probe.wait_for_camera()

    # Select the second camera
    selected_device = camera_probe.select_other_camera()
    await camera_probe.redraw("New camera selected")

    # The shutter is enabled
    assert camera_probe.shutter_enabled

    # Simulate pressing the shutter on the camer
    image, used_device, _ = await camera_probe.press_shutter_button(photo)

    # The camera used the selected device
    assert camera_probe.same_device(selected_device, used_device)
    assert image is not None


async def test_no_cameras(app, camera_probe):
    """If there are no cameras attached, the dialog is displayed, but the button is disabled"""
    # Disconnect the cameras
    camera_probe.disconnect_cameras()

    # Ensure the camera has permissions
    camera_probe.allow_photo_permission()

    # Trigger taking a photo
    photo = app.camera.take_photo()
    await camera_probe.wait_for_camera(device_count=0)

    # The shutter is *not* enabled
    assert not camera_probe.shutter_enabled

    # Simulate pressing the shutter on the camer
    image = await camera_probe.cancel_photo(photo)

    # No image was returned
    assert image is None
