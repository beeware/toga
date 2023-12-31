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

    # Reset the photo permissions
    camera_probe.reset_photo_permission()

    # Initiate the permission request
    assert await app.camera.request_photo_permission()

    # Permission now exists
    assert app.camera.has_photo_permission


async def test_take_photo(app, camera_probe):
    """A user can take a photo with the all the available cameras"""

    # Ensure the camera has permissions
    camera_probe.grant_photo_permission()

    for camera in [None] + app.camera.devices:
        # Trigger taking a photo
        photo = app.camera.take_photo(device=camera)

        # Simulate pressing the shutter on the camera
        image = await camera_probe.take_photo(photo)

        # The image exists, and has the expected size.
        assert image.size == (512, 512)


async def test_flash_mode(app, camera_probe):
    """A user can take a photo with all the flash modes"""

    # Ensure the camera has permissions
    camera_probe.grant_photo_permission()

    for flash_mode in [FlashMode.AUTO, FlashMode.ON, FlashMode.OFF]:
        # Trigger taking a photo with the default device
        photo = app.camera.take_photo(flash=flash_mode)

        # Simulate pressing the shutter on the camera
        image = await camera_probe.take_photo(photo)

        # The image exists, and has the expected size.
        assert image.size == (512, 512)


async def test_take_photo_unknown_permission(app, camera_probe):
    """If a user hasn't explicitly granted permissions, they can take a photo with the camera"""

    # This test relies on the fact that permissions have been "pre-granted".

    # Trigger taking a photo
    photo = app.camera.take_photo()

    # Simulate pressing the shutter on the camer
    image = await camera_probe.take_photo(photo)

    # The image exists, and has the expected size.
    assert image.size == (512, 512)


async def test_cancel_photo(app, camera_probe):
    """A user can cancel taking a photo"""

    # Ensure the camera has permissions
    camera_probe.grant_photo_permission()

    # Trigger taking a photo
    photo = app.camera.take_photo()

    # Simulate pressing the shutter on the camer
    image = await camera_probe.cancel_photo(photo)

    # No image was returned
    assert image is None


async def test_take_photo_no_permission(app, camera_probe):
    """If the user doesn't have camera permission, an error is raised"""
    # Revoke camera permission
    camera_probe.deny_photo_permission()

    with pytest.raises(PermissionError):
        await app.camera.take_photo()
