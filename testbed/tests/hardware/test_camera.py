import pytest

from toga.constants import FlashMode
from toga.hardware.camera import Camera

from ..conftest import skip_on_platforms
from .probe import get_probe


@pytest.fixture
async def camera_probe(monkeypatch, app_probe):
    skip_on_platforms("android", "macOS", "linux", "windows")
    return get_probe(monkeypatch, app_probe, "Camera")


async def test_camera_properties(app, camera_probe):
    assert app.camera.devices == camera_probe.known_cameras()

    assert app.camera.has_flash(Camera.FRONT) == camera_probe.has_flash(Camera.FRONT)
    assert app.camera.has_flash(Camera.REAR) == camera_probe.has_flash(Camera.REAR)
    assert app.camera.has_flash(None) == camera_probe.has_flash(Camera.REAR)

    # Test the properties of a camera that doesn't exist
    with pytest.raises(ValueError, match=r"Unknown camera device 'selfiestick'"):
        app.camera.has_flash("selfiestick")


async def test_grant_photo_permission(app, camera_probe):
    """A user can grant permission to use the camera"""

    # Reset the photo permissions
    camera_probe.reset_photo_permission()

    # Initiate the permission request
    assert await app.camera.request_photo_permission()

    # Permission now exists
    assert app.camera.has_photo_permission


@pytest.mark.parametrize(
    "camera,flash_mode",
    [
        (None, None),
        (Camera.FRONT, FlashMode.AUTO),
        (Camera.REAR, FlashMode.AUTO),
        (Camera.REAR, FlashMode.ON),
        (Camera.REAR, FlashMode.OFF),
    ],
)
async def test_take_photo(app, camera_probe, camera, flash_mode):
    """A user can take a photo with the camera"""

    # Ensure the camera has permissions
    camera_probe.grant_photo_permission()

    # Trigger taking a photo
    photo = app.camera.take_photo(device=camera, flash=flash_mode)

    # Simulate pressing the shutter on the camer
    image = await camera_probe.take_photo(photo)

    # The image exists, and has the expected size.
    assert image.size == (512, 512)


async def test_take_photo_unknown_permission(app, camera_probe):
    """A user can take a photo with the camera,"""

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
