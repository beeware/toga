import warnings

import pytest

from toga.constants import FlashMode

from .probe import list_probes


@pytest.fixture(
    params=list_probes(
        "camera",
        skip_platforms=("linux", "windows"),
        skip_unbundled=True,
    )
)
async def camera_probe(monkeypatch, app_probe, request):
    probe_cls = request.param
    probe = probe_cls(monkeypatch, app_probe)
    yield probe
    probe.cleanup()


async def test_camera_properties(app, camera_probe):
    assert {
        device.id: (device.name, device.has_flash) for device in app.camera.devices
    } == camera_probe.known_cameras()


async def test_grant_permission(app, camera_probe):
    """A user can grant permission to use the camera"""
    # Prime the permission system to approve permission requests
    camera_probe.allow_permission()

    # Initiate the permission request. As permissions are primed, they will be approved.
    assert await app.camera.request_permission()

    # Permission now exists
    assert app.camera.has_permission

    # A second request to grant permissions is a no-op
    assert await app.camera.request_permission()

    # Permission still exists
    assert app.camera.has_permission


async def test_deny_permission(app, camera_probe):
    """A user can deny permission to use the camera"""
    # Initiate the permission request. As permissions are not primed,
    # they will be denied.
    assert not await app.camera.request_permission()

    # Permission has been denied
    assert not app.camera.has_permission

    # A second request to request permissions is a no-op
    assert not await app.camera.request_permission()

    # Permission is still denied
    assert not app.camera.has_permission


async def test_take_photo(app, camera_probe):
    """A user can take a photo with the all the available cameras"""
    # Ensure the camera has permissions
    camera_probe.grant_permission()

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
    camera_probe.grant_permission()

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
    """If a user hasn't explicitly granted permissions,
    they can take a photo with the camera"""
    if not camera_probe.request_permission_on_first_use:
        pytest.xfail("Platform does not request permission on first use")

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
    camera_probe.grant_permission()

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
    camera_probe.reject_permission()

    with pytest.raises(PermissionError):
        await app.camera.take_photo()


async def test_change_camera(app, camera_probe):
    """The currently selected camera can be changed"""
    # Ensure the camera has permissions
    camera_probe.grant_permission()

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
    """If there are no cameras attached, the only option is cancelling."""
    # Disconnect the cameras
    camera_probe.disconnect_cameras()

    # Ensure the camera has permissions
    camera_probe.grant_permission()

    # Trigger taking a photo. This may raise a warning.
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "No camera is available")
        photo = app.camera.take_photo()

    # Some platforms (e.g., macOS) can't know ahead of time that there are no cameras,
    # so they show the camera dialog, but disable the shutter until a camera is
    # available, leaving cancel as the only option. Other platforms know ahead of time
    # that there are no cameras, so they can short cut and cancel the photo request.
    if camera_probe.allow_no_camera:
        await camera_probe.wait_for_camera(device_count=0)

        # The shutter is *not* enabled
        assert not camera_probe.shutter_enabled

        # Simulate pressing the shutter on the camera
        image = await camera_probe.cancel_photo(photo)
    else:
        image = await photo

    # No image was returned
    assert image is None
